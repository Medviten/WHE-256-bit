#!/usr/bin/env python3
"""Add the Alpha-Worgen package (Character, DBFilesClient) to WHE: two appearance modpaks and two new races.

- F-094 Alpha Worgen, F-095 Alpha Goblin: new looks for the existing races, like F-037 for Mag'har. New model ids, so
  NPCs on the old models keep them; the race's customization rows are replaced.
- F-096 Cultist, F-097 Man'ari: full race modpaks made with new_race_modpaks.py's templates. Stock human and draenei
  models; the skins are the extra colours the package added to those races (human 10, draenei male 14-17, female 12-15).

The package overwrites stock and F-023/F-024 paths, so its files are copied to folders of their own and every path is
rewritten. Its M2s keep all sequences inline, so the .anim files aren't copied, and only the .skin files the header
counts are. Its Creature folder is left out: those files are already in WHE-common, byte for byte.

Fixes made to the package's rows:
- Worgen female: faces 22 and 24 are numbered 14 and 16 (and 24 points at face 16's textures), which hid both
- Worgen female: the Death Knight colours' faces 9 and 13 have no textures: they use face 7's
- Worgen male: facial hair style 0 is listed twice, and CharSections has a style 11 no geosets exist for
- Goblin female: hair styles start at 1, renumbered from 0
- Draenei: only the first colour has underwear textures; the others use the same ones instead of none

usage: alpha_race_modpaks.py <package folder> <stock DBFilesClient> <WHE-common patch-A.MPQ> [modpaks dir] [output dir]
Rerun it to regenerate; it overwrites the modpaks and the copied assets. Run racemask/word2.py afterwards: Cultist and
Man'ari are above race 64, so without their second mask word their racial skill rows would have a race mask of 0 (all
races)."""
import os
import re
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import new_race_modpaks as nrm   # noqa: E402

BS = chr(92)
SECTIONS = {0: '@Skin', 1: '@Face', 2: '@FacialHair', 3: '@Hair', 4: '@Underwear'}
GENDERS = ('@Male', '@Female')
# Package folder under Character -> folder in WHE-common
FOLDERS = {'worgen': 'AlphaWorgen', 'goblin': 'AlphaGoblin', 'human': 'Cultist', 'draenei': 'Manari'}
BARBER_LANGS = ('enus', 'kokr', 'frfr', 'dede', 'zhcn', 'zhtw', 'eses', 'esmx', 'ruru', 'jajp', 'ptpt', 'itit', 'unused_1',
                'unused_2', 'unused_3', 'unused_4')
# Rows the appearance modpaks replace, and what they call the race
APPEARANCE = [
    (94, 'alpha-worgen-assets', 'AlphaWorgen', 'Worgen', 12, 'worgen', 'Alpha Worgen', 'F-024_mod-playable-worgen',
     ['- MountSelf animations for Running Wild (F-063) are retargeted from F-024's models by `tools/models/m2_retarget_mountself.py`; hair and ear bones without a match stay in their Stand pose',
      '- Without F-063, Running Wild uses F-024's quadrupedal models, and the druid forms keep their own models: neither follows the alpha look',
      '- Its hair colours are matched to the druid forms by number, as in F-024']),
    (95, 'alpha-goblin-assets', 'AlphaGoblin', 'Goblin', 9, 'goblin', 'Alpha Goblin', 'F-023_mod-playable-goblin', []),
]
MODELS = {'worgen': ('Worgen', 'WorgenMale', 'WorgenFemale'), 'goblin': ('Goblin', 'goblinmale', 'goblinfemale')}

PACKAGE = STOCK = COMMON = MODPAKS = OUTPUT = None
FILES = {}        # lower case package path -> real path
COPIES = {}       # real path -> destination below patch-A.MPQ


def index_package():
    for root, _, names in os.walk(os.path.join(PACKAGE, 'Character')):
        for name in names:
            path = os.path.join(root, name)
            FILES[os.path.relpath(path, PACKAGE).replace(os.sep, BS).lower()] = path


