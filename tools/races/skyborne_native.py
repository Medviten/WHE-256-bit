#!/usr/bin/env python3
"""The native Skyborne of F-103/F-104: rows from Kalibro's races package (Kalibros_Races_<date>, its races 52/53) and its
files copied to WHE-common, for clients that don't draw the race from the Forever source.

The package's own rows are an "expanded" encoding for Kalibro's client (beards folded into male face indices, feathers in
facial styles), which a stock client can't turn into geosets. The rows written here use its textures with stock sliders:
- skin colour: 5 skins x 26 eye colours (index = eye * 5 + skin); the eye texture is the skin row's texture_2, which fills
  the models' type 8 eye slots. Faces and underwear have a row per skin colour, as the sliders need
- face: Forever's 10 faces
- hair style: Forever's styles, then each with its feathers in Forever's first feather colour; hair colour: its 32 colours
- facial style: male beard x eyebrows, female eyebrows
tools/models/skyborne_native_prep.py makes the feathers part of the hair styles and parks the other feather colours.
The Forever client only reads these rows at row 0, as with F-040 and F-098/F-099.

Files: the models become custom/skyborne/native/<sex>/skyborne<sex>.m2 (with their .skin and .anim files); the textures keep
the package's custom/skyborne paths, which the models name. Nothing lands on stock Blood Elf paths.

usage: skyborne_native.py <modpaks dir> [more modpaks dirs ...] [--package PATH] [--common PATH] [--no-files]
Rewrites the files, so it can be rerun."""
import argparse, glob, os, re, shutil, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kalibro_races   # noqa: E402
import new_race_modpaks as nrm   # noqa: E402

PACKAGE = r'D:\Downloads\Downloads\Races\Kalibros_Races_20261012'
COMMON = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'WHE-common', 'patch-A.MPQ')
BS = '\\'
SOURCE_RACE = 52                     # the package's Alliance Skyborne; 53 has the same rows
MODELS = {'male': '7478487', 'female': '7478494'}
SKINS, EYES, FACES, HAIR_COLOURS = 5, 26, 10, 32
OVERLAY = 'custom\\skyborne\\runtime\\transparent_lower.blp'
RACES = (('AllianceSkyborne', 103), ('HordeSkyborne', 104))
GAP = ", ''" * 15
# Forever's choice names (RetailRaceProbe --forever <ini> choices <option>), in its order, which is the package's variation order
HAIR = {'male': ['Flipped', 'Swept', 'Falcon', 'Foxtail', 'Parted Long', 'Spiked', 'Long Bangs', 'Feathered', 'Slicked', 'Headband',
                 'Topknot', 'Mane', 'Thick Braids', 'Tail', 'Windswept', 'Chonmage', 'Short', 'Circlet', 'Prince', 'Thin Braids', 'Bald',
                 'Wayward', 'Crested', 'Aerie', 'Noble'],
        'female': ['Ponytail', 'Parted Long', 'Soaked', 'Trouble', 'Circlet', 'Full', 'Tied', 'Bun', 'Parted Short', 'Simple', 'Shy',
                   'Raquel', 'Glamorous', 'Headband', 'Diva', 'Elaborate', 'Nape', 'Boar Tails', 'Bangs', 'Braided Tail', 'Slicked Back',
                   'Chonmage', 'Tiara', 'Pixie', 'Bald', 'Windswept', 'Swoop', 'Tailwind', 'Tress']}
BEARDS = ['Point', 'Soul Patch', 'Spike', 'Pointed', 'Cropped', 'Soul Strip', 'Dagger', 'Goatee', 'Styled', 'Beaded', 'Full', 'Chin Strap']
EYEBROWS = ['Piercing', 'Swept', 'Feathered', 'Winged']
FEATHERED = 50   # skyborne_native_prep.py: geoset of a hair style with its (Seafoam) feathers
SUMMARY = ('5 skin colours x 26 eye colours, 10 faces, 25 (male) / 29 (female) hair styles each with or without feathers, '
           '32 hair colours, and beard x eyebrows (male) / eyebrows (female) as facial styles')
