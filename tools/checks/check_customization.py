#!/usr/bin/env python3
"""Check the character customization data of race modpaks for errors.

Reads each modpak's INSERT statements for charsections, charhairgeosets, characterfacialhairstyles,
charhairtextures and barbershopstyle (no database needed) and reports, per race and gender:

  - textures that exist neither in the client patch (data/patch-A.MPQ, case-insensitive like an MPQ) nor
    among the stock CharSections textures (when --stock-dbc points at the original client DBCs)
  - rows whose textures live in another race's folder (e.g. copy-paste leftovers)
  - duplicate rows (same gender, section, type and colour)
  - colour/type grids with gaps, faces or underwear that don't cover every skin colour, hair styles or facial
    hair styles with differing colour sets
  - CharHairGeosets / CharacterFacialHairStyles variations that don't line up with the CharSections hair and
    facial hair types or the barber shop styles, and hair/facial geosets the race's model doesn't have
  - missing CharHairTextures rows

Usage:
    python3 check_customization.py [--repo PATH] [--stock-dbc DIR] [MODPAK ...]

With no MODPAK arguments every modpak that inserts charsections rows is checked."""
import argparse, collections, os, re, struct, sys

SECTION_NAMES = {0: "skin", 1: "face", 2: "facial hair", 3: "hair", 4: "underwear"}
TABLES = ("charsections", "charhairgeosets", "characterfacialhairstyles", "charhairtextures", "barbershopstyle")


# --------------------------------------------------------------------------------------------- SQL parsing
def split_statements(text):
    i, n, start, state = 0, len(text), 0, None
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
                yield text[start:i + 1]
                start = i + 1
        i += 1


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


def top_level_split(s):
    parts, depth, state, last, i = [], 0, None, 0, 0
    while i < len(s):
        c = s[i]
        if state in ("'", '"'):
            if c == "\\":
                i += 2; continue
            if c == state:
                state = None
        elif c in "'\"":
            state = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[last:i]); last = i + 1
        i += 1
    parts.append(s[last:])
    return parts


INSERT_RE = re.compile(r"^\s*(?:INSERT|REPLACE)(?:\s+IGNORE)?\s+INTO\s+`(\w+)`\s*\((.*?)\)\s*VALUES\s*(.*?);?\s*$", re.S | re.I)
STRING_RE = re.compile(r"^'((?:[^'\\]|\\.)*)'$", re.S)


def unescape(s):
    return re.sub(r"\\(.)", r"\1", s)


class Vars:
    """Integer and string values of SET @x = ... in config.sql and every variables.sql (static, no evaluation)."""

    def __init__(self, modpaks):
        self.raw = {}
        files = [os.path.join(modpaks, "config.sql")] + sorted(
            os.path.join(modpaks, d, "variables.sql") for d in os.listdir(modpaks)
            if os.path.exists(os.path.join(modpaks, d, "variables.sql")))
        for f in files:
            for stmt in split_statements(open(f, encoding="utf-8").read()):
                m = re.match(r"\s*SET\s+@(\w+)\s*:?=\s*(.*?);\s*$", strip_comments(stmt), re.S | re.I)
                if m:
                    self.raw[m.group(1)] = m.group(2).strip()

    def value(self, token, depth=0):
        token = token.strip()
        m = STRING_RE.match(token)
        if m:
            return unescape(m.group(1))
        if re.fullmatch(r"-?\d+", token):
            return int(token)
        m = re.fullmatch(r"@(\w+)", token)
        if m and depth < 10 and m.group(1) in self.raw:
            v = self.value(self.raw[m.group(1)], depth + 1)
            return v if v is not None else token
        return token if token.startswith("@") else None


def read_rows(path, variables):
    """Yield (table, row dict) for every INSERT ... VALUES row of the customization tables in path."""
    text = open(path, encoding="utf-8").read()
    for stmt in split_statements(text):
        m = INSERT_RE.match(strip_comments(stmt))
        if not m or m.group(1).lower() not in TABLES:
            continue
        table = m.group(1).lower()
        cols = [c.strip().strip("`").lower() for c in m.group(2).split(",")]
        for tup in top_level_split(m.group(3)):
            tup = tup.strip()
            if not tup.startswith("(") or not tup.endswith(")"):
                continue
            vals = top_level_split(tup[1:-1])
            if len(vals) != len(cols):
                yield table, {"_error": f"{len(vals)} values for {len(cols)} columns: {tup[:80]}"}
                continue
            row = {}
            for c, v in zip(cols, vals):
                if c == "race" and v.strip().startswith("@"):
                    row[c] = v.strip()
                elif v.strip().startswith("@") and ":=" in v:
                    row[c] = None
                else:
                    row[c] = variables.value(v)
            yield table, row


