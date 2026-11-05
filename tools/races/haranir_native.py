#!/usr/bin/env python3
"""Point F-098/F-099 at the native Haranir baked by tools/models/haranir_native_prep.py: model paths and customization rows.

Clients that map the race in retailRaces don't read these beyond row 0, as with F-040. Sliders:
- skin colour: Retail's 20 colours
- face: Retail's faces, then the same faces with the Growth face paint
- hair style and hair colour: Retail's (no highlights)
- facial style: male: no facial hair, each beard, each pair of sideburns, each moustache. Female: Retail's eyebrows

usage: haranir_native.py <modpaks dir> [more modpaks dirs ...]
Rewrites the files, so it can be rerun."""
import glob, os, re, sys

BS = '\\\\'     # as written in the SQL files
SKINS = 20
HAIR_COLOURS = 30
FACES = {'Male': 16, 'Female': 18}
HAIR = {'Male': ('Bald', 'Tendril', 'Abundant', 'Flourish', 'Balance', 'Petals', 'Spore', 'Reach', 'Barbed', 'Moss', 'Commune',
                 'Overgrowth', 'Wilted', 'Vines', 'Bundled', 'Gathered', 'Blades', 'Rootways'),
        'Female': ('Bald', 'Flow', 'Balance', 'Sprout', 'Moss', 'Reach', 'Spore', 'Wilted', 'Flora', 'Overgrowth', 'Vines', 'Tendril',
                   'Spinehawk', 'Commune', 'Abundant', 'Petals', 'Bundled', 'Blooming')}
BEARDS = ('Growth', 'Bloom', 'Brush', 'Pruned', 'Spines', 'Knot', 'Tendrils')
SIDEBURNS = ('Wild', 'Full', 'Cheek', 'Low', 'Neat', 'Knots', 'Spines', 'Sparse')
MOUSTACHES = ('Short', 'Long', 'Full', 'Sparse', 'Spines')
EYEBROWS = ('Clean', 'Low', 'Medium', 'High', 'Partial', 'Straight', 'Bushy', 'Thorns', 'Reach', 'Branch', 'Swept', 'Short Spines',
            'Long Spines', 'Sparse')
RACES = (('AllianceHaranir', 98), ('HordeHaranir', 99))
GAP = ", ''" * 15


def facial_styles(gender):
    """(name, geoset_1 (group 1), geoset_2 (group 3), geoset_3 (group 2)) per style"""
    if gender == 'Female':     # the model's eyebrows are moved to group 1
        return [(name, i + 1, 0, 0) for i, name in enumerate(EYEBROWS)]
    return ([('None', 0, 0, 0)] + [(n + ' Beard', i + 1, 0, 0) for i, n in enumerate(BEARDS)] +
            [(n + ' Moustache', 0, i + 1, 0) for i, n in enumerate(MOUSTACHES)] +
            [(n + ' Sideburns', 0, 0, i + 1) for i, n in enumerate(SIDEBURNS)])


def path(gender, name):
    return "'custom{0}haranir{0}native{0}{1}{0}{2}.blp'".format(BS, gender.lower(), name)


