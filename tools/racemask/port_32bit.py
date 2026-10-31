"""Port WHE-256-bit modpaks to the 32-bit racemask version (WHE-32-bit / mod-worgoblin-high-elf).

  python port_32bit.py SRC_MODPAKS DEST_MODPAKS [MODPAK ...]   -- write the ported modpaks (all when none named)
  python port_32bit.py SRC_MODPAKS DEST_MODPAKS --config        -- write config.sql only

The reverse of word2vars.py and word2.py, plus the race IDs:
- every second race-mask word goes: `SET @X_2 = ...; -- races 65-128` lines, `<mask column>_2` columns and their
  values in INSERTs, `<mask column>_2 = ...` assignments in UPDATEs and `AND <mask column>_2 = @X_2` in WHEREs
- race IDs are fixed in the 256-bit config.sql but auto-incremented in the 32-bit version: a variables.sql that
  defines a race mask gets `SET @X := @NextRace := @NextRace +1;` before it, and the fixed-ID block of config.sql
  becomes the single @NextRace line
- readmes lose their "race ID N" mentions, which are only true in the 256-bit version

When the 32-bit version already has a file, its own choices survive the port (see merge_sets): the race ID, mask and
helmet mask lines of a variables.sql (some races have fixed IDs there, e.g. Goblin 9 and Worgen 12), the KEEP_VARS
values of config.sql and every SET line that only the 32-bit file has. Files in KEEP_FILES are left as they are,
files in SKIP_FILES are not ported (they need the 256-bit core or client).

Whatever the 32-bit SQL cannot express is reported (and left in place): leftover _2 variables or columns and mask
literals above 32 bits. Non-SQL files are copied unchanged."""
import os, re, shutil, sys

# 32-bit choices that differ from the 256-bit version on purpose
KEEP_FILES = {
    "F-013_zep-goblin-start/dbc/[I-334]_creaturedisplayinfoextra.sql",  # Worgen is dynamic (12), not retail 22
    "F-024_mod-playable-worgen/dbc/[BASE,F-024]_skilllineability.sql",  # Running Wild row (src/modpaks/F-024...)
    "F-024_mod-playable-worgen/sql/db-world/base/[F-024]_spell_script_names.sql",
    "F-026_custom-race-support/readme.md",                              # no spillover table (256-bit core only)
    "F-026_custom-race-support/variables.sql",
    "F-032_mod-taunka/dbc/[BASE,F-032]_creaturemodeldata.sql",          # Taunka keep the Tauren female
    "F-063_worgen_racial_spells/dbc/[F-063]_spell.sql",
}
SKIP_FILES = {
    "F-026_custom-race-support/sql/db-world/base/[BASE,F-026]_reputation_spillover_faction.sql",  # 256-bit core table
}
KEEP_VARS = {"GoblinMask", "GoblinHelmetMask", "TaunkaFemaleModel"}  # config.sql
SET_VAR = re.compile(r"^(?:--\s*)?SET @(\w+)\s*:?=")

MASK_COLS = {"reputation_race_mask_1", "reputation_race_mask_2", "reputation_race_mask_3", "reputation_race_mask_4",
             "required_races", "race_mask", "racemask", "allowableraces", "allowablerace"}
CLASS_MASKS = ("Warrior", "Paladin", "Hunter", "Rogue", "Priest", "DeathKnight", "Shaman", "Mage", "Warlock", "Monk",
               "Druid", "DemonHunter", "Evoker")
MASK_DEF = re.compile(r"^SET @(\w+)Mask(\s*)=\s*1\s*<<\s*\(@(\w+)\s*-\s*1\);(.*)$")
WORD2_LINE = re.compile(r"^.*-- races 65-128\s*$")
VAR_2 = re.compile(r"@\w+_2\b")
COL_2 = re.compile(r"`(\w+)_2`")


def is_mask_col_2(name):
    return name.lower().endswith("_2") and name.lower()[:-2] in MASK_COLS


