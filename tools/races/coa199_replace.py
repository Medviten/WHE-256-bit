#!/usr/bin/env python3
"""Replace the look of WHE races that Ilusixn's CoA 1.9.9 release does better, keeping everything else about them.

Only the files that make up a race's look change: charsections, charhairgeosets, characterfacialhairstyles,
barbershopstyle, creaturemodeldata, creaturedisplayinfo, creature_model_info, and the model paths and customization
labels in variables.sql. Race id, Home/Kin, racials, faction, outfits and helmet prefix stay. The modpak's DK skin file
is removed: it was made from the old textures (run tools/races/dk_skins.py again).

Client files come from coa199_race_prep.py's sources and overwrite same-named files in WHE-common. The old race's other
files stay there, unused.

- A skin or hair colour needing a texture nobody has is dropped and the remaining colours renumbered (Arakkoa: CoA's
  own recolours of retail's Outland arakkoa).
- Sequences whose .anim file nobody has are taken out of the model's lookup table, so the client falls back to another
  animation instead of asking for the file (the Arakkoa male's bow, wave, sit and sleep).

usage: coa199_replace.py <built DBFilesClient> <release server/dbc> <release client folder> <release Work folder>
                         <client Data folder> <CoA-based client Data folder> <scratch folder> [WHE-common patch-A.MPQ]"""
import os
import re
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'models'))
import coa199_race_modpaks as gen   # noqa: E402
import coa199_race_prep as prep   # noqa: E402
import coa199_races   # noqa: E402
import coa_race_prep   # noqa: E402
import coa_race_modpaks   # noqa: E402
import m2_anim_split   # noqa: E402
import new_race_modpaks as nrm   # noqa: E402

B = chr(92)
Race = coa199_races.Race
# key, name, plural, F number, folder slug, side, home, kin, CoA race, catalog (None: CharSections rows); the rest unused
REPLACED = [
    Race('Furbolg', 'Furbolg', 'Furbolgs', 45, 'furbolg', 'Alliance', 'NightElf', 'NightElf', 50, None, '', '', '', '', []),
    Race('Qiraji', 'Qiraji', 'Qiraji', 52, 'qiraji', 'Horde', 'Orc', 'Orc', 88, None, '', '', '', '', []),
    Race('Eredar', 'Eredar', 'Eredar', 53, 'eredar', 'Alliance', 'Draenei', 'Draenei', 55, None, '', '', '', '', []),
    Race('Arakkoa', 'Arakkoa', 'Arakkoa', 54, 'arakkoa', 'Alliance', 'Draenei', 'Draenei', 79, None, '', '', '', '', []),
    Race('Gnoll', 'Gnoll', 'Gnolls', 60, 'gnoll', 'Alliance', 'Human', 'Human', 83, 'Gnoll', '', '', '', '', []),
]
# creature models whose skins are CharSections rows filling texture type 11 (no catalog)
ROW_SKINS = {'Qiraji'}
CREDITS = {'Furbolg': 'Project Reforged', 'Qiraji': 'the AllRaces v12 pack (Furioz, Corruption, Eunoia, Kalibros)',
           'Eredar': 'Furioz, Corruption and the Eunoia team', 'Arakkoa': 'Yami', 'Gnoll': 'CoA Custom (Ilusixn)'}
FILES = [('dbc', t) for t in ('charsections', 'charhairgeosets', 'characterfacialhairstyles', 'barbershopstyle',
                              'creaturemodeldata', 'creaturedisplayinfo')] + \
        [(os.path.join('sql', 'db-world', 'base'), 'creature_model_info')]
BEGIN, END = '-- >>> CoA 1.9.9 replaced looks (tools/races/coa199_replace.py) >>>', '-- <<< CoA 1.9.9 replaced looks <<<'
SKIN_SECTIONS, HAIR_SECTIONS = (0, 1, 4), (2, 3)


class RowLook:
    """What coa199_race_prep needs of a catalog, from a race's CharSections skin rows."""
    def __init__(self, skins):
        self.skin_types, self.skins, self.fixed, self.keep, self.driven = [11], [(t,) for t in skins], {}, set(), set()


def row_looks(dbc, coa_id):
    rows, strings, _ = nrm.load_dbc(os.path.join(dbc, 'CharSections.dbc'))
    skins = {0: [], 1: []}
    for r in rows:
        v = struct.unpack_from('<10I', r)
        if v[1] == coa_id and v[3] == 0:
            skins[v[2]].append(nrm.string(strings, v[4]).strip())
    return {g: RowLook(s) for g, s in skins.items() if s}


