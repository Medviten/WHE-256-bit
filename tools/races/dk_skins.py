#!/usr/bin/env python3
"""Give every race that can be a Death Knight Death Knight skin colours, as the stock races have.

Stock DK skins are extra skin colours (Human: 12-14) whose CharSections rows carry flag 4 (Death Knight only): a skin
row, a face row per face style and an underwear row per colour. Most WHE races have none, so their Death Knights look
like anyone else of the race. For each race in CharBaseInfo with class 6 and no flag 4 skin rows, this takes
DK_COLOURS of the race's own skin colours (spread over its range), and adds a Death Knight colour after its highest
for each: the skin and face rows copied with flag 4 (and without 16, the barber shop flag, as stock DK skins have it)
and their textures made pale and ashen with tools/patch_eyes/dk_tint_blp.py (texture_2 too, except eye textures);
underwear and other colour-keyed rows copied with their textures as they are.

The rows are read from a built CharSections.dbc (a client's DBFilesClient with every race in), the textures from
WHE-common, the client's patch folders or its MPQs. Output:
- the tinted textures, next to their sources' paths with a _dk suffix, in WHE-common/patch-A.MPQ;
- dbc/[<modpak>]_charsections_dk.sql in the last modpak (in manifest order) that writes the race's charsections, so
  it runs after them, with the race's variable from its <Race>ClientString.
Stock races (1-11) are left alone: the Undead have no DK skins in stock either.

usage: dk_skins.py [--client DATA] [--common PATH] [--whe PATH] [--colours N] [--race CLIENTSTRING ...] [--apply-dbc]
Races that already have DK skin rows in the DBC are skipped, so it can be rerun after a build. --apply-dbc also appends
the rows to the client's CharSections.dbc (a copy is kept as CharSections.dbc.before-dk), to try them without a build."""
import argparse, collections, glob, os, re, shutil, struct, subprocess, sys

SLASH = chr(92)
HERE = os.path.dirname(os.path.abspath(__file__))
TINT = os.path.join(HERE, '..', 'patch_eyes', 'dk_tint_blp.py')
MPQ = os.path.join(HERE, '..', 'models', 'mpq_extract.py')
DK_COLOURS = 3
SKIN, FACE, FACIAL_HAIR, HAIR, UNDERWEAR = 0, 1, 2, 3, 4
TINTED_SECTIONS = {SKIN, FACE}
COLOUR_SECTIONS = {SKIN, FACE, UNDERWEAR}          # sections whose colour index is the skin colour
FLAG_DK, FLAG_BARBER = 4, 16
STOCK_RACES = set(range(1, 12))
CLASS_DK = 6
MPQS = ('patch-5.mpq', 'patch-4.MPQ', 'patch-3.mpq', 'patch-2.MPQ', 'patch.MPQ', 'lichking.MPQ', 'expansion.MPQ',
        'common-2.MPQ', 'common.MPQ')
SECTION_VARS = {SKIN: '@Skin', FACE: '@Face', FACIAL_HAIR: '@FacialHair', HAIR: '@Hair', UNDERWEAR: '@Underwear'}


def load_dbc(path):
    d = open(path, 'rb').read()
    _, n, fc, rs, ss = struct.unpack('<4s4I', d[:20])
    st = 20 + n * rs
    rows = [struct.unpack_from('<%dI' % fc, d, 20 + i * rs) for i in range(n)]
    def string(o):
        return d[st + o:d.index(b'\0', st + o)].decode('utf-8') if o < ss else ''
    return rows, string


_listing = {}


def listdir(path):
    if path not in _listing:
        _listing[path] = {e.lower(): e for e in os.listdir(path)} if os.path.isdir(path) else {}
    return _listing[path]


def resolve(rel, roots, client, cache_dir):
    """A local file for an archive path: WHE-common or the client's folders first, then its MPQs."""
    parts = rel.replace(SLASH, '/').split('/')
    for root in roots:
        cur = root
        for part in parts:
            match = listdir(cur).get(part.lower())
            if not match:
                cur = None
                break
            cur = os.path.join(cur, match)
        if cur and os.path.isfile(cur):
            return cur
    out = os.path.join(cache_dir, *[p.lower() for p in parts])
    if os.path.isfile(out):
        return out
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for name in MPQS:
        archive = next((os.path.join(client, e) for e in os.listdir(client) if e.lower() == name.lower()), None)
        if archive and subprocess.run([sys.executable, '-I', MPQ, archive, rel, out], capture_output=True).returncode == 0 \
                and os.path.isfile(out):
            return out
    return None