# ----------------------------------------------------------------------------------------------- tokenizer
# (the same quote/comment-aware splitting as word2.py)
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
        elif state == "/*":
            if s.startswith("*/", i):
                state = None; i += 2; continue
        else:
            if c in "'\"`":
                state = c
            elif s.startswith("--", i) and i + 2 < len(s) and s[i + 2] in " \t\r\n":
                state = "--"
            elif s.startswith("/*", i):
                state = "/*"; i += 2; continue
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


def drop_pieces(s, drop):
    """Rejoin top-level comma pieces of s without those for which drop(piece) is true, dropping the comma before each
    dropped piece (or after it, for the first one)."""
    pieces = top_level_split(s)
    keep = [not drop(p) for p, _ in pieces]
    if all(keep):
        return s
    out, first = [], True
    for (p, _), k in zip(pieces, keep):
        if not k:
            continue
        if first:
            out.append(p.lstrip() if not keep[0] else p)
            first = False
        else:
            out.append("," + p)
    return "".join(out)


# ------------------------------------------------------------------------------------------- statements
UPDATE_RE = re.compile(r"^(\s*UPDATE\s+.*?\s+SET\s+)(.*?)(\s+WHERE\s+.*)?$", re.S | re.I)
INSERT_RE = re.compile(r"^(\s*(?:INSERT|REPLACE)(?:\s+IGNORE)?\s+INTO\s+`\w+`\s*\()(.*?)(\)\s*)(VALUES\s*.*|SELECT\s.*)$",
                       re.S | re.I)
WHERE_2 = re.compile(r"\s+AND\s+`(\w+)_2`\s*=\s*@\w+_2\b", re.I)


def col_name(piece):
    return strip_comments(piece).strip().strip("`")


def rewrite_insert(stmt):
    m = INSERT_RE.match(stmt)
    if not m:
        return stmt
    head, cols, mid, rest = m.groups()
    col_list = [col_name(c) for c, _ in top_level_split(cols)]
    idx = {i for i, c in enumerate(col_list) if is_mask_col_2(c)}
    if not idx:
        return stmt
    new_cols = drop_pieces(cols, lambda p: is_mask_col_2(col_name(p)))
    if re.match(r"SELECT\s", rest, re.I):
        sel = re.match(r"(SELECT\s+)(.*?)(\s+FROM\s.*)$", rest, re.S | re.I)
        if not sel:
            return stmt
        items = top_level_split(sel.group(2))
        if len(items) != len(col_list):
            return stmt
        k = iter(range(len(items)))
        new_items = drop_pieces(sel.group(2), lambda p: next(k) in idx)
        return head + new_cols + mid + sel.group(1) + new_items + sel.group(3)
    vm = re.match(r"(VALUES\s*)(.*?)(;?\s*)$", rest, re.S | re.I)
    values, tail = vm.group(2), vm.group(3)
    out = []
    for t, _ in top_level_split(values):
        if not t.strip():
            out.append(t)
            continue
        # a tuple piece may start with comment lines (between tuples) and end with a trailing comment
        k, open_at, in_comment = 0, -1, False
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
            return stmt
        lead, body = t[:open_at], t[open_at:]
        close = body.rfind(")")
        inner, after = body[1:close], body[close + 1:]
        vals = top_level_split(inner)
        if len(vals) != len(col_list):
            return stmt
        n = iter(range(len(vals)))
        out.append(lead + "(" + drop_pieces(inner, lambda p: next(n) in idx) + ")" + after)
    return head + new_cols + mid + vm.group(1) + ",".join(out) + tail


def rewrite_update(stmt):
    m = UPDATE_RE.match(stmt)
    if not m:
        return stmt
    head, sets, where = m.group(1), m.group(2), m.group(3) or ""
    if not COL_2.search(sets):
        return head + sets + WHERE_2.sub("", where)

    def drop(p):
        return "=" in p and is_mask_col_2(col_name(p.split("=", 1)[0]))
    return head + drop_pieces(sets, drop) + WHERE_2.sub("", where)


