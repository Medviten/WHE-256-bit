#!/usr/bin/env python3
"""Make a WMO's indoor groups that no portal leads into exterior groups, so the client draws them.

  python -I wmo_portalless_interiors.py ROOT.wmo OUT_DIR

An indoor group is only drawn through its portals: from outside it is seen through the portal in its doorway, and from
inside the rest of the WMO is seen the same way. Open Azeroth's Gilneas_PrisonQuarter_Entrance adds five shop interiors
to Cataclysm's WMO, but only two got portals (and one portal is empty): the other three draw nothing from outside,
their doors are invisible but solid, and looking through them shows the sky where the walls behind should be.

Each such group loses its indoor flag (0x2000) and gets the exterior one (0x8), in the root's MOGI and in its group
file's MOGP. Its vertex colours (MOCV), which light an indoor group but are added on top of the sun for an exterior one,
are set to black, keeping alpha (see wmo_mop_fixups.py). The root and the changed group files are written to OUT_DIR
under their own names; groups with portals are left alone. Safe to rerun on its own output."""
import os, struct, sys

INDOOR, EXTERIOR, HAS_MOCV = 0x2000, 0x8, 0x4


def chunks(d, start, end):
    p = start
    while p + 8 <= end:
        t, n = d[p:p + 4], struct.unpack_from('<I', d, p + 4)[0]
        yield t, p, n
        p += 8 + n


def find(d, tag):
    for t, p, n in chunks(d, 0, len(d)):
        if t == tag:
            return p + 8, n
    raise SystemExit('no %s chunk' % tag[::-1].decode())


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    root, out = sys.argv[1], sys.argv[2]
    d = bytearray(open(root, 'rb').read())
    ngroups = struct.unpack_from('<I', d, find(d, b'DHOM')[0] + 4)[0]
    refs_at, refs_n = find(d, b'RPOM')
    with_portal = {struct.unpack_from('<H', d, refs_at + i * 8 + 2)[0] for i in range(refs_n // 8)}
    gi = find(d, b'IGOM')[0]
    stem = os.path.splitext(os.path.basename(root))[0]
    folder = os.path.dirname(root)
    os.makedirs(out, exist_ok=True)
    fixed = []
    for g in range(ngroups):
        flags = struct.unpack_from('<I', d, gi + g * 32)[0]
        if not flags & INDOOR or g in with_portal:
            continue
        struct.pack_into('<I', d, gi + g * 32, (flags & ~INDOOR) | EXTERIOR)
        name = '%s_%03d%s' % (stem, g, os.path.splitext(root)[1])
        gd = bytearray(open(os.path.join(folder, name), 'rb').read())
        mogp, size = find(gd, b'PGOM')
        gflags = struct.unpack_from('<I', gd, mogp + 8)[0]
        struct.pack_into('<I', gd, mogp + 8, (gflags & ~INDOOR) | EXTERIOR)
        if gflags & HAS_MOCV:
            for t, p, n in chunks(gd, mogp + 0x44, mogp + size):
                if t == b'VCOM':
                    for i in range(n // 4):
                        struct.pack_into('<3B', gd, p + 8 + i * 4, 0, 0, 0)
        open(os.path.join(out, name), 'wb').write(gd)
        fixed.append(g)
    open(os.path.join(out, os.path.basename(root)), 'wb').write(d)
    print('%s: %d indoor groups without a portal made exterior: %s' % (os.path.basename(root), len(fixed), fixed))


if __name__ == '__main__':
    main()
