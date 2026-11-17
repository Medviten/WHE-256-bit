#!/usr/bin/env python3
"""Fix converted MoP WMO groups for the 3.3.5a client: near-white exterior vertex colours and river-typed WMO water.

  python -I wmo_mop_fixups.py FOLDER_OR_GROUP_WMO...

The client adds an exterior group's vertex colours on top of its sun lighting, so they are stored near black (F-134's
WMOs average 0-60). A few MoP groups carry near-white ones (the Singing Pools' tu_boardwalk_004: 252), which
washes their textures out to a glow (the red footbridge turned pink). Groups whose average colour is above 128 get
black colours; alpha, which can blend texture layers, is kept.

Groups with their own water (MLIQ) whose liquid is a river type (1 Water, 5 Slow Water) get 13, WMO Water: stock WMO
pools use it, while river water is shaded by a depth the WMO liquid doesn't have (the Singing Pools'
pa_pools_of_sight came out purple). Safe to rerun."""
import glob, os, struct, sys

LIMIT = 128
RIVER, WMO_WATER = (1, 5), 13


def chunks(d, start, end):
    p = start
    while p + 8 <= end:
        t, n = d[p:p + 4], struct.unpack_from('<I', d, p + 4)[0]
        yield t, p, n
        p += 8 + n


def patch(path):
    d = bytearray(open(path, 'rb').read())
    changed = 0
    for t, p, n in chunks(d, 0, len(d)):
        if t != b'PGOM':
            continue
        if struct.unpack_from('<I', d, p + 8 + 0x34)[0] in RIVER and b'QILM' in d[p + 8 + 0x44:p + 8 + n]:
            struct.pack_into('<I', d, p + 8 + 0x34, WMO_WATER)
            changed += 1
        if not struct.unpack_from('<I', d, p + 16)[0] & 0x8:
            continue
        for st, sp, sn in chunks(d, p + 8 + 0x44, p + 8 + n):
            if st != b'VCOM':
                continue
            c = d[sp + 8:sp + 8 + sn]
            if sn >= 4 and (sum(c[0::4]) + sum(c[1::4]) + sum(c[2::4])) / (3 * (sn // 4)) > LIMIT:
                for i in range(sp + 8, sp + 8 + sn, 4):
                    d[i:i + 3] = b'\0\0\0'
                changed += 1
    if changed:
        open(path, 'wb').write(d)
    return changed


def main():
    files = []
    for x in sys.argv[1:]:
        files += glob.glob(os.path.join(x, '**', '*_[0-9][0-9][0-9].wmo'), recursive=True) if os.path.isdir(x) else [x]
    n = sum(patch(f) for f in files)
    print('fixed %d vertex colour sets and WMO waters in %d group files' % (n, len(files)))


if __name__ == '__main__':
    main()
