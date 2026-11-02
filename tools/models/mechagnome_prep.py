#!/usr/bin/env python3
"""Make F-040's native Mechagnome models work without the retail race pack's client code.

Those models expect the pack's helper to bind the eye colour to texture type 5, which nothing fills in this client, so the
eyes draw white. Point that slot at one of the race's eye textures instead. Also copies the default paint (type 8, set
through the skin rows' texture_2) that WHE-common lacked: without it the mechanical arms and legs are blank.

usage: mechagnome_prep.py [--common PATH] [--package PATH]
Patched in place and safe to rerun; restore with git in WHE-common to start over."""
import argparse, os, shutil, struct, sys

SLASH = chr(92)
PAINT = 'custom/mechagnome/character/mechagnome/male/mechagnomemale_paint_2628237.blp'


def eye_section_slots(base, types, lookup):
    """Texture slots of type 5 that batches of the always-on geoset 0 draw with: the eyeballs."""
    s = open(base + '00.skin', 'rb').read()
    (_, _, _, _, _, _, _, os_, nb, ob, _) = struct.unpack_from('<11I', s, 4)
    slots = set()
    for b in range(nb):
        field = struct.unpack_from('<BBHHHhHHHHHHH', s, ob + 24 * b)
        sid = struct.unpack_from('<H', s, os_ + 48 * field[3])[0]
        slot = lookup[field[9]]
        if sid == 0 and types[slot] == 5:
            slots.add(slot)
    return slots


def fix_model(common, sex):
    base = os.path.join(common, 'patch-A.MPQ', 'custom', 'mechagnome', 'native', sex, 'mechagnome' + sex)
    d = bytearray(open(base + '.m2', 'rb').read())
    nt, ot = struct.unpack_from('<II', d, 0x50)
    nl, ol = struct.unpack_from('<II', d, 0x80)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    lookup = struct.unpack_from('<%dH' % nl, d, ol)
    slots = eye_section_slots(base, types, lookup)
    if not slots:
        return 'already fixed'
    name = SLASH.join(('custom', 'mechagnome', 'native', sex, 'eyes0_0_0.blp')).encode('latin1') + b'\0'
    for slot in slots:
        at = ot + 16 * slot
        flags = struct.unpack_from('<I', d, at + 4)[0]
        struct.pack_into('<4I', d, at, 0, flags, len(name), len(d))
    d += name
    open(base + '.m2', 'wb').write(d)
    return 'eye slots %s' % sorted(slots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common')
    ap.add_argument('--package', default='D:/Downloads/Downloads/Races/Kalibros_Races_20261012')
    a = ap.parse_args()
    dst = os.path.join(a.common, 'patch-A.MPQ', *PAINT.split('/'))
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(a.package, *PAINT.split('/')), dst)
    for sex in ('male', 'female'):
        print(sex, fix_model(a.common, sex))


if __name__ == '__main__':
    sys.exit(main())
