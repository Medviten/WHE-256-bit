#!/usr/bin/env python3
"""Find the files F-013's item displays name that the client doesn't have, and copy those Zeppelin has.

Zeppelin's goblin-start items use Cataclysm icons, armour textures and models. Its own client carries them, ours only
when they are in WHE-common (or stock). An item whose files are missing shows no icon and paints nothing when worn.

For each row of F-013's [AUTO,F-011]_itemdisplayinfo.sql this looks up the icon, the models (any ObjectComponents
folder; head models with any race suffix) and textures, and the armour textures (any of _U, _M, _F) in WHE-common, the
client's patch folders and its MPQs (enUS ones included). With --copy, what is missing but in Zeppelin's extracted
client files (ZEPPELIN/Work, the output of extracting its patches) is copied to WHE-common under the client's path.

usage: f013_item_assets.py [--client DATA] [--common PATH] [--zeppelin DATA] [--copy]"""
import argparse, collections, glob, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_f013_assets import Archive  # noqa: E402

B = chr(92)
HERE = os.path.dirname(os.path.abspath(__file__))
F013 = os.path.join(HERE, '..', '..', 'modpaks', 'F-013_zep-goblin-start')
MODEL_DIRS = ('Weapon', 'Shield', 'Head', 'Shoulder', 'Quiver', 'Ammo', 'Cape')
REGIONS = {'upper_arm_texture': 'ArmUpperTexture', 'lower_arm_texture': 'ArmLowerTexture', 'hands_texture': 'HandTexture',
           'upper_torso_texture': 'TorsoUpperTexture', 'lower_torso_texture': 'TorsoLowerTexture',
           'upper_leg_texture': 'LegUpperTexture', 'lower_leg_texture': 'LegLowerTexture', 'foot_texture': 'FootTexture'}


def tree(root):
    """Upper-case client path -> real path for every file under root."""
    out = {}
    for dirpath, _, names in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        for name in names:
            out[os.path.normpath(os.path.join(rel, name)).upper().replace(os.sep, B).lstrip('.' + B)] = \
                os.path.join(dirpath, name)
    return out


def needs(row):
    """(what, [candidate client paths]) for each file a display row names."""
    out = []
    if row.get('icon_1'):
        out.append(('icon ' + row['icon_1'], [B.join(('Interface', 'Icons', row['icon_1'] + '.blp'))]))
    for k in ('left_model', 'right_model'):
        m = re.sub(r'\.(mdx|mdl|m2)$', '', row.get(k, ''), flags=re.I)
        if m:
            out.append(('model ' + m, [B.join(('Item', 'ObjectComponents', d, m)) for d in MODEL_DIRS]))
    for k in ('left_model_texture', 'right_model_texture'):
        t = row.get(k, '')
        if t:
            out.append(('texture ' + t, [B.join(('Item', 'ObjectComponents', d, t + '.blp')) for d in MODEL_DIRS]))
    for k, region in REGIONS.items():
        t = row.get(k, '')
        if t:
            out.append((region + ' ' + t, [B.join(('Item', 'TextureComponents', region, t + s + '.blp'))
                                           for s in ('_U', '_M', '_F')]))
    return out


