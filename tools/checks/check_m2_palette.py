#!/usr/bin/env python3
"""Check that the bone palette indices of a 3.3.5 character model's skin profiles agree with its vertices' bones.

The client skins a vertex through the .skin file's per-vertex palette indices (section bone combo + index), not the bone
ids in the .m2 vertex. A tool that changes a vertex's bones without rewriting those indices leaves it following the wrong
bones in game, while anything reading the .m2 alone (a renderer, a dump) looks fine.

usage: python -I check_m2_palette.py <model.m2>...   (exit status 1 if any vertex disagrees)"""
import os
import struct
import sys


def check(model):
    with open(model, 'rb') as f:
        data = f.read()
    nvert, overt = struct.unpack_from('<II', data, 0x3C)
    ncombo, ocombo = struct.unpack_from('<II', data, 0x78)
    combos = struct.unpack_from('<%dH' % ncombo, data, ocombo)
    base = os.path.splitext(model)[0]
    total = 0
    for profile in range(struct.unpack_from('<I', data, 0x44)[0]):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            skin = f.read()
        nlook, olook = struct.unpack_from('<II', skin, 0x04)
        lookup = struct.unpack_from('<%dH' % nlook, skin, olook)
        oprop = struct.unpack_from('<I', skin, 0x18)[0]
        nsec, osec = struct.unpack_from('<II', skin, 0x1C)
        for s in range(nsec):
            sid, _, vstart, vcount, _, icount, bones, index = struct.unpack_from('<8H', skin, osec + 48 * s)
            if not icount:
                continue
            palette = combos[index:index + bones]
            bad = 0
            for i in range(vstart, vstart + vcount):
                o = overt + 48 * lookup[i]
                indices = skin[oprop + 4 * i:oprop + 4 * i + 4]
                for w, b, p in zip(data[o + 12:o + 16], data[o + 16:o + 20], indices):
                    if w and (p >= len(palette) or palette[p] != b):
                        bad += 1
                        break
            if bad:
                print('%s: geoset %d section %d: %d of %d vertices follow other bones in game'
                      % (path, sid, s, bad, vcount))
                total += bad
    print('%s: %s' % (model, 'palette indices agree' if not total else '%d vertices disagree' % total))
    return total


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(1 if sum(check(m) for m in sys.argv[1:]) else 0)
