"""Taper the upper robe (geoset 1302) of the female Vrykul PC model so it flows from the waist instead of jutting out.

Right below the hip seam the robe is 6-9 cm wider than the hips at the sides and stays that wide down to the thighs,
so it reads as panniers sticking out on either side, with a step at the waist. For each direction around the hips the
robe's outer radius should instead run from the seam (where vrykul_robe_seam.py put its top edge) down to the skirt's
radius at SKIRT height. Every robe vertex between the two is scaled towards the robe's centre line by the factor that
brings the robe's outer radius there (smoothed over neighbouring heights and directions) down to that line, so folds
and layers keep their shape. Where the robe is narrower than the line just below the seam (at the back and lower
sides, where the hips end wider than the robe below them), it is eased out to it instead, letting go by EASE below
the seam, so it does not tuck in under the hips' edge. The top edge and the skirt below SKIRT stay where they are. Run after vrykul_robe_seam.py (and m2_subdivide_geoset.py if used); the robe's vertices must be
its own (they are in this model).

usage: python -I vrykul_robe_taper.py <VrykulPCFemale.m2>   (in place; its 00 skin defines the geosets)"""
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vrykul_robe_seam import BODY, LEGS, ROBE, VERTEX_SIZE, geosets, key, load, open_edge_vertices, position   # noqa: E402

SKIRT = 0.85          # height (model units) where the skirt's own width takes over
SEAM_MARGIN = 0.01    # the robe's outside at the seam: this far outside the hips
EASE = 0.35           # how far below the seam a robe narrower than the line is still eased out to it
ANGLE_BIN, HEIGHT_BIN = 15.0, 0.05


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    data, skin = load(model)
    data = bytearray(data)
    geo = geosets(data, skin)
    robe = sorted({v for t in geo[ROBE] for v in t})
    pos = {v: position(data, v) for v in robe}
    cx = sum(p[0] for p in pos.values()) / len(robe)
    cy = sum(p[1] for p in pos.values()) / len(robe)
    polar = lambda p: (math.degrees(math.atan2(p[1] - cy, p[0] - cx)) % 360, math.hypot(p[0] - cx, p[1] - cy))

    # the hip seam (as in vrykul_robe_seam.py): radius and height by direction
    legs = {key(position(data, v)) for t in geo[LEGS] for v in t}
    near_legs = lambda p: any(max(abs(p[i] - q[i]) for i in range(3)) < 0.01 for q in legs)
    seam = {key(position(data, v)) for v in open_edge_vertices(data, geo[BODY])}
    seam = sorted((polar(p)[0], polar(p)[1], p[2]) for p in seam if p[2] > 1.3 and near_legs(p))

    def around(points, angle):
        """Linear interpolation by direction between the two neighbouring (angle, ...) entries, wrapping round."""
        after = next((i for i, s in enumerate(points) if s[0] >= angle), 0)
        a, b = points[after - 1], points[after]
        span = (b[0] - a[0]) % 360 or 360.0
        f = ((angle - a[0]) % 360) / span
        return [x + (y - x) * f for x, y in zip(a[1:], b[1:])]

    # the robe's outer radius by (direction, height) bin, and the skirt's radius by direction
    outer = {}
    for v, p in pos.items():
        a, r = polar(p)
        b = (int(a // ANGLE_BIN), int(p[2] // HEIGHT_BIN))
        outer[b] = max(outer.get(b, 0.0), r)
    na = int(360 // ANGLE_BIN)

    def smooth_outer(a, z):
        ia, iz = int(a // ANGLE_BIN), int(z // HEIGHT_BIN)
        found = [outer[((ia + da) % na, iz + dz)] for da in (-1, 0, 1) for dz in (-1, 0, 1) if ((ia + da) % na, iz + dz) in outer]
        return max(found) if found else None

    skirt = []
    for ia in range(na):
        rs = [outer[(ia, iz)] for iz in range(int((SKIRT - 0.1) // HEIGHT_BIN), int((SKIRT + 0.05) // HEIGHT_BIN) + 1)
              if (ia, iz) in outer]
        if rs:
            skirt.append(((ia + 0.5) * ANGLE_BIN, max(rs)))

    vertices = struct.unpack_from('<I', data, 0x40)[0]
    moved, most = 0, 0.0
    for v, p in pos.items():
        a, r = polar(p)
        seam_r, seam_z = around(seam, a)
        if not SKIRT < p[2] < seam_z or r < 1e-6:
            continue
        top = seam_r + SEAM_MARGIN
        bottom = around(skirt, a)[0]
        f = (seam_z - p[2]) / (seam_z - SKIRT)
        target = top + (bottom - top) * f
        current = smooth_outer(a, p[2])
        if not current:
            continue
        if current <= target:
            # narrower than the line: just below the seam, ease out to it (else the robe tucks in under the hips'
            # edge, a shelf), letting go by EASE below the seam
            ease = (seam_z - p[2]) / EASE
            if ease >= 1:
                continue
            s = 1 + (target / current - 1) * (1 - ease * ease * (3 - 2 * ease))
        else:
            s = target / current
        new = (cx + (p[0] - cx) * s, cy + (p[1] - cy) * s, p[2])
        struct.pack_into('<3f', data, vertices + VERTEX_SIZE * v, *new)
        moved += 1
        most = max(most, r * (1 - s))

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: %d robe vertices pulled in or eased out (at most %.3f in)' % (model, moved, most))


if __name__ == '__main__':
    main()