def disable_missing_anims(path):
    """Point the sequence lookup entries of external sequences without a file at the stand animation, which never
    matches their id: the client then treats the animation as absent and uses its fallback."""
    data = bytearray(open(path, 'rb').read())
    table = m2_anim_split.sequences(data)
    gone = {s for s in range(len(table)) if not table[s][2] & m2_anim_split.HAS_DATA and
            not os.path.exists(path[:-3] + m2_anim_split.anim_name(table, '', s))}
    if not gone:
        return []
    stand = next(s for s in range(len(table)) if table[s][0] == 0)
    count, offset = struct.unpack_from('<II', data, 0x24)
    for i in range(count):
        if struct.unpack_from('<h', data, offset + 2 * i)[0] in gone:
            struct.pack_into('<h', data, offset + 2 * i, stand)
    open(path, 'wb').write(bytes(data))
    return sorted(table[s][0] for s in gone)


def overwrite(src, common):
    """Copy a tree over WHE-common, keeping the case of folders it already has."""
    copied = 0
    for dirpath, _, names in os.walk(src):
        rel = os.path.relpath(dirpath, src)
        cur = common
        for part in ([] if rel == '.' else rel.split(os.sep)):
            hit = next((e for e in os.listdir(cur) if e.lower() == part.lower()), None) if os.path.isdir(cur) else None
            cur = os.path.join(cur, hit or part)
        os.makedirs(cur, exist_ok=True)
        existing = {e.lower(): e for e in os.listdir(cur)}
        for n in names:
            shutil.copyfile(os.path.join(dirpath, n), os.path.join(cur, existing.get(n.lower(), n)))
            copied += 1
    return copied


def filtered(customization, has):
    """customization() without the colours whose textures nobody has, the remaining colours renumbered per gender."""
    def wrapped(source):
        sections, hair, facial = customization(source)
        if source[0] != 'coa':
            return sections, hair, facial
        kept, dropped = [], set()
        for keyed in (SKIN_SECTIONS, HAIR_SECTIONS):
            for g in {s[0] for s in sections}:
                rows = [s for s in sections if s[0] == g and s[1] in keyed]
                bad = {s[3] for s in rows if any(t and not has(t) for t in s[4])}
                if keyed is SKIN_SECTIONS and bad >= {s[3] for s in rows if s[1] == 0}:
                    bad = set()   # never drop every skin
                new = {c: i for i, c in enumerate(sorted({s[3] for s in rows} - bad))}
                dropped |= {(g, keyed[0], c) for c in bad}
                flags = dict(nrm.PLAYER_FLAGS)
                for s in rows:
                    if s[3] in new:
                        kept.append((s[0], s[1], s[2], new[s[3]], s[4]))
                        if (s[0], s[1], s[2], s[3]) in flags:
                            nrm.PLAYER_FLAGS[(s[0], s[1], s[2], new[s[3]])] = flags[(s[0], s[1], s[2], s[3])]
        if dropped:
            print('  source %s: dropped %d colours with missing textures' % (source[1], len(dropped)))
        return sorted(kept, key=lambda s: s[:4]), hair, facial
    return wrapped


def update_variables(path, scratch, key):
    text = open(path, encoding='utf-8').read()
    new = open(scratch, encoding='utf-8').read()
    for var in ('FacialHairCustomization1', 'FacialHairCustomization2', 'HairCustomization'):
        m = re.search(r'SET @%s%s\s*=[^;]*;' % (key, var), new)
        text = re.sub(r'SET @%s%s\s*=[^;]*;' % (key, var), lambda _: m.group(0), text)
    male, female = (re.search(r"SET @%s%sModelPath = '[^']*';" % (key, g), new).group(0) for g in ('Male', 'Female'))
    note = ' -- CoA 1.9.9 model (tools/races/coa199_replace.py)'
    text = re.sub(r"SET @%sFemaleModelPath\s*=[^\n]*\n" % key, '', text)
    text = re.sub(r"SET @%sMaleModelPath\s*=[^\n]*\n" % key, lambda _: male + note + '\n' + female + '\n', text)
    nrm.write(path, text)