# ------------------------------------------------------------------------------------------- client data
def index_patch(data_dir):
    files = set()
    for root, _, names in os.walk(data_dir):
        for n in names:
            files.add(os.path.relpath(os.path.join(root, n), data_dir).replace(os.sep, "\\").lower())
    return files


def stock_textures(dbc_dir):
    path = os.path.join(dbc_dir, "CharSections.dbc") if dbc_dir else None
    if not path or not os.path.exists(path):
        return set()
    d = open(path, "rb").read()
    _, n, _, size, _ = struct.unpack_from("<4s4I", d)
    strings = 20 + n * size
    out = set()
    for r in range(n):
        for k in range(3):
            o = struct.unpack_from("<I", d, 20 + r * size + 16 + 4 * k)[0]
            s = d[strings + o:d.index(b"\0", strings + o)].decode("latin-1")
            if s:
                out.add(s.lower())
    return out


def model_geosets(data_dir, model_path):
    """Geoset ids of a model's first skin profile, or None when the model isn't in the patch."""
    if not model_path:
        return None
    rel = re.sub(r"\.(mdx|mdl)$", ".m2", model_path, flags=re.I).replace("\\", os.sep)
    base = os.path.join(data_dir, os.path.splitext(rel)[0])
    skin = None
    folder = os.path.dirname(base)
    if os.path.isdir(folder):
        want = (os.path.basename(base) + "00.skin").lower()
        for f in os.listdir(folder):
            if f.lower() == want:
                skin = os.path.join(folder, f)
    if not skin:
        return None
    d = open(skin, "rb").read()
    if d[:4] != b"SKIN":
        return None
    n, o = struct.unpack_from("<II", d, 28)
    return {struct.unpack_from("<H", d, o + i * 48)[0] for i in range(n)}


# ---------------------------------------------------------------------------------------------- checks
def folder_of(path):
    """The race folder a texture belongs to: character/<race> or custom/<race>; empty for bare file names."""
    parts = path.lower().split("\\")
    if len(parts) < 2:
        return ""
    return "\\".join(parts[:2])


def ranges(values):
    v = sorted(values)
    return v == list(range(len(v)))