def port_sql(text):
    pieces, last = [], 0
    for a, b in split_statements(text):
        stmt = text[a:b]
        lead = re.match(r"((?:\s*(?:--[^\n]*|#[^\n]*|/\*.*?\*/))*\s*)", stmt, re.S).group(1)
        core = stmt[len(lead):]
        semi = core.endswith(";")
        body = core[:-1] if semi else core
        if re.match(r"(INSERT|REPLACE)\s", body, re.I):
            body = rewrite_insert(body)
        elif re.match(r"UPDATE\s", body, re.I):
            body = rewrite_update(body)
        else:
            body = WHERE_2.sub("", body)
        pieces.append(text[last:a] + lead + body + (";" if semi else ""))
        last = b
    pieces.append(text[last:])
    return "".join(pieces)


# ----------------------------------------------------------------------------------------------- variables
def port_variables(text, defined):
    """Drop the word-2 lines and the fixed-ID notes; define each race whose mask is set here (and that is not defined
    earlier in the file or in `defined`) with @NextRace."""
    out = []
    lines = text.split("\n")
    for line in lines:
        if WORD2_LINE.match(line):
            continue
        if line.startswith("-- Race masks (race IDs are fixed in config.sql)"):
            out.append("-- Race ID")
            continue
        m = MASK_DEF.match(line)
        if m and not m.group(1).endswith("Helmet") and m.group(1) not in CLASS_MASKS:
            race = m.group(3)
            if race not in defined and not any(re.match(r"SET @%s\s*:?=" % race, l) for l in out):
                width = len("SET @" + m.group(1) + "Mask" + m.group(2))
                out.append(("SET @" + race).ljust(width) + ":= @NextRace := @NextRace +1;")
        line = re.sub(r"(;)\s*-- race ID \d+.*$", r"\1", line)
        out.append(line)
    return "\n".join(out)


def race_vars(text):
    """The race ID, mask and helmet mask variables a variables.sql defines."""
    names = set()
    for m in re.finditer(r"^SET @(\w+)Mask\s*=\s*1\s*<<\s*\(@(\w+)\s*-\s*1\);", text, re.M):
        if not m.group(1).endswith("Helmet") and m.group(1) not in CLASS_MASKS:
            names |= {m.group(2), m.group(1) + "Mask", m.group(1) + "HelmetMask"}
    return names


def merge_sets(port, dest, keep, notes, path):
    """Port text with the dest's lines for the `keep` variables, plus every SET line only dest has (placed after the
    line of the nearest earlier variable both have)."""
    plines, dlines = port.split("\n"), dest.split("\n")
    pidx = {}
    for i, l in enumerate(plines):
        m = SET_VAR.match(l)
        if m and m.group(1) not in pidx:
            pidx[m.group(1)] = i
    dvars = {}
    for l in dlines:
        m = SET_VAR.match(l)
        if m and m.group(1) not in dvars:
            dvars[m.group(1)] = l
    for v in keep:
        if v in pidx and v in dvars:
            plines[pidx[v]] = dvars[v].rstrip("\r") + ("\r" if plines[pidx[v]].endswith("\r") else "")
    inserts, prev = {}, -1
    for l in dlines:
        m = SET_VAR.match(l)
        if not m:
            continue
        if m.group(1) in pidx:
            prev = pidx[m.group(1)]
        elif not m.group(1).endswith("_2"):
            inserts.setdefault(prev, []).append(l)
            notes.append(f"{path}: kept 32-bit-only line: {l.strip()[:100]}")
    out = []
    for l in inserts.get(-1, []):
        out.append(l)
    for i, l in enumerate(plines):
        out.append(l)
        out.extend(inserts.get(i, []))
    return "\n".join(out)


