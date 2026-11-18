#!/usr/bin/env python3
"""Remove the invisible collision that seals a WMO doorway: collision-only triangles inside a box are collapsed.

  python -I wmo_open_doorway.py GROUP.wmo X0 Y0 Z0 X1 Y1 Z1 [--write]

Cataclysm's Gilneas WMOs seal their shop doors with a plane of collision-only triangles (MOPY flags 0x08, material
255: never drawn). Open Azeroth added interiors behind some of those doors but kept the seals, so the doors can't be
walked through. Every collision-only triangle of the group whose three vertices lie in the box (the group's own
coordinates, as wmo tools report them) is listed; with --write its three indices are pointed at its first vertex, a
zero-area triangle nothing collides with, leaving the BSP and every other chunk as they are. Safe to rerun."""
import struct, sys

COLLISION_ONLY = (0x08, 255)


def chunks(d, start, end):
    p = start
    while p + 8 <= end:
        t, n = d[p:p + 4], struct.unpack_from('<I', d, p + 4)[0]
        yield t, p + 8, n
        p += 8 + n


def main():
    args = [a for a in sys.argv[1:] if a != '--write']
    if len(args) != 7:
        raise SystemExit(__doc__)
    path, box = args[0], [float(a) for a in args[1:]]
    lo, hi = box[:3], box[3:]
    d = bytearray(open(path, 'rb').read())
    mogp = next((p, n) for t, p, n in chunks(d, 0, len(d)) if t == b'PGOM')
    sub = {t[::-1].decode(): (p, n) for t, p, n in chunks(d, mogp[0] + 0x44, mogp[0] + mogp[1])}
    verts = [struct.unpack_from('<3f', d, sub['MOVT'][0] + i * 12) for i in range(sub['MOVT'][1] // 12)]
    movi = sub['MOVI'][0]
    found = []
    for t in range(sub['MOVI'][1] // 6):
        if struct.unpack_from('<BB', d, sub['MOPY'][0] + t * 2) != COLLISION_ONLY:
            continue
        ids = struct.unpack_from('<3H', d, movi + t * 6)
        if ids[0] == ids[1] == ids[2]:
            continue
        if all(lo[a] <= verts[i][a] <= hi[a] for i in ids for a in range(3)):
            found.append(t)
            if '--write' in sys.argv:
                struct.pack_into('<3H', d, movi + t * 6, ids[0], ids[0], ids[0])
    if '--write' in sys.argv and found:
        open(path, 'wb').write(d)
    print('%s: %d collision-only triangles %s %s' % (path, len(found), 'removed' if '--write' in sys.argv else 'in the box',
                                                      found))


if __name__ == '__main__':
    main()
