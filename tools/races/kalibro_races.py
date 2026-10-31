#!/usr/bin/env python3
"""Take Lightforged Draenei, Nightborne and Void Elf (F-033..F-035) from Kalibro's races package.

The package (Kalibros_Races_<date>: Character, DBFilesClient, ...) has their complete retail-derived models (four skin
profiles, .anim files) and texture sets, with customization rows for the stock 3.3.5 compositor in its DBFilesClient
(its races 21, 17 and 19). This script
- rewrites the modpaks' charsections, charhairgeosets, characterfacialhairstyles and barbershopstyle files from those
  rows (renumbered to the modpaks' race variables). Duplicate keys are dropped: CharSections keeps the last row of a
  (gender, section, type, colour), as the client does; CharHairGeosets and CharacterFacialHairStyles keep the row of a
  (gender, variation) whose geosets the model has (the first on a tie);
- replaces the races' folders in WHE-common's patch-A.MPQ with the files the models and rows use (models, skins, .anim
  files, the textures named in the models and the CharSections textures), completing truncated BLP mip chains.

The models also declare retail texture types (15-20) that the 3.3.5 client never fills, but no batch draws with them.

usage: kalibro_races.py <Kalibros_Races folder> [modpaks dir] [WHE-common patch-A.MPQ] [more modpaks dirs ...]
(more modpaks dirs get the same customization files, e.g. another checkout with these modpaks)"""
import glob, os, re, shutil, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import new_race_modpaks as nrm   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
# key, modpak, Kalibro's race id, race folders in Kalibro's Character folder and WHE-common's, barber shop file name
RACES = [
    ('LightforgedDraenei', 'F-033_mod-lightforged-draenei', 21, 'LightForgedDraenei', 'lightforgeddraenei', 'barbershopstyle'),
    ('Nightborne', 'F-034_mod-nightborne', 17, 'nightborne', 'Nightborne', 'barbershopstyles'),
    ('VoidElf', 'F-035_mod-void-elf', 19, 'VoidElf', 'Voidelf', None),
]
SOURCE = 'Kalibro\'s races package (Kalibros_Races_20261012, race %d)'
BS = '\\'


def dbc_rows(folder, name):
    rows, strings, f = nrm.load_dbc(os.path.join(folder, 'DBFilesClient', name + '.dbc'))
    return [struct.unpack_from('<%dI' % f, r) for r in rows], strings


def model_geosets(package, kfolder):
    """gender -> geoset ids of the race's model (its first skin profile)"""
    geosets = {}
    for gender, name in enumerate(('male', 'female')):
        for m in glob.glob(os.path.join(package, 'Character', kfolder, '*', '*.m2')):
            if os.path.basename(os.path.dirname(m)).lower() == name:
                s = open(m[:-3] + '00.skin', 'rb').read()
                count, offset = struct.unpack_from('<II', s, 28)
                geosets[gender] = {struct.unpack_from('<H', s, offset + 48 * i)[0] for i in range(count)}
    return geosets