def update_readme(path, race):
    text = open(path, encoding='utf-8').read()
    text = re.sub(r'\n    - WallCraft\'s playable [^\n]*', '\n    - Model, textures and customization from Ilusixn\'s CoA 1.9.9 release '
                  '(see Look)', text)
    if race.key in ROW_SKINS or race.catalog:
        req = ('- Custom client with `creatureSkinRaces` containing the race ID: the skin texture is composited whole and '
               'armour textures are not drawn on it')
        if req not in text:
            text = text.replace('### Requirements\n', '### Requirements\n' + req + '\n', 1)
    text = re.sub(r'\n    - Customization: [^\n]*(\n      [^\n]*)*', '\n    - Customization: CoA\'s (see Look)', text)
    text = re.sub(r', display scale [\d.]+', '', text)
    text = re.sub(r'\n- Converted Vanilla model[^\n]*', '', text)
    text = re.sub(r'\n- Male only[^\n]*', '', text)
    text = re.sub(r', male only\b', '', text)
    section = ('### Look\nModel, textures and customization from Ilusixn\'s CoA 1.9.9 release (CoA race %d), put in place by '
               '`tools/races/coa199_replace.py`. Author: %s; see `CREDITS.md` in the release, which must ship with these files.'
               '\n\n' % (race.coa_id, CREDITS[race.key]))
    text = re.sub(r'### Look\n.*?\n\n', '', text, flags=re.S)
    i = text.find('### Known Issues')
    text = text[:i] + section + text[i:] if i >= 0 else text.rstrip('\n') + '\n\n' + section
    nrm.write(path, text)


def main():
    args = sys.argv[1:]
    if len(args) < 7:
        sys.exit(__doc__)
    built, dbc, catalogs, work, data, extra, scratch = args[:7]
    common = args[7] if len(args) > 7 else os.path.join(HERE, '..', '..', '..', 'WHE-common', 'patch-A.MPQ')
    assets, output = os.path.join(scratch, 'assets'), os.path.join(scratch, 'modpaks')
    for d in (assets, output):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    cp = prep.Copier(work, data, assets, extra)
    for race in REPLACED:
        models = prep.race_models(dbc, race)
        if race.key in ROW_SKINS:
            prep.prepare_catalog(cp, row_looks(dbc, race.coa_id), race, models)
        elif race.catalog:
            prep.prepare_catalog(cp, catalogs, race, models)
        else:
            prep.prepare_classic(cp, dbc, race, models)
            for path in dict.fromkeys(models):
                m2 = os.path.join(assets, *path.split(B))
                if os.path.exists(m2):
                    gone = disable_missing_anims(m2)
                    if gone:
                        print('    %s: no file for animations %s' % (path, gone))
    print('assets: %d files, missing %s' % (cp.copied, sorted(set(cp.missing))[:40]))
    print('copied to WHE-common:', overwrite(assets, common))

    nrm.BUILT, nrm.DONOR = built, dbc
    nrm.MODPAKS = os.path.join(HERE, '..', '..', 'modpaks')
    nrm.OUTPUT = output
    races = []
    for r in REPLACED:   # Home as the modpak has it (it decides the model rows' sounds, blood and footprints)
        text = open(os.path.join(nrm.MODPAKS, nrm.folder_name(r.fnum, r.slug), 'variables.sql'), encoding='utf-8').read()
        home = re.search(r'SET @%sHome\s*=\s*@(\w+);' % r.key, text)
        races.append(r._replace(home=home.group(1)) if home else r)
    nrm.RACES = [gen.as_nrm(r, catalogs, dbc) for r in races]
    nrm.write_readme = lambda *a: None
    nrm.customization = filtered(gen.one_body_sections(nrm.customization), lambda t: cp.has(t) or cp.is_stock(t))
    nrm.main()
    model_rows = coa_race_modpaks.coa_model_rows(dbc)
    scales = gen.coa_display_scales(dbc)
    for race in REPLACED:
        name = nrm.folder_name(race.fnum, race.slug)
        src, dst = os.path.join(output, name), os.path.join(nrm.MODPAKS, name)
        gen.patch_files(src, race, model_rows, scales, dbc)
        tag = '[BASE,F-%03d]' % race.fnum
        for sub, table in FILES:
            shutil.copyfile(os.path.join(src, sub, '%s_%s.sql' % (tag, table)), os.path.join(dst, sub, '%s_%s.sql' % (tag, table)))
        update_variables(os.path.join(dst, 'variables.sql'), os.path.join(src, 'variables.sql'), race.key)
        update_readme(os.path.join(dst, 'readme.md'), race)
        dk = os.path.join(dst, 'dbc', '[F-%03d]_charsections_dk.sql' % race.fnum)
        if os.path.exists(dk):
            os.remove(dk)
    path = os.path.join(nrm.MODPAKS, 'config.sql')
    text = open(path, encoding='utf-8').read()
    body = '%s\n%s\n%s\n' % (BEGIN, ('SET @ArakkoaFemaleModel'.ljust(64) + '=   @NextModelID := @NextModelID +1; -- F-054 was male only'), END)
    pattern = re.compile(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n', re.S)
    if pattern.search(text):
        text = pattern.sub(lambda m: body, text)
    else:
        m = re.search(r'^-- <<< Retail totems <<<\n', text, re.M)
        text = text[:m.end()] + body + text[m.end():]
    nrm.write(path, text)


if __name__ == '__main__':
    main()
