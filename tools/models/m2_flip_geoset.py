"""Turn geosets of a 3.3.5 character model inside out: reverse the winding of all their triangles (in every skin
profile) and flip their vertices' normals.

For two-layer cloth (an outer layer facing out and a lining facing in) whose layers were converted the wrong way round
(the lining outside), as in the female Vrykul PC sleeves (802, 803): reversing both layers makes the outside one face
out and the inside one in. The geosets' vertices must not be used by other geosets (their normals flip).

usage: python -I m2_flip_geoset.py <model.m2> <geoset> [geoset...]   (in place)"""
import os
import struct
import sys

VERTEX_SIZE, SECTION_SIZE = 48, 48


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    model, wanted = sys.argv[1], {int(g) for g in sys.argv[2:]}
    base = os.path.splitext(model)[0]
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    overt = struct.unpack_from('<I', data, 0x40)[0]
    profiles = struct.unpack_from('<I', data, 0x44)[0]

    mine, others = set(), set()
    for profile in range(profiles):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            skin = bytearray(f.read())
        nlook, olook = struct.unpack_from('<II', skin, 0x04)
        lookup = struct.unpack_from('<%dH' % nlook, skin, olook)
        ntri, otri = struct.unpack_from('<II', skin, 0x0C)
        nsec, osec = struct.unpack_from('<II', skin, 0x1C)
        reversed_ = 0
        for s in range(nsec):
            sid, level, _, _, start, count = struct.unpack_from('<6H', skin, osec + SECTION_SIZE * s)
            start |= level << 16
            corners = {lookup[struct.unpack_from('<H', skin, otri + 2 * t)[0]] for t in range(start, start + count)}
            if sid not in wanted:
                others |= corners
                continue
            mine |= corners
            for t in range(start, start + count, 3):
                a, b = struct.unpack_from('<HH', skin, otri + 2 * (t + 1))
                struct.pack_into('<HH', skin, otri + 2 * (t + 1), b, a)
                reversed_ += 1
        if profile == 0 and mine & others:
            sys.exit('%s: geosets %s share %d vertices with other geosets' % (model, sorted(wanted), len(mine & others)))
        with open(path, 'wb') as f:
            f.write(skin)
        print('%s: %d triangles reversed' % (path, reversed_))

    for v in mine:
        o = overt + VERTEX_SIZE * v + 20
        struct.pack_into('<3f', data, o, *(-c for c in struct.unpack_from('<3f', data, o)))
    with open(model, 'wb') as f:
        f.write(data)
    print('%s: normals of %d vertices of geosets %s flipped' % (model, len(mine), sorted(wanted)))


if __name__ == '__main__':
    main()
