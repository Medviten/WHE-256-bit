"""Carry the shading across the female Vrykul PC model's hip seam, from the body into the robe (geoset 1302).

The robe's normals come from its own faces (m2_fix_winding.py), the body's from its faces and the legs': at the seam
they differ by a median of 39 degrees (up to 77), so light falls differently on either side and even a closed join
reads as a hard line. The robe's vertices on the seam take the body's normal there; those below blend from it to their
own over DEPTH, by direction around the hips. Run after m2_fix_winding.py, which would overwrite this.

usage: python -I vrykul_robe_normals.py <VrykulPCFemale.m2>   (in place)"""
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vrykul_robe_seam import BODY, ROBE, VERTEX_SIZE, geosets, key, load, position   # noqa: E402
from vrykul_robe_zip import seam_loop   # noqa: E402

DEPTH = 0.25    # how far below the seam the robe's normals still lean towards the body's


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    data, skin = load(model)
    geo = geosets(data, skin)
    overt = struct.unpack_from('<I', data, 0x40)[0]
    normal = lambda v: struct.unpack_from('<3f', data, overt + VERTEX_SIZE * v + 20)

    loop = seam_loop(data, geo)
    body_at = {}
    for t in geo[BODY]:
        for v in t:
            body_at.setdefault(key(position(data, v)), v)
    cx = sum(p[0] for p in loop) / len(loop)
    cy = sum(p[1] for p in loop) / len(loop)
    angle = lambda p: math.atan2(p[1] - cy, p[0] - cx)
    seam = sorted((angle(p), p[2]) + normal(body_at[p]) for p in loop)

    def seam_at(a):
        """Seam height and normal in direction a, between its two neighbouring points."""
        after = next((i for i, s in enumerate(seam) if s[0] >= a), 0)
        p, q = seam[after - 1], seam[after]
        span = (q[0] - p[0]) % (2 * math.pi) or 1.0
        f = ((a - p[0]) % (2 * math.pi)) / span
        return [p[i] + (q[i] - p[i]) * f for i in range(1, 5)]

    moved = 0
    for v in sorted({v for t in geo[ROBE] for v in t}):
        p = position(data, v)
        z, nx, ny, nz = seam_at(angle(p))
        t = max(z - p[2], 0.0) / DEPTH
        if t >= 1:
            continue
        keep = t * t * (3 - 2 * t)
        own = normal(v)
        mixed = [own[0] * keep + nx * (1 - keep), own[1] * keep + ny * (1 - keep), own[2] * keep + nz * (1 - keep)]
        length = math.sqrt(sum(c * c for c in mixed)) or 1.0
        struct.pack_into('<3f', data, overt + VERTEX_SIZE * v + 20, *(c / length for c in mixed))
        moved += 1

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: normals of %d robe vertices blended into the body\'s at the seam' % (model, moved))


if __name__ == '__main__':
    main()