def dk_path(rel):
    stem, ext = os.path.splitext(rel)
    return stem + '_dk' + ext


def race_variables(whe):
    """ClientString -> (race variable, modpak) for every modpak's <Race>ClientString."""
    out = {}
    for path in glob.glob(os.path.join(whe, 'modpaks', '*', 'variables.sql')):
        for var, value in re.findall(r"SET\s+@(\w+)ClientString\s*=\s*'([^']*)'", open(path, encoding='utf-8').read()):
            out.setdefault(value, var)
    return out


def charsections_owner(whe, var):
    """The last modpak in manifest order whose charsections SQL writes the race."""
    order = []
    for line in open(os.path.join(whe, 'tools', 'scripts', 'build-dbc.manifest'), encoding='utf-8'):
        m = re.match(r'\s*#?\s*(F-\d+[^\s#]*)', line)
        if m:
            order.append(m.group(1))
    owner = None
    for modpak in order:
        for path in glob.glob(os.path.join(whe, 'modpaks', modpak, 'dbc', '*charsections*.sql')):
            if path.endswith('_dk.sql'):
                continue
            if re.search(r'@%s\b' % re.escape(var), open(path, encoding='utf-8').read()):
                owner = modpak
    return owner


def append_rows(path, rows):
    if not os.path.exists(path + '.before-dk'):
        shutil.copy2(path, path + '.before-dk')
    d = open(path, 'rb').read()
    magic, n, fields, size, string_size = struct.unpack('<4s4I', d[:20])
    records = bytearray(d[20:20 + n * size])
    strings = bytearray(d[20 + n * size:20 + n * size + string_size])
    offsets = {}

    def string(text):
        if not text:
            return 0
        if text not in offsets:
            offsets[text] = len(strings)
            strings.extend(text.encode('utf-8') + bytes(1))
        return offsets[text]
    next_id = max(struct.unpack_from('<I', records, i * size)[0] for i in range(n)) + 1
    for race, sex, section, textures, flags, type_, colour in rows:
        records += struct.pack('<10I', next_id, race, sex, section, *[string(t) for t in textures], flags, type_, colour)
        next_id += 1
    open(path, 'wb').write(struct.pack('<4s4I', magic, n + len(rows), fields, size, len(strings)) + records + strings)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', default='C:/Users/Medviten/Desktop/WowSquished-256-bit/Data')
    ap.add_argument('--common', default='D:/GitHub/WHE-common/patch-A.MPQ')
    ap.add_argument('--whe', default=os.path.join(HERE, '..', '..'))
    ap.add_argument('--cache', default='D:/wow-scratch/dk-skins-sources')
    ap.add_argument('--colours', type=int, default=DK_COLOURS)
    ap.add_argument('--race', nargs='*', help='only these races (ClientString)')
    ap.add_argument('--apply-dbc', action='store_true', help="also append the rows to the client's CharSections.dbc")
    a = ap.parse_args()
    dbc = os.path.join(a.client, 'patch-A.MPQ', 'DBFilesClient')
    races, rstr = load_dbc(os.path.join(dbc, 'ChrRaces.dbc'))
    sections, sstr = load_dbc(os.path.join(dbc, 'CharSections.dbc'))
    base = open(os.path.join(dbc, 'CharBaseInfo.dbc'), 'rb').read()
    dk_races = {base[20 + 2 * i] for i in range(struct.unpack_from('<I', base, 4)[0]) if base[21 + 2 * i] == CLASS_DK}
    client_string = {r[0]: rstr(r[11]) for r in races}
    variables = race_variables(a.whe)
    roots = [a.common] + [os.path.join(a.client, p) for p in ('patch-C.MPQ', 'patch-B.MPQ', 'patch-A.MPQ')]

    by_race = collections.defaultdict(list)
    for r in sections:
        by_race[r[1]].append(r)
    tinted = {}
    summary = []
    dbc_rows = []
    for race in sorted(dk_races - STOCK_RACES):
        name = client_string.get(race, '')
        if a.race and name not in a.race:
            continue
        rows = by_race[race]
        if any(r[3] == SKIN and r[7] & FLAG_DK for r in rows):
            continue
        var = variables.get(name)
        owner = var and charsections_owner(a.whe, var)
        if not owner:
            summary.append('%3d %-18s skipped: no modpak writes its charsections' % (race, name))
            continue
        out_rows, missing = [], set()
        for sex in (0, 1):
            skins = sorted({r[9] for r in rows if r[2] == sex and r[3] == SKIN and not r[7] & FLAG_DK})
            if not skins:
                continue
            picks = [skins[round(i * (len(skins) - 1) / max(1, a.colours - 1))] for i in range(min(a.colours, len(skins)))]
            picks = list(dict.fromkeys(picks))
            first_new = max(r[9] for r in rows if r[2] == sex and r[3] in COLOUR_SECTIONS) + 1
            for k, colour in enumerate(picks):
                new = first_new + k
                for r in rows:
                    if r[2] != sex or r[3] not in COLOUR_SECTIONS or r[9] != colour or r[7] & FLAG_DK:
                        continue
                    textures = [sstr(x) for x in r[4:7]]
                    if r[3] in TINTED_SECTIONS:
                        for j, rel in enumerate(textures):
                            if not rel or (j and 'eye' in rel.lower()):
                                continue
                            if rel not in tinted:
                                src = resolve(rel, roots, a.client, a.cache)
                                if not src:
                                    missing.add(rel)
                                    tinted[rel] = None
                                else:
                                    dst = os.path.join(a.common, *dk_path(rel).split(SLASH))
                                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                                    if not os.path.exists(dst) and subprocess.run(
                                            [sys.executable, '-I', TINT, src, dst], capture_output=True).returncode:
                                        missing.add(rel)
                                        tinted[rel] = None
                                    else:
                                        tinted[rel] = dk_path(rel)
                            textures[j] = tinted[rel] or rel
                    flags = (r[7] & ~FLAG_BARBER) | FLAG_DK
                    out_rows.append((sex, r[3], textures, flags, r[8], new))
        if not out_rows:
            continue
        dbc_rows += [(race,) + row for row in out_rows]
        sql = os.path.join(a.whe, 'modpaks', owner, 'dbc', '[%s]_charsections_dk.sql' % owner.split('_')[0])
        lines = ["(@CharSectionsID := @CharSectionsID +1, @%s, %-8s %-12s %s, %s, %s, %d, %d, %d)" % (
            var, ('@Male', '@Female')[sex] + ',', SECTION_VARS[sec] + ',',
            *["'%s'" % t.replace(SLASH, SLASH * 2) for t in tex], flags, type_, colour)
            for sex, sec, tex, flags, type_, colour in out_rows]
        with open(sql, 'w', encoding='utf-8', newline='\n') as f:
            f.write('-- charsections: %d inserts, 0 updates, 0 deletes\n' % len(lines))
            f.write('-- Death Knight skin colours (flag 4): %d per gender, made from the race\'s own skin colours with\n'
                    '-- tools/patch_eyes/dk_tint_blp.py. Generated by tools/races/dk_skins.py; textures in WHE-common.\n\n'
                    % len(picks))
            f.write('-- New entries\nSET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);\n')
            f.write('INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, '
                    '`texture_3`, `flags`, `type`, `color_index`) VALUES\n')
            f.write(',\n'.join(lines) + ';\n')
        summary.append('%3d %-18s %-34s %4d rows%s' % (race, name, owner, len(lines),
                                                         ', missing textures: %d' % len(missing) if missing else ''))
    if a.apply_dbc and dbc_rows:
        append_rows(os.path.join(dbc, 'CharSections.dbc'), dbc_rows)
        summary.append('%d rows appended to CharSections.dbc' % len(dbc_rows))
    print('\n'.join(summary))
    print('textures tinted:', sum(1 for v in tinted.values() if v), 'missing:', sum(1 for v in tinted.values() if not v))


if __name__ == '__main__':
    main()