def creature_needs(client):
    """(display, what, [candidates]) for the models and texture variations of F-013's creature displays; model paths
    come from the client's built CreatureModelData.dbc (the displays can name a model by a variable)."""
    import struct
    d = open(os.path.join(client, 'patch-A.MPQ', 'DBFilesClient', 'CreatureModelData.dbc'), 'rb').read()
    _, n, fields, size, _ = struct.unpack('<4s4I', d[:20])
    table = 20 + n * size
    models = {}
    for i in range(n):
        mid, _, name = struct.unpack_from('<3I', d, 20 + i * size)
        models[mid] = d[table + name:d.index(b'\0', table + name)].decode('latin1')
    # every display the modpak inserts or updates, as the client's built DBC has it
    ids = set()
    for path in glob.glob(os.path.join(F013, 'dbc', '*creaturedisplayinfo*.sql')):
        text = open(path, encoding='utf-8').read()
        ids.update(int(i) for i in re.findall(r"`id` = (\d+),", text))
        for where in re.findall(r"WHERE\s+`?id`?\s*(?:=\s*(\d+)|IN\s*\(([\d,\s]+)\))", text, re.I):
            ids.update(int(i) for i in (where[0] or where[1]).replace(' ', '').split(',') if i)
    d = open(os.path.join(client, 'patch-A.MPQ', 'DBFilesClient', 'CreatureDisplayInfo.dbc'), 'rb').read()
    _, n, fields, size, _ = struct.unpack('<4s4I', d[:20])
    table = 20 + n * size
    text = lambda o: d[table + o:d.index(b'\0', table + o)].decode('latin1')
    out = []
    for i in range(n):
        row = struct.unpack_from('<%dI' % fields, d, 20 + i * size)
        if row[0] not in ids or row[1] not in models:
            continue
        model = re.sub(r'\.(mdx|mdl|m2)$', '', models[row[1]], flags=re.I)
        folder = model.rsplit(B, 1)[0]
        out.append((row[0], 'creature model ' + model, [model]))
        for o in row[6:9]:
            if o and text(o):
                out.append((row[0], 'creature texture ' + folder + B + text(o), [folder + B + text(o) + '.blp']))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--client', default='C:/Users/Medviten/Desktop/WowSquished-256-bit/Data')
    ap.add_argument('--common', default='D:/GitHub/WHE-common/patch-A.MPQ')
    ap.add_argument('--zeppelin', default='D:/GitHub/References/Zeppelin_patches/Data')
    ap.add_argument('--copy', action='store_true')
    a = ap.parse_args()
    local = {}
    for root in [a.common] + [os.path.join(a.client, p) for p in ('patch-C.MPQ', 'patch-B.MPQ', 'patch-A.MPQ')]:
        for k, v in tree(root).items():
            local.setdefault(k, v)
    archives = [Archive(p) for p in glob.glob(os.path.join(a.client, '*.[mM][pP][qQ]'))
                + glob.glob(os.path.join(a.client, 'enUS', '*.[mM][pP][qQ]')) if os.path.isfile(p)]
    work = tree(os.path.join(a.zeppelin, 'Work'))

    def present(path):
        if path.upper().endswith('.BLP'):
            return path.upper() in local or any(x.has(path) for x in archives)
        # a model: the path without extension, any race suffix (head models) or none
        stem = path.upper()
        return any(k.startswith(stem) and k.endswith('.M2') for k in local) or \
            any(x.has(path + suffix + '.m2') for x in archives for suffix in ('', '_HuM', '_HuF'))

    items = collections.defaultdict(list)
    for path in glob.glob(os.path.join(F013, 'sql', 'db-world', 'base', '*item_template*.sql')):
        for entry, name, display in re.findall(r"`entry` = (\d+),.*?`name` = '(.*?)',\s*\n.*?`displayid` = (\d+)",
                                               open(path, encoding='utf-8').read(), re.S):
            items[int(display)].append('%s %s' % (entry, name))
    sql = open(os.path.join(F013, 'dbc', '[AUTO,F-011]_itemdisplayinfo.sql'), encoding='utf-8').read()
    wanted = []
    for block in re.findall(r"INSERT INTO `itemdisplayinfo` SET(.*?);", sql, re.S):
        row = dict(re.findall(r"`(\w+)` = '?([^',\n]*)'?", block))
        wanted += [(int(row['id']), what, candidates) for what, candidates in needs(row)]
    wanted += creature_needs(a.client)
    copied, lost = 0, collections.defaultdict(list)
    for display, what, candidates in wanted:
        if True:
            if any(present(c) for c in candidates):
                continue
            source = next(((c, work[k]) for c in candidates for k in work
                           if k == c.upper() or (k.startswith(c.upper()) and k.endswith('.M2'))), None)
            if source and a.copy:
                client_path, real = source
                folder = os.path.join(a.common, os.path.dirname(client_path.replace(B, os.sep)))
                os.makedirs(folder, exist_ok=True)
                stem = os.path.splitext(real)[0]
                skins = glob.glob(stem + '*.skin') + glob.glob(stem + '*.SKIN') if real.upper().endswith('.M2') else []
                for f in [real] + skins:
                    shutil.copy2(f, os.path.join(folder, os.path.basename(f)))
                    copied += 1
            elif not source:
                lost[what].append(display)
    print('copied %d files' % copied if a.copy else '(dry run: --copy copies what Zeppelin has)')
    print('%d files nobody has:' % len(lost))
    for what, displays in sorted(lost.items()):
        print('  %-60s displays %s, items %s' % (what, displays[:4], [i for d in displays for i in items.get(d, [])][:3]))


if __name__ == '__main__':
    main()