def sections(dbc_dir):
    rows, strings, _ = nrm.load_dbc(os.path.join(dbc_dir, 'CharSections.dbc'))
    out = []
    for r in rows:
        v = struct.unpack_from('<10I', r)
        out.append(dict(race=v[1], gender=v[2], section=v[3], tex=[nrm.string(strings, o) for o in v[4:7]], flags=v[7], var=v[8], colour=v[9]))
    return out


def hair_rows(dbc_dir, race):
    rows, _, _ = nrm.load_dbc(os.path.join(dbc_dir, 'CharHairGeosets.dbc'))
    return sorted(tuple(struct.unpack_from('<6i', r)[2:]) for r in rows if struct.unpack_from('<I', r, 4)[0] == race)


def facial_rows(dbc_dir, race):
    """Gender, variation, 5 geosets. A variation listed twice keeps its row with geosets."""
    rows, _, f = nrm.load_dbc(os.path.join(dbc_dir, 'CharacterFacialHairStyles.dbc'))
    best = {}
    for r in rows:
        v = struct.unpack_from('<%di' % f, r)
        if v[0] != race:
            continue
        row = (v[1], v[2]) + tuple(g if g != -858993460 else 0 for g in v[3:8])
        if (v[1], v[2]) not in best or any(row[2:]):
            best[(v[1], v[2])] = row
    return sorted(best.values())


def moved(path):
    """A package texture's path in its new folder, queued for copying. Stock textures (not in the package) stay."""
    if not path or path.lower() not in FILES:
        return path
    real = FILES[path.lower()]
    parts = path.split(BS)
    folder = FOLDERS[parts[1].lower()]
    new = BS.join(['Character', folder] + [p.capitalize() for p in parts[2:-1]] + [os.path.basename(real)])
    COPIES[real] = new
    return new


def fix_worgen(rows):
    faces = [r for r in rows if r['section'] == 1 and r['gender'] == 1]
    for r in faces:
        number = int(re.search(r'FaceLower(\d\d)_', r['tex'][0], re.I).group(1))
        if r['colour'] <= 8 and number == 22:
            r['var'] = 22
    seen = set()
    for r in sorted(faces, key=lambda r: r['tex'][0].lower()):
        if r['colour'] <= 8 and r['var'] == 16:   # the second row of 16 is really face 24
            if r['colour'] in seen:
                r['var'] = 24
                r['tex'] = [t.replace('FaceLower16_', 'FaceLower24_').replace('FaceUpper16_', 'FaceUpper24_') for t in r['tex']]
            seen.add(r['colour'])
    for r in faces:
        if r['colour'] >= 9 and r['var'] in (9, 13):
            for i, t in enumerate(r['tex']):
                if t and t.lower() not in FILES:
                    r['tex'][i] = re.sub(r'(Face(?:Lower|Upper))\d\d_', r'\g<1>07_', t, flags=re.I)
    return rows


def checked(rows):
    missing = sorted({t for r in rows for t in r['tex'] if t and t.lower() not in FILES})
    if missing:
        raise SystemExit('rows point at textures the package lacks: %s' % missing[:10])
    return rows


def appearance_rows(all_rows, race, slug):
    rows = [dict(r, tex=list(r['tex'])) for r in all_rows if r['race'] == race]
    hair = hair_rows(os.path.join(PACKAGE, 'DBFilesClient'), race)
    facial = facial_rows(os.path.join(PACKAGE, 'DBFilesClient'), race)
    if slug == 'worgen':
        rows = fix_worgen(rows)
    if slug == 'goblin':
        for r in rows:
            if r['gender'] == 1 and r['section'] == 3:
                r['var'] -= 1
        hair = [(g, v - 1 if g == 1 else v, geoset, scalp) for g, v, geoset, scalp in hair]
    styles = {(row[0], row[1]) for row in facial}
    rows = [r for r in rows if r['section'] != 2 or (r['gender'], r['var']) in styles]
    return checked(rows), hair, facial


