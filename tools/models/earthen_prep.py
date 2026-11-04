#!/usr/bin/env python3
"""Make F-038/F-039's native Earthen models work with the stock customization code.

Models (the 00.skin and the m2's texture table, rebuilt from the package each run):
- hair styles 4002-4011 become geosets 2-11 of group 0, which CharHairGeosets selects
- the client only manages geosets up to 2000, so everything above is always drawn. Variants nothing can select are parked in
  group 19 (hidden by SetGeometryVisible(0, 2000, 0), never shown again): feet 2002+, torso 2202, eye lenses 5102/5103 and all
  but the first variant of each gem group (42xx-47xx), which retail picks per body part
- the eye slot (type 5, which nothing fills) points at the race's first eye texture

The gems (those groups, 4105 and a small geoset 0 batch) are on texture type 9, which the client fills from the skin rows'
texture_3 (ReplaceExtraSkinTexture).

Textures, copied as earthendwarf_*.blp and shared by both genders through F-038/F-039's rows:
- hair colours from Kalibro's package (the male files)
- gem colours from --gems: retail's file ids in GEMS order, from https://wago.tools/api/casc/<id>?download as gem_<id>.blp

usage: earthen_prep.py [--common PATH] [--package PATH] [--gems PATH]"""
import argparse, glob, os, shutil, struct, sys

SLASH = chr(92)
PARKED = 1999
HAIR = range(4002, 4012)
# Red, Yellow, Purple, Blue, White, Brown, Green, Orange, Teal, Grey, Cream, Lime, Rose, Indigo
GEMS = (5547351, 5547352, 5547353, 5547354, 5547355, 5547356, 5733886, 5733887, 5733888, 5733889, 5733890, 5733891, 5733892, 5733893)
PARK = set(range(2002, 2009)) | {2202, 5102, 5103} | {sid for group in range(4200, 4800, 100) for sid in range(group + 2, group + 100)}


def fix_skin(data):
    s = bytearray(data)
    (_, _, _, _, _, _, ns, os_, _, _, _) = struct.unpack_from('<11I', s, 4)
    changed = 0
    for i in range(ns):
        at = os_ + 48 * i
        sid = struct.unpack_from('<H', s, at)[0]
        new = sid - 4000 if sid in HAIR else (PARKED if sid in PARK else sid)
        if new != sid:
            struct.pack_into('<H', s, at, new)
            changed += 1
    return s, changed


def fix_model(common, package, sex):
    rel = os.path.join('custom', 'earthen', 'native', sex, 'earthendwarf' + sex)
    src = os.path.join(package, rel)
    dst = os.path.join(common, 'patch-A.MPQ', rel)
    d = bytearray(open(src + '.m2', 'rb').read())
    s, changed = fix_skin(open(src + '00.skin', 'rb').read())
    nt, ot = struct.unpack_from('<II', d, 0x50)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    slots = [i for i, t in enumerate(types) if t == 5]
    name = SLASH.join(('custom', 'earthen', 'native', sex, 'eyes0_1.blp')).encode('latin1') + b'\0'
    for slot in slots:
        at = ot + 16 * slot
        flags = struct.unpack_from('<I', d, at + 4)[0]
        struct.pack_into('<4I', d, at, 0, flags, len(name), len(d))
    d += name
    open(dst + '.m2', 'wb').write(d)
    open(dst + '00.skin', 'wb').write(s)
    return 'sections changed %d, eye slots %s' % (changed, slots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common')
    ap.add_argument('--package', default='D:/Downloads/Downloads/Races/Kalibros_Races_20261012')
    ap.add_argument('--gems', default='D:/wow-scratch/earthen_gems')
    a = ap.parse_args()
    src = os.path.join(a.package, 'custom', 'earthen', 'character', 'earthendwarf')
    dst = os.path.join(a.common, 'patch-A.MPQ', 'custom', 'earthen', 'character', 'earthendwarf')
    hair = sorted(glob.glob(os.path.join(src, 'earthendwarfmale_hair_color_*.blp')))
    for path in hair:
        shutil.copy2(path, os.path.join(dst, os.path.basename(path).replace('earthendwarfmale_', 'earthendwarf_')))
    for gem in GEMS:
        shutil.copy2(os.path.join(a.gems, 'gem_%d.blp' % gem), os.path.join(dst, 'earthendwarf_gem_color_%d.blp' % gem))
    print('hair colours:', len(hair), 'gem colours:', len(GEMS))
    for sex in ('male', 'female'):
        print(sex, fix_model(a.common, a.package, sex))


if __name__ == '__main__':
    sys.exit(main())