def missing_geosets(model, pairs):
    """how many of the (group, value) choices pick a geoset the model lacks, in groups the model has"""
    return sum(1 for group, value in pairs
               if any(g // 100 == group for g in model) and group * 100 + value not in model)


def customization(package, race, kfolder):
    rows, strings = dbc_rows(package, 'CharSections')
    sections = {}
    for v in rows:   # id, race, gender, section, texture 1-3, flags, type, colour
        if v[1] == race:
            key = (v[2], v[3], v[8], v[9])
            sections.pop(key, None)   # the client keeps the last row of a key: move it to the end
            sections[key] = ([nrm.string(strings, o).strip() for o in v[4:7]], v[7])
    # The package repeats some (gender, variation) keys with stray rows ahead of the complete set (e.g. Void Elf style 0
    # without eyes or ears). The client takes the first, so keep the row whose geosets the model has, the first on a tie.
    geosets = model_geosets(package, kfolder)
    hair = {}
    for v in dbc_rows(package, 'CharHairGeosets')[0]:   # id, race, gender, variation, geoset, show scalp
        if v[1] == race:
            row = tuple(struct.unpack('<4i', struct.pack('<4I', *v[2:6])))
            score = missing_geosets(geosets.get(row[0], ()), [(0, row[2])])
            if row[:2] not in hair or score < hair[row[:2]][0]:
                hair[row[:2]] = (score, row)
    facial = {}
    for v in dbc_rows(package, 'CharacterFacialHairStyles')[0]:   # race, gender, variation, geosets
        if v[0] == race:
            row = (v[1], v[2]) + tuple(g if g != 0xCCCCCCCC else 0 for g in v[3:8])
            # geoset columns 1-5 are groups 1xx, 3xx, 2xx, 16xx and 17xx (eyes)
            score = missing_geosets(geosets.get(row[0], ()), zip((1, 3, 2, 16, 17), row[2:7]))
            if row[:2] not in facial or score < facial[row[:2]][0]:
                facial[row[:2]] = (score, row)
    return sections, sorted(r for _, r in hair.values()), sorted(r for _, r in facial.values())


def barber_names(path):
    """(type, gender, data) -> display name of the modpak's current barber shop rows, to keep the named ones"""
    names = {}
    if os.path.exists(path):
        for m in re.finditer(r"\+1, (\d+), '((?:[^'\\]|\\.)*)', .*?, @\w+, @(Male|Female), (\d+)\)", open(path, encoding='utf-8').read()):
            if m.group(2):
                names[(int(m.group(1)), m.group(3), int(m.group(4)))] = m.group(2).replace("\\'", "'")
    return names


def write_customization(out, key, fnum, race, barber, sections, hair, facial):
    tag = '[BASE,%s]' % fnum
    source = SOURCE % race
    lines = []
    for (gender, section, var, colour), (tex, flags) in sections.items():
        lines.append("(@CharSectionsID := @CharSectionsID +1, @%s, %-7s %-12s %s, %s, %s, %d, %d, %d)" % (
            key, ('@Male', '@Female')[gender] + ',', nrm.SECTIONS[section] + ',', nrm.sql_str(tex[0]), nrm.sql_str(tex[1]),
            nrm.sql_str(tex[2]), flags, var, colour))
    nrm.write(os.path.join(out, 'dbc', tag + '_charsections.sql'),
              "-- charsections: %d inserts, 0 updates, 0 deletes\n-- From %s, with its flags\n\n"
              "-- New entries\nDELETE FROM `charsections` WHERE `race` = @%s;\nSET @CharSectionsID = (SELECT COALESCE(MAX(id), 0) FROM `charsections`);\n"
              "INSERT INTO `charsections` (`id`, `race`, `gender`, `base_section`, `texture_1`, `texture_2`, `texture_3`, `flags`, `type`, `color_index`) VALUES\n%s;"
              % (len(lines), source, key, ',\n'.join(lines)))

    lines = ["(@CharHairGeosetsID := @CharHairGeosetsID +1, @%s, %-8s %2d, %2d, %d)" % (key, ('@Male', '@Female')[g] + ',', var, geoset, scalp)
             for g, var, geoset, scalp in hair]
    nrm.write(os.path.join(out, 'dbc', tag + '_charhairgeosets.sql'),
              "-- charhairgeosets: %d inserts, 0 updates, 0 deletes (from %s)\n\n-- New entries\nDELETE FROM `charhairgeosets` WHERE `race` = @%s;\n"
              "SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);\n"
              "INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES\n%s;" % (len(lines), source, key, ',\n'.join(lines)))

    lines = ["(@%s, %-8s %2d, %s)" % (key, ('@Male', '@Female')[row[0]] + ',', row[1], ', '.join('%d' % x for x in row[2:7])) for row in facial]
    nrm.write(os.path.join(out, 'dbc', tag + '_characterfacialhairstyles.sql'),
              "-- characterfacialhairstyles: %d inserts, 0 updates, 0 deletes (from %s)\n\n-- New entries\n"
              "DELETE FROM `characterfacialhairstyles` WHERE `race` = @%s;\n"
              "INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES\n%s;"
              % (len(lines), source, key, ',\n'.join(lines)))

    if not barber:
        return
    path = os.path.join(out, 'dbc', '%s_%s.sql' % (tag, barber))
    names = barber_names(path)
    cols = ', '.join(['`id`', '`type`'] + ['`display_name_%s`' % l for l in ('enus', 'kokr', 'frfr', 'dede', 'zhcn', 'zhtw', 'eses', 'esmx', 'ruru', 'jajp', 'ptpt', 'itit', 'unused_1', 'unused_2', 'unused_3', 'unused_4')]
                     + ['`display_name_flags`'] + ['`description_%s`' % l for l in ('enus', 'kokr', 'frfr', 'dede', 'zhcn', 'zhtw', 'eses', 'esmx', 'ruru', 'jajp', 'ptpt', 'itit', 'unused_1', 'unused_2', 'unused_3', 'unused_4')]
                     + ['`description_flags`', '`cost_modifier`', '`race`', '`gender`', '`data`'])
    lines = []
    for gi, g in enumerate(['@Male', '@Female']):
        for t, label, variations in ((0, 'Style', sorted({h[1] for h in hair if h[0] == gi})), (2, 'Facial Style', sorted({h[1] for h in facial if h[0] == gi}))):
            for v in variations:
                name = names.get((t, g[1:], v), '%s %d' % (label, v + 1))
                lines.append("(@BarbershopStyleID := @BarbershopStyleID +1, %d, %s, %s, 16712190, %s, 16712172, '%s', @%s, %s, %d)" % (
                    t, nrm.sql_str(name), ', '.join(["''"] * 15), ', '.join(["''"] * 16), '1.0000000000000000' if t == 0 else '0.7500000000000000', key, g, v))
    nrm.write(path,
              "-- barbershopstyle: %d inserts, 0 updates, 0 deletes\n-- type 0 = hair style, type 2 = facial hair: one per CharHairGeosets / CharacterFacialHairStyles variation;\n"
              "-- generic names where the earlier rows had none\n\n-- New entries\n"
              "DELETE FROM `barbershopstyle` WHERE `race` = @%s;\nSET @BarbershopStyleID = (SELECT COALESCE(MAX(id), 0) FROM `barbershopstyle`);\n"
              "INSERT INTO `barbershopstyle` (%s) VALUES\n%s;" % (len(lines), key, cols, ',\n'.join(lines)))


def m2_textures(path):
    d = open(path, 'rb').read()
    count, offset = struct.unpack_from('<II', d, 0x50)
    names = []
    for i in range(count):
        _, _, length, at = struct.unpack_from('<IIII', d, offset + 16 * i)
        name = d[at:at + length].split(b'\0')[0].decode('latin1')
        if name:
            names.append(name)
    return names


def pad_mips(path):
    """Complete a BLP's mip chain down to 1x1 by repeating its smallest level; returns whether the file changed.

    Many of the package's textures stop a level or two short. The compositor reads single levels and doesn't mind,
    but textures set on the model (Nightborne jewelry, Void Elf hair) are reloaded whole and come out white."""
    d = bytearray(open(path, 'rb').read())
    if d[:4] != b'BLP2' or not d[11]:
        return False
    encoding, alpha_depth, alpha_type = d[8], d[9], d[10]
    width, height = struct.unpack_from('<II', d, 12)
    offsets, sizes = list(struct.unpack_from('<16I', d, 20)), list(struct.unpack_from('<16I', d, 84))
    levels, w, h = [], width, height
    while True:
        levels.append((w, h))
        if w == 1 and h == 1:
            break
        w, h = max(w >> 1, 1), max(h >> 1, 1)
    have = next((i for i, s in enumerate(sizes) if not s), 16)
    if have >= len(levels) or not have:
        return False
    last = bytes(d[offsets[have - 1]:offsets[have - 1] + sizes[have - 1]])
    for i in range(have, len(levels)):
        w, h = levels[i]
        if encoding == 2:   # DXT: whole 4x4 blocks
            block = 8 if alpha_type == 0 else 16
            level = last[:block] * (max(1, (w + 3) // 4) * max(1, (h + 3) // 4))
        elif encoding == 1:   # palette indices, then the alpha bits
            lw, lh = levels[have - 1]
            level = last[:1] * (w * h) + (last[lw * lh:lw * lh + 1] or b'\xff') * ((w * h * alpha_depth + 7) // 8)
        else:   # raw BGRA
            level = last[:4] * (w * h)
        offsets[i], sizes[i] = len(d), len(level)
        d += level
    struct.pack_into('<16I', d, 20, *offsets)
    struct.pack_into('<16I', d, 84, *sizes)
    open(path, 'wb').write(d)
    return True


def copy_assets(package, common, kfolder, wfolder, sections):
    """Replace WHE-common's race folder with the files the models and rows use; returns (files, bytes, missing)"""
    index = {}   # lower-case path below the package -> real path
    for root, _, files in os.walk(package):
        for f in files:
            full = os.path.join(root, f)
            index[os.path.relpath(full, package).replace('/', BS).lower()] = full
    src_root = os.path.join(package, 'Character', kfolder)
    models = [p for p in glob.glob(os.path.join(src_root, '*', '*.m2'))]
    wanted = set()
    for m in models:
        stem = m[:-3]
        wanted.update(glob.glob(stem + '0?.skin') + glob.glob(stem + '[0-9][0-9][0-9][0-9]-[0-9][0-9].anim') + [m])
        wanted.update(index.get(t.lower()) or t for t in m2_textures(m))
    for tex, _ in sections.values():
        wanted.update(index.get(t.replace('/', BS).lower()) or t for t in tex if t)
    missing = sorted(w for w in wanted if not os.path.isfile(w))
    wanted -= set(missing)

    dest_root = os.path.join(common, 'Character', wfolder)
    for root, _, files in os.walk(dest_root):
        for f in files:
            os.remove(os.path.join(root, f))
    total = padded = 0
    for w in sorted(wanted):
        rel = os.path.relpath(w, package).split(os.sep)
        if rel[0].lower() == 'character' and rel[1].lower() == kfolder.lower():
            rel[1] = wfolder   # WHE-common's spelling of the race folder (case-insensitive for the client)
        dst = os.path.join(common, *rel)
        if not os.path.realpath(dst).lower().startswith(os.path.realpath(dest_root).lower()) and os.path.exists(dst):
            continue   # another race's file (e.g. Character\Eredar\EredarCaustic.blp): keep WHE-common's
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(w, dst)
        if dst.lower().endswith('.blp'):
            padded += pad_mips(dst)
        total += os.path.getsize(dst)
    for root, dirs, files in os.walk(dest_root, topdown=False):
        if not os.listdir(root):
            os.rmdir(root)
    return len(wanted), total, padded, missing


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    package = sys.argv[1]
    modpaks = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', 'modpaks')
    common = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', '..', '..', 'WHE-common', 'patch-A.MPQ')
    for key, modpak, race, kfolder, wfolder, barber in RACES:
        sections, hair, facial = customization(package, race, kfolder)
        for folder in [modpaks] + sys.argv[4:]:
            write_customization(os.path.join(folder, modpak), key, modpak[:5], race, barber, sections, hair, facial)
        files, size, padded, missing = copy_assets(package, common, kfolder, wfolder, sections)
        print('%s: %d charsections, %d hair geosets, %d facial styles; %d files (%d MB) copied, %d mip chains completed' % (
            key, len(sections), len(hair), len(facial), files, size >> 20, padded))
        for m in missing:
            print('  missing in the package:', m)


if __name__ == '__main__':
    main()
