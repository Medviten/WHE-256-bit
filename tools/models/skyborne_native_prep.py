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

usage: skyborne_native_prep.py [--common PATH]
Patched in place; already patched skins are left alone. skyborne_native.py runs it after copying the models."""
import argparse, os, struct

FEATHERED = 50
PARKED = 1999
SEX = ('male', 'female')
SECTION, BATCH = 48, 24


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


if __name__ == '__main__':
    main()
