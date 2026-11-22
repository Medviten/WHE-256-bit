#!/usr/bin/env python3
"""Scale the light intensities of a (3.3.5a, v264) M2 in place.

  python -I m2_scale_lights.py MODEL.m2 FACTOR [--ambient]

Multiplies every key of each light's diffuse intensity track (and with --ambient, its ambient intensity track) by
FACTOR. A glue scene's lights also light the character attached to it: F-141's UI_Gnome (Cataclysm's) lights its
character far brighter than the 3.3.5a client's other scenes.
"""
import argparse, struct

LIGHT_SIZE = 0x9C
TRACKS = 16          # the light's first track (ambient color), after type, bone and position
AMBIENT_INTENSITY = TRACKS + 20
DIFFUSE_INTENSITY = TRACKS + 60


def scale_track(d, at, factor):
    """Scales every float value of the M2Track at offset at (values: per-sequence arrays of floats)."""
    n, ofs = struct.unpack_from('<II', d, at + 12)
    count = 0
    for s in range(n):
        vn, vofs = struct.unpack_from('<II', d, ofs + 8 * s)
        for v in range(vn):
            struct.pack_into('<f', d, vofs + 4 * v, struct.unpack_from('<f', d, vofs + 4 * v)[0] * factor)
            count += 1
    return count


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('model')
    p.add_argument('factor', type=float)
    p.add_argument('--ambient', action='store_true')
    a = p.parse_args()
    d = bytearray(open(a.model, 'rb').read())
    assert d[:4] == b'MD20' and struct.unpack_from('<I', d, 4)[0] == 264, 'not a 3.3.5a (v264) M2'
    n, o = struct.unpack_from('<II', d, 0x108)
    keys = 0
    for i in range(n):
        b = o + i * LIGHT_SIZE
        keys += scale_track(d, b + DIFFUSE_INTENSITY, a.factor)
        if a.ambient:
            keys += scale_track(d, b + AMBIENT_INTENSITY, a.factor)
    open(a.model, 'wb').write(d)
    print('%s: %d lights, %d keys scaled by %g' % (a.model, n, keys, a.factor))


if __name__ == '__main__':
    main()
