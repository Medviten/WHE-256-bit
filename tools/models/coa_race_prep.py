"""Copy the CoA Custom 1.9 race models into a client folder and make them WHE player models without
EsteriaAppearance.dll (see tools/races/coa_races.py for what is kept of the DLL's customization).

For each model of a race (patched in place in the output, no layout change except appended texture names):
- texture type 11 (the catalog's option 0, skin colour) becomes type 1: the composited body, i.e. the CharSections
  skin row's texture_1 (the race must be in the client's creatureSkinRaces, which keeps it whole)
- a second option 0 texture (type 12: Banshee face, Faceless glow) becomes type 8: the skin row's texture_2
- textures of the other options become type 0 with the option's first choice as file name
- geosets above 2000 (the character code only hides 0-2000) that the catalog does not keep move to geoset 1999,
  which is never shown; so do geosets drawn only with creature textures nobody fills (Kyrian/Venthyr armour,
  200xx and 1302: type 15, the DLL's baked armour)

usage: python -I coa_race_prep.py <CoA client Work folder> <CoA client_root folder> <output folder> [race key ...]"""
import os
import shutil
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'races'))
import coa_races   # noqa: E402

TEXTURES = 0x50            # M2Array<M2Texture>, 16 bytes each
REPLACEABLE_LOOKUP = 0x68  # M2Array<int16>, indexed by texture type
TEXTURE_LOOKUP = 0x80      # M2Array<int16>, texture combos
NUM_SKINS = 0x44


def patch_model(data, look):
    b = bytearray(data)
    if b[:4] != b'MD20' or struct.unpack_from('<I', b, 4)[0] != 264:
        raise ValueError('not a 3.3.5 (version 264) M2')
    count, offset = struct.unpack_from('<II', b, TEXTURES)
    lcount, loffset = struct.unpack_from('<II', b, REPLACEABLE_LOOKUP)
    new_type = {look.skin_types[0]: 1}
    if len(look.skin_types) > 1:
        new_type[look.skin_types[1]] = 8
    lookup, changes, appended = {}, [], bytearray()
    for i in range(count):
        o = offset + 16 * i
        typ = struct.unpack_from('<I', b, o)[0]
        if typ in new_type:
            struct.pack_into('<I', b, o, new_type[typ])
            lookup.setdefault(new_type[typ], i)
            lookup[typ] = -1
            changes.append('texture %d: type %d -> %d' % (i, typ, new_type[typ]))
        elif typ in look.fixed:
            name = look.fixed[typ].encode('latin1') + b'\0'
            name_offset = len(b) + len(appended)
            appended += name
            struct.pack_into('<IIII', b, o, 0, struct.unpack_from('<I', b, o + 4)[0], len(name), name_offset)
            lookup[typ] = -1
            changes.append('texture %d: type %d -> %s' % (i, typ, look.fixed[typ]))
    for typ, index in lookup.items():
        if typ >= lcount:
            if index >= 0:
                raise ValueError('replaceable texture lookup has %d entries, type %d needs more' % (lcount, typ))
            continue   # the type had no lookup entry to clear
        struct.pack_into('<h', b, loffset + 2 * typ, index)
    return bytes(b + appended), changes


def texture_types(model):
    count, offset = struct.unpack_from('<II', model, TEXTURES)
    types = [struct.unpack_from('<I', model, offset + 16 * i)[0] for i in range(count)]
    lcount, loffset = struct.unpack_from('<II', model, TEXTURE_LOOKUP)
    return [types[struct.unpack_from('<h', model, loffset + 2 * i)[0]] for i in range(lcount)]


def patch_skin(data, look, model):
    """Hide the geosets the catalog does not keep and those drawn only with creature textures nobody fills (the DLL's
    baked armour, type 15); report the texture types the remaining geosets above 2000 use."""
    b = bytearray(data)
    if b[:4] != b'SKIN':
        raise ValueError('not a 3.3.5 skin')
    count, offset = struct.unpack_from('<II', b, 0x1C)
    ids = [struct.unpack_from('<H', b, offset + 48 * i)[0] for i in range(count)]
    combo_types = texture_types(model)
    bcount, boffset = struct.unpack_from('<II', b, 0x24)
    types_of = {}
    for i in range(bcount):
        section, combo = struct.unpack_from('<H', b, boffset + 24 * i + 4)[0], struct.unpack_from('<H', b, boffset + 24 * i + 16)[0]
        types_of.setdefault(ids[section], set()).add(combo_types[combo])
    unfilled = lambda g: types_of.get(g) and all(t >= 11 for t in types_of[g])
    hidden = []
    for i, g in enumerate(ids):
        if g == 0 or g in look.keep:
            continue
        if (g > 2000 and g // 100 in look.driven) or unfilled(g):
            struct.pack_into('<H', b, offset + 48 * i, coa_races.HIDDEN_GEOSET)
            hidden.append(g)
    shown = sorted({g for g in ids if g not in hidden and (g == 0 or g > 2000)})
    used = sorted({t for g in shown for t in types_of.get(g, ())})
    return bytes(b), sorted(set(hidden)), shown, used


def prepare(work, catalogs, out, race):
    key, catalog_name, folders, male, female = race[0], race[10], race[12], race[13], race[14]
    for folder in folders:
        src, dst = os.path.join(work, folder), os.path.join(out, folder)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    looks = coa_races.catalog(os.path.join(catalogs, 'Esteria%s.bin' % catalog_name))
    models = [(0, male)] + ([(1, female)] if female and female != male else [])
    for gender, path in models:
        look = looks.get(gender, looks[0])
        m2 = os.path.join(out, *path.split('\\'))
        model, changes = patch_model(open(m2, 'rb').read(), look)
        open(m2, 'wb').write(model)
        print('%s %s: %s' % (key, path, '; '.join(changes) or 'no texture changes'))
        for n in range(struct.unpack_from('<I', model, NUM_SKINS)[0]):
            skin_path = m2[:-3] + '%02d.skin' % n
            if not os.path.exists(skin_path):
                continue
            skin, hidden, shown, used = patch_skin(open(skin_path, 'rb').read(), look, model)
            open(skin_path, 'wb').write(skin)
            if n == 0:
                print('    hidden geosets %s; always shown %s; texture types drawn %s' % (hidden, shown, used))
                missing = [t for t in used if t >= 11]
                if missing:
                    print('    WARNING: shown batches use replaceable types without a texture: %s' % missing)


if __name__ == '__main__':
    work, catalogs, out = sys.argv[1:4]
    wanted = set(sys.argv[4:])
    for race in coa_races.RACES + [coa_races.CENTAUR]:
        if not wanted or race[0] in wanted:
            prepare(work, catalogs, out, race)
