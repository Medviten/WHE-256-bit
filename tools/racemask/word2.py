"""Add second race-mask word (races 65-128) handling to WHE-256-bit modpak SQL.

  python word2.py MODPAKS report   -- list what would change and what needs a manual look
  python word2.py MODPAKS apply    -- rewrite the files

Mirroring: a statement that writes a word-0 mask column (see MASK_COLS) with an expression that uses a faction-wide
mask variable (AGGREGATES) or the mask of a race above 64 gets a matching assignment/value for <column>_2, where every
race-mask variable @X becomes @X_2 and every mask column c becomes c_2. Statements are never split or reordered.

When adding a race above 64: add its name to WORD2_RACES below, run word2vars.py (variables) and then this script,
both with `report` first. Both are idempotent, so re-running them on already converted files changes nothing."""
import os, re, sys

MODPAKS, MODE = sys.argv[1], sys.argv[2]

AGGREGATES = ["VanillaAllianceMask", "VanillaHordeMask", "BaseAllianceMask", "BaseHordeMask", "AllianceMask", "HordeMask",
              "UndercityMask", "BarrensBros", "PlayableRaceMask", "GunHunters", "CrossbowHunters", "BowHunters",
              "ExtendedAllianceMask", "ExtendedHordeMask"]
MASK_COLS = {"reputation_race_mask_1", "reputation_race_mask_2", "reputation_race_mask_3", "reputation_race_mask_4",
             "required_races", "race_mask", "racemask", "allowableraces", "allowablerace"}
WORD2_RACES = {"AllianceEarthen", "HordeEarthen"}


def races():
    names = set()
    txt = open(os.path.join(MODPAKS, "config.sql"), encoding="utf-8").read()
    names |= set(re.findall(r"^SET @(\w+)Mask\s*=\s*1\s*<<", txt, re.M))
    for d in os.listdir(MODPAKS):
        v = os.path.join(MODPAKS, d, "variables.sql")
        if os.path.exists(v):
            names |= set(re.findall(r"^SET @(\w+)Mask\s*=\s*1\s*<<", open(v, encoding="utf-8").read(), re.M))
    return names | WORD2_RACES


RACES = races()
MASKVARS = set(AGGREGATES) | {r + "Mask" for r in RACES}
VAR_RE = re.compile(r"@(\w+)\b")
TRIGGER = set(AGGREGATES) | {r + "Mask" for r in WORD2_RACES}


def mask_vars(expr):
    return [v for v in VAR_RE.findall(expr) if v in MASKVARS]


def mirror(expr):
    def var(m):
        return "@" + m.group(1) + "_2" if m.group(1) in MASKVARS else m.group(0)
    out = VAR_RE.sub(var, expr)
    def col(m):
        return "`" + m.group(1) + "_2`" if m.group(1).lower() in MASK_COLS else m.group(0)
    return re.sub(r"`(\w+)`", col, out)


def literal_bits(expr):
    """Non-zero integer literals that are OR-ed/assigned (would wrongly set word-2 bits when copied)."""
    scrubbed = VAR_RE.sub("V", expr)
    scrubbed = re.sub(r"`\w+`", "C", scrubbed)
    return [n for n in re.findall(r"(?<![\w.])-?\d+(?![\w.])", scrubbed) if n not in ("0",)]


# ----------------------------------------------------------------------------------------------- tokenizer
def split_statements(text):
    """Yield (start, end) of each statement (end is index of ';' + 1), respecting quotes and comments."""
    i, n, start = 0, len(text), 0
    state = None
    while i < n:
        c = text[i]
        if state in ("'", '"'):
            if c == "\\":
                i += 2; continue
            if c == state:
                state = None
        elif state == "`":
            if c == "`":
                state = None
        elif state == "/*":
            if text.startswith("*/", i):
                state = None; i += 2; continue
        elif state == "--":
            if c == "\n":
                state = None
        else:
            if c in "'\"`":
                state = c
            elif text.startswith("/*", i):
                state = "/*"; i += 2; continue
            elif (text.startswith("--", i) and i + 2 < n and text[i + 2] in " \t\r\n") or c == "#":
                state = "--"
            elif c == ";":
                yield start, i + 1
                start = i + 1
        i += 1