def check_race(race, gender, rows, hair_geo, facial, barber, hairtex, geosets, exists, report):
    g = "male" if gender == 0 else "female"
    out = []
    by_sec = collections.defaultdict(list)
    for r in rows:
        by_sec[r["base_section"]].append(r)
    # duplicates
    seen = collections.Counter((r["base_section"], r["type"], r["color_index"], r["flags"]) for r in rows)
    for (s, t, c, f), n in seen.items():
        if n > 1:
            out.append(f"{n} identical {SECTION_NAMES.get(s, s)} rows (type {t}, colour {c}, flags {f})")
    keyed = collections.Counter((r["base_section"], r["type"], r["color_index"]) for r in rows)
    for (s, t, c), n in keyed.items():
        if n > 1 and seen[(s, t, c, next(r["flags"] for r in rows if (r["base_section"], r["type"], r["color_index"]) == (s, t, c)))] == 1:
            out.append(f"{SECTION_NAMES.get(s, s)} type {t} colour {c} defined {n} times with different flags")

    def colours(sec, t=None, regular=False):
        return {r["color_index"] for r in by_sec.get(sec, [])
                if (t is None or r["type"] == t) and (not regular or (r["flags"] or 0) & 16)}

    # NPC-only skins (flag 8) have no faces or underwear in stock data, and DK skins (flag 4) don't always,
    # so faces and underwear only have to cover the regular player skins (flag 16).
    skins = colours(0, 0)
    player_skins = colours(0, 0, regular=True)
    if not skins:
        out.append("no skin rows")
    elif not ranges(skins):
        out.append(f"skin colours not contiguous: {sorted(skins)}")
    for sec in (1, 4):
        types = sorted({r["type"] for r in by_sec.get(sec, [])})
        if sec == 1 and not types:
            out.append("no face rows")
        if types and not ranges(types):
            out.append(f"{SECTION_NAMES[sec]} types not contiguous: {types}")
        for t in types:
            # DK-only types (every row has flag 4, e.g. Worgen's extra faces) only need the skins they are for
            dk_only = all((r["flags"] or 0) & 4 for r in by_sec[sec] if r["type"] == t)
            miss = set() if dk_only else player_skins - colours(sec, t)
            if miss:
                out.append(f"{SECTION_NAMES[sec]} type {t} missing skin colours {sorted(miss)}")
            extra = colours(sec, t) - skins
            if extra:
                out.append(f"{SECTION_NAMES[sec]} type {t} has colours with no skin: {sorted(extra)}")
    for sec in (2, 3):
        types = sorted({r["type"] for r in by_sec.get(sec, [])})
        if types and not ranges(types):
            out.append(f"{SECTION_NAMES[sec]} types not contiguous: {types}")
        sets = {t: frozenset(colours(sec, t, regular=True)) for t in types}
        if len(set(sets.values())) > 1:
            common = collections.Counter(sets.values()).most_common(1)[0][0]
            for t, s in sets.items():
                if s != common:
                    out.append(f"{SECTION_NAMES[sec]} type {t} player colours {sorted(s)} differ from the usual {sorted(common)}")
        allc = set().union(*sets.values()) if sets else set()
        if allc and not ranges(allc):
            out.append(f"{SECTION_NAMES[sec]} colours not contiguous: {sorted(allc)}")
    hair_types = {r["type"] for r in by_sec.get(3, [])}
    facial_types = {r["type"] for r in by_sec.get(2, [])}
    hair_colours = colours(3)
    if facial_types and hair_colours and colours(2) - hair_colours:
        out.append(f"facial hair colours {sorted(colours(2) - hair_colours)} have no matching hair colour")
    # geosets
    if hair_geo:
        var = {v for v, _ in hair_geo}
        if not ranges(var):
            out.append(f"CharHairGeosets variations not contiguous: {sorted(var)}")
        if hair_types and var != hair_types:
            out.append(f"hair styles: CharHairGeosets has {len(var)} ({min(var)}-{max(var)}), CharSections hair types {sorted(hair_types)}")
        if geosets is not None:
            missing = sorted({gs for _, gs in hair_geo if gs and gs not in geosets})
            if missing:
                out.append(f"hair geosets not in the model: {missing}")
    elif hair_types:
        out.append(f"no CharHairGeosets rows for {len(hair_types)} hair styles")
    if facial:
        var = {v for v, _ in facial}
        if not ranges(var):
            out.append(f"CharacterFacialHairStyles variations not contiguous: {sorted(var)}")
        if facial_types and var != facial_types:
            out.append(f"facial hair styles: CharacterFacialHairStyles has {len(var)}, CharSections facial hair types {sorted(facial_types)}")
        if geosets is not None:
            missing = set()
            for _, gs in facial:
                for value, group in zip(gs, (100, 300, 200)):
                    if value and group + value not in geosets:
                        missing.add(group + value)
            if missing:
                out.append(f"facial hair geosets not in the model: {sorted(missing)}")
    elif facial_types:
        out.append(f"no CharacterFacialHairStyles rows for {len(facial_types)} facial hair styles")
    if barber is not None:
        for btype, label, want in ((0, "hair", hair_types), (2, "facial hair", facial_types)):
            have = {d for t, d in barber if t == btype}
            if want and have and have != want:
                out.append(f"barber {label} styles {sorted(have)} don't match the {label} types {sorted(want)}")
    if hairtex is not None and not hairtex:
        out.append("no CharHairTextures row")
    # textures
    missing = collections.OrderedDict()
    for r in rows:
        for k in ("texture_1", "texture_2", "texture_3"):
            t = r.get(k)
            if isinstance(t, str) and t and not exists(t):
                missing.setdefault(t, f"{SECTION_NAMES.get(r['base_section'], r['base_section'])} type {r['type']} colour {r['color_index']}")
    for t, where in list(missing.items())[:12]:
        out.append(f"missing texture {t} ({where})")
    if len(missing) > 12:
        out.append(f"... and {len(missing) - 12} more missing textures")
    # foreign folders
    folders = collections.Counter(folder_of(t) for r in rows for k in ("texture_1", "texture_2", "texture_3")
                                  for t in [r.get(k)] if isinstance(t, str) and t)
    if folders:
        main = folders.most_common(1)[0][0]
        for f, n in folders.items():
            if f != main and f and n < folders[main]:
                ex = next(r for r in rows for k in ("texture_1", "texture_2", "texture_3")
                          if isinstance(r.get(k), str) and r.get(k) and folder_of(r[k]) == f)
                out.append(f"{n} texture(s) from {f}\\ (main folder {main}\\), e.g. "
                           f"{SECTION_NAMES.get(ex['base_section'], ex['base_section'])} type {ex['type']} colour {ex['color_index']}")
    for line in out:
        report.append(f"  {race} {g}: {compress(line)}")