def race_rows(all_rows, race, colours):
    """The package's extra colours of a stock race, from 0, with the race's own hair and facial hair rows."""
    rows = []
    for gender, picked in colours.items():
        first = {}
        for r in all_rows:
            if r['race'] != race or r['gender'] != gender:
                continue
            if r['section'] in (2, 3):
                rows.append(dict(r, tex=list(r['tex'])))
            elif r['colour'] in picked:
                row = dict(r, tex=list(r['tex']), colour=picked.index(r['colour']))
                if r['section'] == 4:
                    if any(row['tex']):
                        first[gender] = row['tex']
                rows.append(row)
        for r in rows:
            if r['gender'] == gender and r['section'] == 4 and not any(r['tex']):
                r['tex'] = list(first[gender])
    checked([r for r in rows if r['section'] not in (2, 3)])   # hair and facial hair are the stock race's files
    return rows


def package_source(rows, race):
    """new_race_modpaks' customization source for a race made from these rows."""
    stock = os.path.join(PACKAGE, 'DBFilesClient')
    sect = [(r['gender'], r['section'], r['var'], r['colour'], [moved(t) for t in r['tex']]) for r in rows]
    flags = {(r['gender'], r['section'], r['var'], r['colour']): r['flags'] for r in rows}
    return ('package', race, sorted(sect), hair_rows(stock, race), facial_rows(stock, race), flags)


def write_sql(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text.rstrip('\n') + '\n')


def barbershop(key, hair, facial):
    cols = ', '.join(['`id`', '`type`'] + ['`display_name_%s`' % l for l in BARBER_LANGS] + ['`display_name_flags`']
                     + ['`description_%s`' % l for l in BARBER_LANGS]
                     + ['`description_flags`', '`cost_modifier`', '`race`', '`gender`', '`data`'])
    lines = []
    for gender, g in enumerate(GENDERS):
        for t, label, variations in ((0, 'Style', sorted({h[1] for h in hair if h[0] == gender})),
                                     (2, 'Facial Style', sorted({f[1] for f in facial if f[0] == gender}))):
            for v in variations:
                lines.append("(@BarbershopStyleID := @BarbershopStyleID +1, %d, '%s %d', %s, 16712190, %s, 16712172, '%s', @%s, %s, %d)" % (
                    t, label, v + 1, ', '.join(["''"] * 15), ', '.join(["''"] * 16), '1.0000000000000000' if t == 0 else '0.7500000000000000', key, g, v))
    return ("-- barbershopstyle: %d inserts, 0 updates, 0 deletes\n-- Replaces the race's styles (the alpha model has other hair and facial hair); generic names\n\n-- New entries\n"
            "DELETE FROM `barbershopstyle` WHERE `race` = @%s;\nSET @BarbershopStyleID = (SELECT COALESCE(MAX(id), 0) FROM `barbershopstyle`);\n"
            "INSERT INTO `barbershopstyle` (%s) VALUES\n%s;" % (len(lines), key, cols, ',\n'.join(lines)))