def top_level_split(s, sep=","):
    """Split s at top-level separators (outside quotes, parentheses and comments). Returns list of (piece, start)."""
    parts, depth, state, last, i = [], 0, None, 0, 0
    while i < len(s):
        c = s[i]
        if state in ("'", '"'):
            if c == "\\":
                i += 2; continue
            if c == state:
                state = None
        elif state == "`":
            if c == "`":
                state = None
        elif state == "--":
            if c == "\n":
                state = None
        else:
            if c in "'\"`":
                state = c
            elif s.startswith("--", i) and i + 2 < len(s) and s[i + 2] in " \t\r\n":
                state = "--"
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            elif c == sep and depth == 0:
                parts.append((s[last:i], last)); last = i + 1
        i += 1
    parts.append((s[last:], last))
    return parts


def strip_comments(s):
    out, state, i = [], None, 0
    while i < len(s):
        c = s[i]
        if state in ("'", '"'):
            out.append(c)
            if c == "\\":
                out.append(s[i + 1:i + 2]); i += 2; continue
            if c == state:
                state = None
        elif state == "--":
            if c == "\n":
                state = None; out.append(c)
        elif state == "/*":
            if s.startswith("*/", i):
                state = None; i += 2; continue
        else:
            if c in "'\"":
                state = c; out.append(c)
            elif s.startswith("/*", i):
                state = "/*"; i += 2; continue
            elif (s.startswith("--", i) and i + 2 < len(s) and s[i + 2] in " \t\r\n") or c == "#":
                state = "--"
            else:
                out.append(c)
        i += 1
    return "".join(out)


# ------------------------------------------------------------------------------------------- statements
UPDATE_RE = re.compile(r"^(\s*UPDATE\s+`\w+`\s+SET\s+)(.*?)(\s+WHERE\s+.*)?$", re.S | re.I)
INSERT_RE = re.compile(r"^(\s*(?:INSERT|REPLACE)(?:\s+IGNORE)?\s+INTO\s+`\w+`\s*\()(.*?)(\)\s*VALUES\s*)(.*?)(;?)\s*$", re.S | re.I)


def triggers(expr):
    return bool(set(mask_vars(expr)) & TRIGGER)


def rewrite_update(stmt, notes):
    m = UPDATE_RE.match(stmt.rstrip(";"))
    if not m:
        return None
    head, sets, where = m.group(1), m.group(2), m.group(3) or ""
    pieces = top_level_split(sets)
    added = []
    have = {p.split("=", 1)[0].strip().strip("`").lower() for p, _ in pieces if "=" in p}
    for piece, _ in pieces:
        if "=" not in piece:
            continue
        col, expr = piece.split("=", 1)
        c = col.strip().strip("`")
        if c.lower() in MASK_COLS and triggers(expr) and (c + "_2").lower() not in have:
            lits = literal_bits(expr)
            if lits:
                notes.append(f"literal mask bits {lits} in: {piece.strip()[:120]}")
            added.append(f"`{c}_2` = {mirror(strip_comments(expr).strip())}")
    if where and re.search(r"`(\w+)`\s*=\s*@", where) and any(
            m2.group(1).lower() in MASK_COLS for m2 in re.finditer(r"`(\w+)`\s*=\s*@", where)):
        notes.append(f"equality on a mask column in WHERE: {where.strip()[:120]}")
    if not added:
        return None
    # insert the new assignments after the last SET piece, before WHERE / trailing comments
    sets_clean = sets.rstrip()
    trail = sets[len(sets_clean):]
    new_sets = sets_clean + ",\n    " + ",\n    ".join(added) + trail
    return head + new_sets + where + (";" if stmt.rstrip().endswith(";") else "")


