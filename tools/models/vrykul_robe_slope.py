"""Limit how fast the female Vrykul PC robe (geoset 1302) widens below the hip seam, in the stand pose.

Fitted from another model, the robe jumps out just below the seam: at the back about 9 cm in 5 cm of height, a "cliff"
above the buttocks. In each direction around the hips, going down from the seam, the robe's radius may grow by at most
SLOPE per unit of height. Vertices beyond that line are pulled in to it with a soft minimum, so no new crease forms where
the line lets go and the robe's own flare takes over. It works in the stand pose (frame 0), where the seam and the
upper robe have their real relation, and maps moved vertices back through their blended bone transforms. Nothing is
pushed out, and the strip of vrykul_robe_zip.py keeps its upper edge, which must stay on the seam.

Run after vrykul_robe_zip.py; m2_fix_winding.py afterwards recomputes the robe's normals.

usage: python -I vrykul_robe_slope.py <VrykulPCFemale.m2>   (in place)"""
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_pose import apply, blended, stand_matrices, unapply, vertex_skin   # noqa: E402
from vrykul_robe_seam import ROBE, VERTEX_SIZE, geosets, key, load, position   # noqa: E402
from vrykul_robe_zip import seam_loop   # noqa: E402

SLOPE = 0.5     # radius gained per unit of height going down from the seam
SOFT = 0.04     # width of the soft minimum


def soft_min(a, b):
    h = max(SOFT - abs(a - b), 0.0) / SOFT
    return min(a, b) - h * h * SOFT / 4


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    data, skin = load(model)
    geo = geosets(data, skin)
    overt = struct.unpack_from('<I', data, 0x40)[0]
    mats = stand_matrices(data)

    # the seam in the pose, through the robe strip's own copies of its vertices (same weights as the body's)
    loop = set(seam_loop(data, geo))
    robe = sorted({v for t in geo[ROBE] for v in t})
    transform = {v: blended(mats, *vertex_skin(data, v)) for v in robe}
    posed = {v: apply(transform[v], position(data, v)) for v in robe}
    on_seam = {key(position(data, v)): v for v in robe if key(position(data, v)) in loop}
    if len(on_seam) < 8:
        sys.exit('%s: run vrykul_robe_zip.py first: the robe has no vertices on the seam' % model)
    seam_posed = [posed[v] for v in on_seam.values()]
    cx = sum(p[0] for p in seam_posed) / len(seam_posed)
    cy = sum(p[1] for p in seam_posed) / len(seam_posed)
    polar = lambda p: (math.atan2(p[1] - cy, p[0] - cx), math.hypot(p[0] - cx, p[1] - cy))
    seam = sorted((polar(p)[0], polar(p)[1], p[2]) for p in seam_posed)

    def seam_at(a):
        after = next((i for i, s in enumerate(seam) if s[0] >= a), 0)
        p, q = seam[after - 1], seam[after]
        span = (q[0] - p[0]) % (2 * math.pi) or 1.0
        f = ((a - p[0]) % (2 * math.pi)) / span
        return p[1] + (q[1] - p[1]) * f, p[2] + (q[2] - p[2]) * f

    moved, most = 0, 0.0
    for v in robe:
        if key(position(data, v)) in loop:   # the strip's upper edge must stay on the seam, or the join opens
            continue
        q = posed[v]
        a, r = polar(q)
        seam_r, seam_z = seam_at(a)
        limit = seam_r + SLOPE * max(seam_z - q[2], 0.0)
        new_r = soft_min(r, limit)
        if new_r >= r - 1e-4 or r < 1e-6:
            continue
        s = new_r / r
        target = (cx + (q[0] - cx) * s, cy + (q[1] - cy) * s, q[2])
        struct.pack_into('<3f', data, overt + VERTEX_SIZE * v, *unapply(transform[v], target))
        moved += 1
        most = max(most, r - new_r)

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: %d robe vertices pulled in to the slope limit (at most %.3f)' % (model, moved, most))


if __name__ == '__main__':
    main()