def compress(line):
    """Shorten long integer lists like [0, 1, 2, ..., 223] to [0-223 (224 values)]."""
    def repl(m):
        nums = [int(x) for x in m.group(1).split(",")]
        if len(nums) <= 8:
            return m.group(0)
        runs, start = [], nums[0]
        for a, b in zip(nums, nums[1:] + [None]):
            if b != a + 1:
                runs.append(f"{start}" if start == a else f"{start}-{a}")
                start = b
        return "[" + ", ".join(runs) + f" ({len(nums)} values)]"
    return re.sub(r"\[(\s*-?\d+(?:\s*,\s*-?\d+)*)\]", repl, line)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    ap.add_argument("--stock-dbc", help="directory with the original client DBCs (for stock CharSections textures)")
    ap.add_argument("modpaks", nargs="*")
    a = ap.parse_args()
    modpaks_dir = os.path.join(a.repo, "modpaks")
    data_dir = os.path.join(a.repo, "data", "patch-A.MPQ")
    patch = index_patch(data_dir)
    stock = stock_textures(a.stock_dbc)
    exists = lambda t: t.lower() in patch or t.lower() in stock
    variables = Vars(modpaks_dir)
    names = a.modpaks or sorted(d for d in os.listdir(modpaks_dir) if os.path.isdir(os.path.join(modpaks_dir, d)))
    total = 0
    for name in names:
        root = os.path.join(modpaks_dir, name)
        data = collections.defaultdict(lambda: collections.defaultdict(list))
        errors = []
        for dirpath, _, files in os.walk(os.path.join(root, "dbc")):
            for f in sorted(files):
                if f.endswith(".sql"):
                    for table, row in read_rows(os.path.join(dirpath, f), variables):
                        if "_error" in row:
                            errors.append(f"  {f}: {row['_error']}")
                        else:
                            data[table][(str(row.get("race")), row.get("gender"))].append(row)
        if not data["charsections"]:
            continue
        report = list(errors)
        races = sorted({k[0] for k in data["charsections"]})
        for race in races:
            rname = race.lstrip("@")
            genders = sorted({k[1] for k in data["charsections"] if k[0] == race})
            for gender in genders:
                key = (race, gender)
                model = variables.value(f"@{rname}{'Male' if gender == 0 else 'Female'}ModelPath")
                geosets = model_geosets(data_dir, model) if isinstance(model, str) and not model.startswith("@") else None
                hair_geo = [(r["variation"], r["geoset"]) for r in data["charhairgeosets"].get(key, [])]
                facial = [(r["variation_id"], [r.get(f"geoset_{i}") or 0 for i in range(1, 6)])
                          for r in data["characterfacialhairstyles"].get(key, [])]
                barber = [(r["type"], r["data"]) for r in data["barbershopstyle"].get(key, [])] if data["barbershopstyle"] else None
                hairtex = data["charhairtextures"].get(key, []) if data["charhairtextures"] else None
                check_race(rname, gender, data["charsections"][key], hair_geo, facial, barber, hairtex, geosets, exists, report)
        if report:
            total += len(report)
            print(f"== {name}")
            print("\n".join(report))
    print(f"\n{total} issue(s)" + ("" if stock else "  (no --stock-dbc: stock textures count as missing)"))


if __name__ == "__main__":
    sys.exit(main())