def rewrite_insert(stmt, notes):
    m = INSERT_RE.match(stmt)
    if not m:
        if re.match(r"^\s*(INSERT|REPLACE)", stmt, re.I) and any(v in TRIGGER for v in mask_vars(stmt)):
            notes.append(f"INSERT form not handled: {stmt.strip()[:140]}")
        return None
    head, cols, mid, values, semi = m.groups()
    col_list = [c.strip().strip("`") for c, _ in top_level_split(cols)]
    idx = [i for i, c in enumerate(col_list) if c.lower() in MASK_COLS]
    if not idx or any(c.lower().endswith("_2") and c.lower()[:-2] in MASK_COLS for c in col_list):
        return None
    tuples = [t for t in top_level_split(values) if t[0].strip()]
    any_trigger = False
    new_tuples = []
    for t, _ in tuples:
        # a tuple piece may start with comment lines (between tuples) and end with a trailing comment
        open_at, k, in_comment = -1, 0, False
        while k < len(t):
            if in_comment:
                if t[k] == "\n":
                    in_comment = False
            elif t.startswith("--", k):
                in_comment = True
            elif t[k] == "(":
                open_at = k
                break
            k += 1
        if open_at < 0:
            notes.append(f"unparsed VALUES tuple: {t.strip()[:100]}")
            return None
        lead, rest = t[:open_at], t[open_at:]
        close = rest.rfind(")")
        inner, after = rest[1:close], rest[close + 1:]
        if strip_comments(after).strip():
            notes.append(f"unparsed VALUES tuple tail: {t.strip()[:100]}")
            return None
        vals = [v for v, _ in top_level_split(inner)]
        if len(vals) != len(col_list):
            notes.append(f"{len(vals)} values for {len(col_list)} columns: {t.strip()[:100]}")
            return None
        extra = []
        for i in idx:
            v = strip_comments(vals[i]).strip()
            if triggers(v):
                any_trigger = True
            lits = literal_bits(v)
            if lits and triggers(v):
                notes.append(f"literal mask bits {lits} in value: {v[:100]}")
            extra.append(mirror(v) if mask_vars(v) else "0")
        new_tuples.append(lead + "(" + inner.rstrip() + ", " + ", ".join(extra) + ")" + after)
    if not any_trigger:
        return None
    new_cols = cols.rstrip() + ", " + ", ".join(f"`{col_list[i]}_2`" for i in idx)
    return head + new_cols + mid + ",".join(new_tuples) + semi


def rewrite_delete(stmt, notes):
    if not re.match(r"^\s*DELETE\s", stmt, re.I):
        return None
    hits = [m for m in re.finditer(r"`(\w+)`\s*=\s*(@\w+)", stmt) if m.group(1).lower() in MASK_COLS and m.group(2)[1:] in MASKVARS]
    if not hits or not any(h.group(2)[1:] in TRIGGER for h in hits) or re.search(r"`\w+_2`\s*=\s*@", stmt):
        return None
    out = stmt
    for h in reversed(hits):
        add = f" AND `{h.group(1)}_2` = {h.group(2)}_2"
        out = out[:h.end()] + add + out[h.end():]
    return out


def process(path, report):
    text = open(path, encoding="utf-8").read()
    pieces, last, changed, notes = [], 0, 0, []
    for a, b in split_statements(text):
        stmt = text[a:b]
        # leading comments/blank lines belong to the statement text but must stay untouched
        lead_len = len(stmt) - len(stmt.lstrip())
        body = stmt[lead_len:]
        # skip leading comment lines
        m = re.match(r"((?:\s*(?:--[^\n]*|/\*.*?\*/)\s*)*)(.*)", body, re.S)
        comments, core = m.group(1), m.group(2)
        new = None
        if re.match(r"\s*UPDATE\s", core, re.I):
            new = rewrite_update(core, notes)
        elif re.match(r"\s*(INSERT|REPLACE)\s", core, re.I):
            new = rewrite_insert(core, notes)
        elif re.match(r"\s*DELETE\s", core, re.I):
            new = rewrite_delete(core, notes)
        else:
            if any(v in TRIGGER for v in mask_vars(strip_comments(core))) and not re.match(r"\s*SET\s", core, re.I):
                notes.append(f"statement type not handled: {core.strip()[:120]}")
        pieces.append(text[last:a])
        if new is not None and new != core:
            changed += 1
            pieces.append(stmt[:lead_len] + comments + new)
        else:
            pieces.append(stmt)
        last = b
    pieces.append(text[last:])
    out = "".join(pieces)
    if report:
        return changed, notes, out
    if changed:
        open(path, "w", encoding="utf-8", newline="\n").write(out)
    return changed, notes, out


total = 0
for root, _, files in os.walk(MODPAKS):
    for f in sorted(files):
        if not f.endswith(".sql") or f in ("variables.sql", "config.sql"):
            continue
        p = os.path.join(root, f)
        changed, notes, _ = process(p, MODE == "report")
        if changed or notes:
            total += changed
            print(f"{os.path.relpath(p, MODPAKS)}: {changed} statement(s)")
            for n in notes:
                print("   !", n)
print("total statements:", total)