LIMITS = ('one feather colour (Seafoam), Long ears, no horns, blindfolds, tattoos or jewelry, and only 26 of the 47 eye colours '
          "(Kalibro's bake); the 130 skin colours make that slider long")


def path(*parts):
    return "'%s'" % (BS * 2).join(parts)


def sql(name):
    return "'%s'" % name.replace(BS, BS * 2) if name else "''"


def package_rows(package):
    """(gender, section, type, colour) -> textures of the package's race-52 rows"""
    rows, strings, _ = nrm.load_dbc(os.path.join(package, 'DBFilesClient', 'CharSections.dbc'))
    out = {}
    for r in rows:
        v = struct.unpack_from('<10I', r)
        if v[1] == SOURCE_RACE:
            out[(v[2], v[3], v[8], v[9])] = [nrm.string(strings, o).strip() if o else '' for o in v[4:7]]
    return out


def hair_geosets(package):
    rows, _, _ = nrm.load_dbc(os.path.join(package, 'DBFilesClient', 'CharHairGeosets.dbc'))
    out = {}
    for r in rows:
        v = struct.unpack_from('<6i', r)
        if v[1] == SOURCE_RACE:
            out[(v[2], v[3])] = (v[4], v[5])
    return out


def hair_styles(geosets, gender):
    """(name, geoset, show scalp) per variation: Forever's styles, then those with feathers (all but Bald)"""
    names = HAIR[('male', 'female')[gender]]
    plain = [(n,) + geosets[(gender, v)] for v, n in enumerate(names)]
    return plain + [(n + ' with Feathers', FEATHERED + g, 0) for n, g, _ in plain if g]


def facial_styles(gender):
    """(name, geoset_1 (group 1), geoset_3 (group 2)) per style"""
    if gender:
        return [(e, 0, i + 1) for i, e in enumerate(EYEBROWS)]
    beards = [('Clean', 0)] + [(b, i + 2) for i, b in enumerate(BEARDS)]   # beards are geosets 102-113
    return [('%s, %s Eyebrows' % (b, e), g, i + 1) for b, g in beards for i, e in enumerate(EYEBROWS)]


def charsections(key, src, geosets):
    rows = []

    def row(gender, section, tex, flags, type_, colour):
        rows.append("(@CharSectionsID := @CharSectionsID +1, @%s, %-8s %-12s %s, %s, %s, %d, %d, %d)" % (
            key, ('@Male', '@Female')[gender] + ',', nrm.SECTIONS[section] + ',', sql(tex[0]), sql(tex[1]), sql(tex[2]),
            flags, type_, colour))

    colours = SKINS * EYES
    for gender in (0, 1):
        for c in range(colours):
            row(gender, 0, src[(gender, 0, 0, c)], 17, 0, c)
        for c in range(colours):
            for face in range(FACES):
                row(gender, 1, src[(gender, 1, face, c)], 1, face, c)
        for style in range(len(facial_styles(gender))):
            for colour in range(HAIR_COLOURS):
                row(gender, 2, [OVERLAY, '', ''], 17, style, colour)
        for style in range(len(hair_styles(geosets, gender))):
            for colour in range(HAIR_COLOURS):   # the package's hair textures only depend on the colour
                row(gender, 3, src[(gender, 3, 0, colour)], 17, style, colour)
        for c in range(colours):
            row(gender, 4, src[(gender, 4, 0, c)], 17, 0, c)
    return ("-- charsections: %d inserts, 0 updates, 0 deletes\n"
            "-- The native Skyborne from Kalibro's races package (tools/races/skyborne_native.py); the Forever client only reads row 0\n\n"
            "-- New entries\nDELETE FROM `charsections` WHERE `race` = @%s;\n"
            "SET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);\n"
            "INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES\n"
            "%s;\n" % (len(rows), key, ',\n'.join(rows)))