def write_appearance(all_rows, fnum, slug, var, key, race, folder_key, title, requires, notes):
    rows, hair, facial = appearance_rows(all_rows, race, folder_key)
    out = os.path.join(OUTPUT, 'F-0%d_%s' % (fnum, slug))
    tag = '[F-0%d]' % fnum
    folder = FOLDERS[folder_key]
    source, male, female = MODELS[folder_key]
    copy_model(source, 'Male', male, folder)
    copy_model(source, 'Female', female, folder)
    write_sql(os.path.join(out, 'variables.sql'),
              "-- %s models: new model IDs, so NPCs on the %s models keep them\n"
              "SET @%sMaleModel           = @NextModelID := @NextModelID +1;\n"
              "SET @%sFemaleModel         = @NextModelID := @NextModelID +1;\n"
              "SET @%sMaleModelPath       = 'Character\\\\%s\\\\Male\\\\%sMale.mdx';\n"
              "SET @%sFemaleModelPath     = 'Character\\\\%s\\\\Female\\\\%sFemale.mdx';"
              % (title, key, var, var, var, folder, folder, var, folder, folder))

    lines = []
    for r in sorted(rows, key=lambda r: (r['gender'], r['section'], r['colour'], r['var'])):
        lines.append("(@CharSectionsID := @CharSectionsID +1, @%s, %s, %s, %s, %s, %s, %d, %d, %d)" % (
            key, GENDERS[r['gender']], SECTIONS[r['section']], *[nrm.sql_str(moved(t)) for t in r['tex']], r['flags'], r['var'], r['colour']))
    write_sql(os.path.join(out, 'dbc', tag + '_charsections.sql'),
              "-- charsections: %d inserts, 0 updates, 0 deletes\n-- %s textures; replaces every row of the race\n\n"
              "DELETE FROM `charsections` WHERE `race` = @%s;\nSET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);\n"
              "INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES\n%s;"
              % (len(lines), title, key, ',\n'.join(lines)))

    lines = ["(@CharHairGeosetsID := @CharHairGeosetsID +1, @%s, %s, %d, %d, %d)" % (key, GENDERS[g], v, geoset, scalp) for g, v, geoset, scalp in hair]
    write_sql(os.path.join(out, 'dbc', tag + '_charhairgeosets.sql'),
              "-- charhairgeosets: %d inserts, 0 updates, 0 deletes\n-- The %s model's hair geosets\n\n"
              "DELETE FROM `charhairgeosets` WHERE `race` = @%s;\nSET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);\n"
              "INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES\n%s;"
              % (len(lines), title, key, ',\n'.join(lines)))

    lines = ["(@%s, %s, %d, %s)" % (key, GENDERS[row[0]], row[1], ', '.join(str(x) for x in row[2:7])) for row in facial]
    write_sql(os.path.join(out, 'dbc', tag + '_characterfacialhairstyles.sql'),
              "-- characterfacialhairstyles: %d inserts, 0 updates, 0 deletes\n-- The %s model's facial geosets\n\n"
              "DELETE FROM `characterfacialhairstyles` WHERE `race` = @%s;\n"
              "INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES\n%s;"
              % (len(lines), title, key, ',\n'.join(lines)))

    write_sql(os.path.join(out, 'dbc', tag + '_barbershopstyle.sql'), barbershop(key, hair, facial))

    columns = ['flags', 'size_class', 'model_scale', 'blood_id', 'footprint_texture_id', 'footprint_texture_length', 'footprint_texture_width',
               'footprint_particle_scale', 'foley_material_id', 'footstep_shake_size', 'death_thud_shake_size', 'sound_data', 'collision_width',
               'collision_height', 'mount_height', 'geo_box_min_x', 'geo_box_min_y', 'geo_box_min_z', 'geo_box_max_x', 'geo_box_max_y', 'geo_box_max_z',
               'world_effect_scale', 'attached_effect_scale', 'missile_collision_radius', 'missile_collision_push', 'missile_collision_raise']
    names = ', '.join('`%s`' % c for c in columns)
    write_sql(os.path.join(out, 'dbc', tag + '_creaturemodeldata.sql'),
              "-- creaturemodeldata: 2 inserts, 0 updates, 0 deletes\n-- Copies of the %s models with the %s paths\n\n"
              "DELETE FROM `creaturemodeldata` WHERE `id` IN (@{v}MaleModel, @{v}FemaleModel);\n".format(v=var) % (key, title) +
              "INSERT INTO `creaturemodeldata` (`id`, `model_path`, {n})\n"
              "SELECT @{v}MaleModel, @{v}MaleModelPath, {n} FROM `creaturemodeldata` WHERE `id` = @{k}MaleModel\nUNION ALL\n"
              "SELECT @{v}FemaleModel, @{v}FemaleModelPath, {n} FROM `creaturemodeldata` WHERE `id` = @{k}FemaleModel;".format(n=names, v=var, k=key))
    write_sql(os.path.join(out, 'dbc', tag + '_creaturedisplayinfo.sql'),
              "-- creaturedisplayinfo: 0 inserts, 2 updates, 0 deletes\n\n-- Changed values\n"
              "UPDATE `creaturedisplayinfo` SET `model_id` = @{v}MaleModel   WHERE `id` = @{k}MaleDisplay;\n"
              "UPDATE `creaturedisplayinfo` SET `model_id` = @{v}FemaleModel WHERE `id` = @{k}FemaleDisplay;".format(v=var, k=key))

    readme = ['# mod-worgoblin-high-elf', '## F-0%d_%s' % (fnum, slug), '', 'Optional update for %s. List it after that modpak in the manifest.' % requires, '',
              '### Features', '- The %s look for %s players: model, skin colours, faces, hair and facial hair' % (title, key),
              '- NPCs keep the models they had: only the player displays change', '', '### Known Issues',
              '- Tentative: not tested in game yet', '- Barber shop styles have generic names'] + notes + [
              '', '### Assets', 'In WHE-common, `patch-A.MPQ/Character/%s`. Made with `tools/races/alpha_race_modpaks.py`, see its notes for the row fixes' % folder]
    write_sql(os.path.join(out, 'readme.md'), '\n'.join(readme))


