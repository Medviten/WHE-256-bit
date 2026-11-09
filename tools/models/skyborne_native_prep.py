#!/usr/bin/env python3
"""Make the native Skyborne models (F-103/F-104, copied to WHE-common by tools/races/skyborne_native.py) selectable by the
stock geoset rules.

Kalibro's "expanded" models keep Forever's feathers as geoset groups 40-47: one group per Feather Color, with variant g
the feathers of the hair style whose geoset is g (Forever's Feathers choice names a skinned model of GeosetType 40 and
GeosetID g for each hair style). The client only manages geosets up to 2000, so all eight groups would always be drawn.
Here
- the feathers of Forever's first Feather Color (group 40, Seafoam) become geoset FEATHERED + g of group 0;
- each hair style's own submeshes (geoset g) are copied to FEATHERED + g as well, so CharHairGeosets variation
  "<style> with feathers" shows the style and its feathers, and the plain variation shows the style alone (Forever's
  default is no feathers);
- the other feather colours (groups 41-47) are parked at PARKED, which the client hides and nothing shows.
And the eyes: their batch has retail's two eye layers, both the skin row's eye texture (type 8), the second on UV set 1,
which maps onto the texture's glow dots. Its shader 0 makes 3.3.5 multiply the two (Combiners_Opaque_Opaque), so the
eyes come out dark and empty; EYE_SHADER (Combiners_Opaque_AddNA) adds the glow on top instead, as retail does.

usage: skyborne_native_prep.py [--common PATH]
Patched in place; already patched skins are left alone. skyborne_native.py runs it after copying the models."""
import argparse, os, struct

FEATHERED = 50
PARKED = 1999
SEX = ('male', 'female')
SECTION, BATCH = 48, 24
EYE_TEXTURE_TYPE = 8
EYE_SHADER = 0x07   # two layers: opaque, then add without alpha (CM2Shared::GetEffect)


def fix_eyes(model_path, skin_path):
    d = open(model_path, 'rb').read()
    nt, ot = struct.unpack_from('<II', d, 0x50)
    nl, ol = struct.unpack_from('<II', d, 0x80)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    lookup = struct.unpack_from('<%dH' % nl, d, ol)
    s = bytearray(open(skin_path, 'rb').read())
    nb, ob = struct.unpack_from('<II', s, 4 + 32)
    fixed = 0
    for b in range(nb):
        shader, = struct.unpack_from('<H', s, ob + BATCH * b + 2)
        count, combo = struct.unpack_from('<HH', s, ob + BATCH * b + 14)
        if count == 2 and shader == 0 and all(types[lookup[combo + k]] == EYE_TEXTURE_TYPE for k in range(2)):
            struct.pack_into('<H', s, ob + BATCH * b + 2, EYE_SHADER)
            fixed += 1
    if fixed:
        open(skin_path, 'wb').write(s)
    return '%d eye batches given the glow shader' % fixed


def prep(skin_path):
    s = bytearray(open(skin_path, 'rb').read())
    _, _, _, _, _, _, ns, os_, nb, ob, _ = struct.unpack_from('<11I', s, 4)
    sections = [bytearray(s[os_ + SECTION * i:os_ + SECTION * (i + 1)]) for i in range(ns)]
    batches = [bytearray(s[ob + BATCH * i:ob + BATCH * (i + 1)]) for i in range(nb)]
    ids = [struct.unpack_from('<H', x)[0] for x in sections]
    if any(FEATHERED < i < 100 for i in ids):
        return 'already prepared'
    feathers = {i - 4000 for i in ids if 4000 < i < 4100}
    added = parked = 0
    for index, sid in enumerate(ids):
        if 4000 < sid < 4100:
            struct.pack_into('<H', sections[index], 0, FEATHERED + sid - 4000)
        elif 4100 <= sid < 4800:
            struct.pack_into('<H', sections[index], 0, PARKED)
            parked += 1
    for index, sid in enumerate(ids):
        if 0 < sid < FEATHERED and sid in feathers:   # a hair style with feathers: its copy joins them
            copy = len(sections)
            section = bytearray(sections[index])
            struct.pack_into('<H', section, 0, FEATHERED + sid)
            sections.append(section)
            for b in list(batches):
                if struct.unpack_from('<H', b, 4)[0] == index:
                    b = bytearray(b)
                    struct.pack_into('<HH', b, 4, copy, copy)   # skin section index, geoset index
                    batches.append(b)
            added += 1
    # the grown arrays go to the end of the file
    os_, ob = len(s), len(s) + SECTION * len(sections)
    s += b''.join(sections) + b''.join(batches)
    struct.pack_into('<II', s, 4 + 24, len(sections), os_)
    struct.pack_into('<II', s, 4 + 32, len(batches), ob)
    open(skin_path, 'wb').write(s)
    return '%d feathered hair styles, %d feather submeshes of other colours parked, %d sections, %d batches' % (
        added, parked, len(sections), len(batches))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'WHE-common', 'patch-A.MPQ'))
    a = ap.parse_args()
    for sex in SEX:
        skin = os.path.join(a.common, 'custom', 'skyborne', 'native', sex, 'skyborne%s00.skin' % sex)
        print(sex, prep(skin))
        print(sex, fix_eyes(os.path.join(os.path.dirname(skin), 'skyborne%s.m2' % sex), skin))


if __name__ == '__main__':
    main()