def charhairgeosets(key, geosets):
    rows = []
    for gender in (0, 1):
        for v, (_, geoset, scalp) in enumerate(hair_styles(geosets, gender)):
            rows.append("(@CharHairGeosetsID := @CharHairGeosetsID +1, @%s, %-8s %2d, %2d, %d)" % (key, ('@Male', '@Female')[gender] + ',', v, geoset, scalp))
    return ("-- charhairgeosets: %d inserts, 0 updates, 0 deletes\n-- Forever's styles (the package's first %d / %d variations), then each with its feathers (geoset 50 + style,\n-- made by tools/models/skyborne_native_prep.py)\n\n"
            "-- New entries\nDELETE FROM `charhairgeosets` WHERE `race` = @%s;\n"
            "SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);\n"
            "INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES\n%s;\n"
            % (len(rows), len(HAIR['male']), len(HAIR['female']), key, ',\n'.join(rows)))


EYE_GLOW = 2   # geoset_5: geoset 1702, the yellow eye glow skyborne_eye_glow.py gives the models (as Night Elves glow)


def facialstyles(key):
    rows = ["(@%s, %-8s %2d, %2d, 0, %d, 0, %d)" % (key, ('@Male', '@Female')[g] + ',', v, s[1], s[2], EYE_GLOW)
            for g in (0, 1) for v, s in enumerate(facial_styles(g))]
    return ("-- characterfacialhairstyles: %d inserts, 0 updates, 0 deletes\n"
            "-- Male: beard (group 1, 102-113) x eyebrows (group 2, 201-204). Female: eyebrows. All: eye glow 1702\n\n"
            "-- New entries\nDELETE FROM `characterfacialhairstyles` WHERE `race` = @%s;\n"
            "INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES\n%s;\n"
            % (len(rows), key, ',\n'.join(rows)))


def barbershop(key, old, geosets):
    insert = re.search(r'^INSERT INTO `barbershopstyle`.*$', old, re.M).group(0)
    rows = []
    for g, sex in ((0, 'male'), (1, 'female')):
        for t, names in ((0, [s[0] for s in hair_styles(geosets, g)]), (2, [s[0] for s in facial_styles(g)])):
            for v, name in enumerate(names):
                rows.append("(@BarbershopStyleID := @BarbershopStyleID +1, %d, %s%s, 16712190, ''%s, 16712172, '%s', @%s, %s, %d)"
                            % (t, nrm.sql_str(name), GAP, GAP, '1.0000000000000000' if t == 0 else '0.7500000000000000', key, ('@Male', '@Female')[g], v))
    return ("-- barbershopstyle: %d inserts, 0 updates, 0 deletes\n-- type 0 = hair style, type 2 = facial hair; Forever's names\n\n"
            "-- New entries\nDELETE FROM `barbershopstyle` WHERE `race` = @%s;\n"
            "SET @BarbershopStyleID = (SELECT COALESCE(MAX(id), 0) FROM `barbershopstyle`);\n%s\n%s;\n" % (len(rows), key, insert, ',\n'.join(rows)))


def model_paths(key, folder, tag):
    """The Blood Elf model rows keep size, collision and sounds; only the file changes."""
    name = os.path.join(folder, 'dbc', tag + '_creaturemodeldata.sql')
    text = open(name, encoding='utf-8', newline='').read()
    for gender in ('Male', 'Female'):
        text = text.replace('SELECT @%s%sModel, 2052, `model_path`,' % (key, gender), 'SELECT @%s%sModel, 2052, @%s%sModelPath,' % (key, gender, key, gender))
    text = text.replace('-- Copies of the stock model rows, with', "-- Size, collision and sounds of the Blood Elf model rows, with")
    nrm.write(name, text)
    name = os.path.join(folder, 'variables.sql')
    text = open(name, encoding='utf-8', newline='').read()
    if '%sMaleModelPath' % key not in text:
        lines = ''.join("SET @%s%sModelPath = %s;\n" % (key, g, path('custom', 'skyborne', 'native', g.lower(), 'skyborne%s.mdx' % g.lower()))
                        for g in ('Male', 'Female'))
        text, count = re.subn(r'(?m)^(SET @%sBlood = 1;\r?\n)' % key, lambda m: m.group(1) + lines, text)
        assert count == 1, name
    # Facial style labels (GlueStrings FACIAL_HAIR_*): beards and eyebrows for males, eyebrows for females
    for var, label in (('FacialHairCustomization1', 'NORMAL'), ('FacialHairCustomization2', 'EYEBROWS')):
        text = re.sub(r"(SET @%s%s\s*= )'[^']*';" % (key, var), lambda m: m.group(1) + "'%s';" % label, text)
    nrm.write(name, text)