def copy_model(source, gender, name, folder):
    """The M2 and the skin profiles its header counts, renamed to <folder><Gender>; the client finds them by file name."""
    src = FILES[BS.join(('character', source, gender, name + '.m2')).lower()]
    new = folder + gender
    COPIES[src] = BS.join(('Character', folder, gender, new + '.m2'))
    views = struct.unpack_from('<I', open(src, 'rb').read(0x48), 0x44)[0]
    for i in range(views):
        skin = os.path.splitext(src)[0] + '%02d.skin' % i
        COPIES[skin] = BS.join(('Character', folder, gender, '%s%02d.skin' % (new, i)))


def copy_assets():
    for src, dest in sorted(COPIES.items()):
        path = os.path.join(COMMON, *dest.split(BS))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.copyfile(src, path)
    print('copied', len(COPIES), 'files')
    # Running Wild plays the model's own MountSelf anims (F-063), which the alpha models don't have
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))
    import m2_retarget_mountself
    character = os.path.join(COMMON, 'Character')
    for lower, gender in (('male', 'Male'), ('female', 'Female')):
        m2_retarget_mountself.retarget(os.path.join(character, 'Worgen', lower, 'worgen%s.m2' % lower),
                                       os.path.join(character, 'AlphaWorgen', gender, 'AlphaWorgen%s.m2' % gender))


def race_readme(out, key, name, plural, fnum, slug, side, home, kin, male_only, model, source, prefix):
    colours = 'one skin colour' if key == 'Cultist' else 'four skin colours'
    model_name = 'human' if key == 'Cultist' else 'draenei'
    lines = ['# mod-worgoblin-high-elf', '## F-0%d_mod-playable-%s' % (fnum, slug), '', '### Features',
             '- Playable %s (%s), race ID set in config.sql' % (DISPLAY[key][1], side),
             '    - Stock %s model, with %s from the Alpha-Worgen package; stock %s hair and facial hair' % (model_name, colours, model_name),
             '    - Home: %s (classes, start position, start outfits, action bars, stats, totems, druid forms, race-restricted' % home,
             '      quests and items)', '    - Kin: %s (voice, emotes and names, copied at build time)' % kin,
             "    - Helmet prefix '%s'" % prefix, '- Generated by `tools/races/alpha_race_modpaks.py` (tentative, for testing)', '',
             '### Requirements', '- Interface: a race button and the %s entries in `CharacterCreate.lua`, `GlueParent.lua` and `GlueStrings.lua`' % key.upper(), '',
             '### Known Issues', '- Tentative: not tested in game yet', '- No racial abilities yet', '- No racial mount',
             '- Placeholder race icon, racial faction name and description', '- Barber shop styles have generic names',
             '- Race ID above 64: `HelmetGeosetVisData` has no rows for it, so hair is not hidden under helmets']
    if key == 'Manari':
        lines.append('- Only the first skin colour has its own underwear textures; the others share them')
    nrm.write(os.path.join(out, 'readme.md'), '\n'.join(lines))