def port_readme(text, name):
    # what the 256-bit core and client do for the races, and where the 32-bit version keeps scripts and core patches
    text = re.sub(r"( {4}- )Retail model and full Retail customization in the wowdecomp-256-bit client[^\n]*",
                  r"\1Retail model and customization only in the 256-bit version (WHE-256-bit with the wowdecomp-256-bit "
                  r"client and azerothcore-wotlk-256-bit)", text)
    text = re.sub(r"( {4}- )Everything else sees the (\w+) model and customization rows \([^\n]*\)",
                  r"\1Shows the \2 model and customization rows", text)
    text = re.sub(r"- (?:wowdecomp-256-bit client built with|azerothcore-wotlk-256-bit with the Retail look)[^\n]*\n", "", text)
    text = text.replace("; `RetailRace_CharacterCreate.lua` for the Retail options", "")
    text = text.replace("C++ scripts in `src/`", "C++ scripts in `src/modpaks/%s/`" % name)
    text = text.replace("(patches/whe-acore.patch)", "(`patches/core/` in this modpak)")
    text = text.replace("The wowdecomp-256-bit client does not have", "The client does not have")
    text = text.replace("- Male only: female characters use the male model and customization",
                        "- Male only: female characters use the male model and customization (F-026's "
                        "`patches/core/male-only-races.patch` creates them male)")
    text = re.sub(r",\s*race IDs?(?: \d+)?(?: \(retail's\))?,? set in config\.sql", "", text)
    text = re.sub(r",\s*race IDs? \d+(?:\s*(?:and|/|,)\s*\d+)*", "", text)
    text = re.sub(r"\s*\(race IDs? \d+(?:\s*(?:and|/|,)\s*\d+)*\)", "", text)
    return text


def port_config(text):
    """The fixed race-ID block becomes the @NextRace line of the 32-bit version."""
    text = "\n".join(l for l in text.split("\n") if not WORD2_LINE.match(l))
    block = re.compile(r"\n\n-- New Playable Races\n.*?\n(?=\n)", re.S)
    m = block.search(text)
    if m:
        text = text[:m.start()] + "\n" + "SET @NextRace".ljust(63) + "=   13; -- Reserved for Worgen (12) and Gilnean " \
            "(13, Worgen + 1 for the client's alteredFormRaces) – increments before assignment\n" + text[m.end():]
    return port_sql(text)


# ------------------------------------------------------------------------------------------------- checks
def check(path, text, notes):
    code = strip_comments(text)
    for v in sorted(set(VAR_2.findall(code))):
        if re.match(r"@\w+(Mask|Bros|Hunters)_2$", v):
            notes.append(f"{path}: second-word variable left: {v}")
    for c in sorted({c for c in COL_2.findall(code) if is_mask_col_2(c + "_2")}):
        notes.append(f"{path}: second-word column left: `{c}_2`")
    for n in re.findall(r"(?<![\w.@'])(\d{11,})(?![\w.'])", code):
        if int(n) > 0xFFFFFFFF:
            notes.append(f"{path}: literal above 32 bits: {n}")


def main():
    src, dest = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    notes = []
    if "--config" in args:
        text = port_config(read(os.path.join(src, "config.sql")))
        d = os.path.join(dest, "config.sql")
        if os.path.exists(d):
            text = merge_sets(text, read(d), KEEP_VARS, notes, "config.sql")
        open(d, "w", encoding="utf-8", newline="").write(text)
        check("config.sql", text, notes)
    else:
        names = args or sorted(d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d)))
        for name in names:
            sdir, ddir = os.path.join(src, name), os.path.join(dest, name)
            for root, _, files in os.walk(sdir):
                if "__pycache__" in root:
                    continue
                rel = os.path.relpath(root, sdir)
                for f in files:
                    key = "/".join(p for p in (name, rel.replace(os.sep, "/"), f) if p != ".")
                    s, d = os.path.join(root, f), os.path.join(ddir, rel, f)
                    if key in SKIP_FILES or (key in KEEP_FILES and os.path.exists(d)):
                        continue
                    os.makedirs(os.path.dirname(d), exist_ok=True)
                    if f.endswith(".sql") or f.lower() == "readme.md":
                        text = read(s)
                        if f == "variables.sql":
                            text = port_sql(port_variables(text, set()))
                            if os.path.exists(d):
                                old = read(d)
                                text = merge_sets(text, old, race_vars(old), notes, key)
                        elif f.endswith(".sql"):
                            text = port_sql(text)
                        else:
                            text = port_readme(text, name)
                        open(d, "w", encoding="utf-8", newline="").write(text)
                        if f.endswith(".sql"):
                            check(key, text, notes)
                    else:
                        shutil.copyfile(s, d)
    for n in notes:
        print("!", n)


def read(path):
    return open(path, encoding="utf-8", newline="").read()


if __name__ == "__main__":
    main()