def copy_files(package, common, src):
    """The models (renamed, with their .skin and .anim files), the textures they name and the rows' textures."""
    root = os.path.join(package, 'custom', 'skyborne')
    dest = os.path.join(common, 'custom', 'skyborne')
    wanted = {}   # destination (relative to patch-A.MPQ) -> source file
    textures = set()
    for sex, stem in MODELS.items():
        folder = os.path.join(root, 'expanded', sex)
        target = os.path.join('custom', 'skyborne', 'native', sex)
        wanted[os.path.join(target, 'skyborne%s.m2' % sex)] = os.path.join(folder, stem + '.m2')
        wanted[os.path.join(target, 'skyborne%s00.skin' % sex)] = os.path.join(folder, stem + '00.skin')
        for anim in glob.glob(os.path.join(folder, stem + '[0-9][0-9][0-9][0-9]-[0-9][0-9].anim')):
            wanted[os.path.join(target, 'skyborne%s%s' % (sex, os.path.basename(anim)[len(stem):]))] = anim
        textures.update(kalibro_races.m2_textures(os.path.join(folder, stem + '.m2')))
    for tex in src.values():
        textures.update(t for t in tex if t)
    textures.add(OVERLAY)
    missing = []
    for t in sorted(textures):
        rel = os.path.join(*t.split(BS))
        if os.path.isfile(os.path.join(package, rel)):
            wanted[rel] = os.path.join(package, rel)
        else:
            missing.append(t)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    size = padded = 0
    for rel, source in sorted(wanted.items()):
        target = os.path.join(common, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy2(source, target)
        if target.lower().endswith('.blp'):
            padded += kalibro_races.pad_mips(target)
        size += os.path.getsize(target)
    print('custom/skyborne: %d files (%d MB), %d mip chains completed' % (len(wanted), size >> 20, padded))
    for m in missing:
        print('  missing in the package:', m)
    # the copied models need their geosets fixed every time
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))
    import skyborne_native_prep
    for sex in MODELS:
        print(sex, skyborne_native_prep.prep(os.path.join(common, 'custom', 'skyborne', 'native', sex, 'skyborne%s00.skin' % sex)))


def apply(modpaks_dirs, package=PACKAGE, common=COMMON, files=True):
    if isinstance(modpaks_dirs, str):
        modpaks_dirs = [modpaks_dirs]
    src = package_rows(package)
    geosets = hair_geosets(package)
    for modpaks in modpaks_dirs:
        for key, fnum in RACES:
            folders = glob.glob(os.path.join(glob.escape(modpaks), 'F-%03d_*' % fnum))
            assert len(folders) == 1, folders
            folder = folders[0]
            tag = '[BASE,F-%03d]' % fnum
            dbc = os.path.join(folder, 'dbc', tag + '_%s.sql')
            old = open(dbc % 'barbershopstyle', encoding='utf-8').read()
            nrm.write(dbc % 'barbershopstyle', barbershop(key, old, geosets))
            nrm.write(dbc % 'charsections', charsections(key, src, geosets))
            nrm.write(dbc % 'charhairgeosets', charhairgeosets(key, geosets))
            nrm.write(dbc % 'characterfacialhairstyles', facialstyles(key))
            model_paths(key, folder, tag)
            print(os.path.basename(folder), 'done')
    if files:
        copy_files(package, common, src)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('modpaks', nargs='+')
    ap.add_argument('--package', default=PACKAGE)
    ap.add_argument('--common', default=COMMON)
    ap.add_argument('--no-files', action='store_true')
    a = ap.parse_args()
    apply(a.modpaks, a.package, a.common, not a.no_files)