# key: (name for SQL strings, plural for readmes). new_race_modpaks can't take an apostrophe in a name
DISPLAY = {'Cultist': ('Cultist', 'Cultists'), 'Manari': ("Man\\'ari", "Man'ari")}


def fix_generated(key, fnum, slug, home, kin):
    out = os.path.join(OUTPUT, 'F-0%d_mod-playable-%s' % (fnum, slug))
    # The template's CoA racial (Slime Giant's Gooey Slam) isn't for these races, which have no racials yet
    for table in ('spell', 'skilllineability'):
        os.remove(os.path.join(out, 'dbc', '[BASE,F-0%d]_%s.sql' % (fnum, table)))
    # Home and Kin: the template's own rows aren't turned into variables by from_template
    nrm.write(os.path.join(out, 'sql', 'db-world', 'base', '[BASE,F-0%d]_player_race_template.sql' % fnum),
              "/* The stock races this race copies, see F-091_race-setup */\n"
              "DELETE FROM `player_race_template` WHERE `race` = @%s;\n"
              "INSERT INTO `player_race_template` (`race`, `home_race`, `kin_race`, `shapeshift_skin_color`) VALUES\n"
              "(@%s, @%s, @%s, 0);" % (key, key, home, kin))
    if key == 'Manari':
        path = os.path.join(out, 'variables.sql')
        text = open(path, encoding='utf-8').read()
        text = re.sub(r"^(SET @Manari\w*enUS\s*= )(.*)$", lambda m: m.group(1) + m.group(2).replace('Manari', DISPLAY[key][0]), text, flags=re.M)
        nrm.write(path, text)


def main():
    global PACKAGE, STOCK, COMMON, MODPAKS, OUTPUT
    PACKAGE, STOCK, COMMON = sys.argv[1:4]
    MODPAKS = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'modpaks')
    OUTPUT = sys.argv[5] if len(sys.argv) > 5 else MODPAKS
    index_package()
    rows = sections(os.path.join(PACKAGE, 'DBFilesClient'))
    for fnum, slug, var, key, race, folder_key, title, requires, notes in APPEARANCE:
        write_appearance(rows, fnum, slug, var, key, race, folder_key, title, requires, notes)

    cultist = race_rows(rows, 1, {0: [10], 1: [10]})
    manari = race_rows(rows, 11, {0: [14, 15, 16, 17], 1: [12, 13, 14, 15]})
    nrm.BUILT, nrm.DONOR, nrm.MODPAKS, nrm.OUTPUT = STOCK, STOCK, MODPAKS, OUTPUT
    nrm.write_readme = race_readme
    nrm.RACES = [
        ('Cultist', 'Cultist', 'Cultists', 96, 'cultist', 'Horde', 'Undead', 'Human', False, ('stock', 49, 50), package_source(cultist, 1), 'Hu',
         'Cult of the Forsaken', 'Living cultists who broke with the Lich King and now serve the Banshee Queen.', ''),
        ('Manari', 'Manari', 'Manari', 97, 'manari', 'Horde', 'BloodElf', 'Draenei', False, ('stock', 2248, 2250), package_source(manari, 11), 'Dr',
         'Fel Covenant', 'Demonic eredar who deserted the Burning Legion and found common cause with the blood elves.', ''),
    ]
    nrm.main()
    fix_generated('Cultist', 96, 'cultist', 'Undead', 'Human')
    fix_generated('Manari', 97, 'manari', 'BloodElf', 'Draenei')
    copy_assets()


if __name__ == '__main__':
    main()