def write(path_, text):
    with open(path_, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def charsections(key):
    rows = []

    def row(gender, section, t1, t2, flags, type_, colour):
        rows.append("(@CharSectionsID := @CharSectionsID +1, @%s, %-8s %-12s %s, %s, '', %d, %d, %d)"
                    % (key, '@' + gender + ',', '@' + section + ',', t1, t2, flags, type_, colour))

    for gender in ('Male', 'Female'):
        for skin in range(SKINS):
            row(gender, 'Skin', path(gender, 'body%d' % skin), "''", 17, 0, skin)
        for skin in range(SKINS):
            for face in range(FACES[gender]):
                row(gender, 'Face', path(gender, 'facelower%d_%d' % (skin, face)), path(gender, 'faceupper%d_%d' % (skin, face)), 1, face, skin)
        for style in range(len(facial_styles(gender))):
            for colour in range(HAIR_COLOURS):
                row(gender, 'FacialHair', "''", "''", 17, style, colour)
        for style in range(len(HAIR[gender])):
            for colour in range(HAIR_COLOURS):
                row(gender, 'Hair', path(gender, 'hair%d' % colour), "''", 17, style, colour)
        for skin in range(SKINS):
            row(gender, 'Underwear', path(gender, 'pelvis%d' % skin), path(gender, 'torso%d' % skin) if gender == 'Female' else "''", 17, 0, skin)
    return ("-- charsections: %d inserts, 0 updates, 0 deletes\n"
            "-- The native Haranir baked by tools/models/haranir_native_prep.py (the Retail client only reads row 0)\n\n"
            "-- New entries\nDELETE FROM `charsections` WHERE `race` = @%s;\n"
            "SET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);\n"
            "INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES\n"
            "%s;\n" % (len(rows), key, ',\n'.join(rows)))


def hairgeosets(key):
    rows = ["(@CharHairGeosetsID := @CharHairGeosetsID +1, @%s, %-8s %2d, %2d, %d)" % (key, '@' + g + ',', v, v + 1 if v else 0, 0 if v else 1)
            for g in ('Male', 'Female') for v in range(len(HAIR[g]))]
    return ("-- charhairgeosets: %d inserts, 0 updates, 0 deletes\n-- Bald, then the model's styles (haranir_native_prep.py moves 4002-4018 to group 0)\n\n"
            "-- New entries\nDELETE FROM `charhairgeosets` WHERE `race` = @%s;\n"
            "SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);\n"
            "INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES\n%s;\n" % (len(rows), key, ',\n'.join(rows)))


def facialstyles(key):
    rows = ["(@%s, %-8s %2d, %2d, %2d, %2d, 0, 0)" % (key, '@' + g + ',', v, s[1], s[2], s[3])
            for g in ('Male', 'Female') for v, s in enumerate(facial_styles(g))]
    return ("-- characterfacialhairstyles: %d inserts, 0 updates, 0 deletes\n"
            "-- Male: groups 1 (beard), 3 (moustache) and 2 (sideburns). Female: eyebrows, moved to group 1 by haranir_native_prep.py\n\n"
            "-- New entries\nDELETE FROM `characterfacialhairstyles` WHERE `race` = @%s;\n"
            "INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES\n%s;\n"
            % (len(rows), key, ',\n'.join(rows)))


def barbershop(key, old):
    insert = re.search(r'^INSERT INTO `barbershopstyle`.*$', old, re.M).group(0)
    rows = []

    def row(type_, name, gender, data):
        rows.append("(@BarbershopStyleID := @BarbershopStyleID +1, %d, '%s'%s, 16712190, ''%s, 16712172, '1.0000000000000000', @%s, @%s, %d)"
                    % (type_, name, GAP, GAP, key, gender, data))

    for gender in ('Male', 'Female'):
        for v, name in enumerate(HAIR[gender]):
            row(0, name, gender, v)
        for v, style in enumerate(facial_styles(gender)):
            row(2, style[0], gender, v)
    return ("-- barbershopstyle: %d inserts, 0 updates, 0 deletes\n-- type 0 = hair style, type 2 = facial hair; Retail's names\n\n"
            "-- New entries\nDELETE FROM `barbershopstyle` WHERE `race` = @%s;\n"
            "SET @BarbershopStyleID = (SELECT COALESCE(MAX(id), 0) FROM `barbershopstyle`);\n%s\n%s;\n" % (len(rows), key, insert, ',\n'.join(rows)))


def model_paths(key, folder, tag):
    """The Home race's model rows keep size, collision and sounds; only the file changes."""
    name = os.path.join(folder, 'dbc', tag + '_creaturemodeldata.sql')
    text = open(name, encoding='utf-8', newline='').read()
    for gender in ('Male', 'Female'):
        text = text.replace('SELECT @%s%sModel, 2052, `model_path`,' % (key, gender), 'SELECT @%s%sModel, 2052, @%s%sModelPath,' % (key, gender, key, gender))
    text = text.replace('-- Copies of the stock model rows, with', '-- Size, collision and sounds of the Home race\'s stock model rows, with')
    write(name, text)
    name = os.path.join(folder, 'variables.sql')
    text = open(name, encoding='utf-8', newline='').read()
    if '%sMaleModelPath' % key not in text:
        lines = ''.join("SET @%s%sModelPath = 'custom%shara" "nir%snative%s%s%sharronir%s.mdx';\n" % (key, g, BS, BS, BS, g.lower(), BS, g.lower()) for g in ('Male', 'Female'))
        text, count = re.subn(r'(?m)^(SET @%sBlood = 1;\r?\n)' % key, lambda m: m.group(1) + lines, text)
        assert count == 1, name
    write(name, text)


def apply(modpaks):
    for key, fnum in RACES:
        folders = glob.glob(os.path.join(glob.escape(modpaks), 'F-0%d_*' % fnum))
        assert len(folders) == 1, folders
        folder = folders[0]
        tag = '[BASE,F-0%d]' % fnum
        dbc = os.path.join(folder, 'dbc', tag + '_%s.sql')
        old = open(dbc % 'barbershopstyle', encoding='utf-8').read()
        write(dbc % 'barbershopstyle', barbershop(key, old))
        write(dbc % 'charsections', charsections(key))
        write(dbc % 'charhairgeosets', hairgeosets(key))
        write(dbc % 'characterfacialhairstyles', facialstyles(key))
        model_paths(key, folder, tag)
        print(os.path.basename(folder), 'done')


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        apply(arg)
