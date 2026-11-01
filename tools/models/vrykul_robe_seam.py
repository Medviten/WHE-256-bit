"""Stitch the female Vrykul PC model's robe (geoset 1302) to its body at the hip seam, so the two run on seamlessly.

The body (geoset 0) ends at a hip seam that only the legs (1301) close; a robe hides the legs and should continue the
body from there, like stock robes do. This robe's top edge (of both its layers) sits a few centimetres off the seam,
with texture coordinates shifted sideways against the body's (up to 0.07 in u: the robe's pattern breaks at the
waist) and other bone weights (the edges drift apart when she moves). Each top-edge vertex is moved onto the seam at
the same angle around the hips (interpolated between seam vertices), then put a little below it (OUTSIDE,
ABOVE; vrykul_robe_zip.py closes the band between the two with a watertight strip), and takes the seam's texture coordinates there
and the nearest seam vertex's bone weights. The robe's rows above FADE are reshaped with the edge, in each direction,
so they stay in order below it. The sideways texture shift fades out down the robe (to nothing at FADE
height), so the pattern bends smoothly into the robe's own mapping instead of breaking. Bone weights of the robe
just below the seam blend towards the seam's (fading out over WEIGHT_DEPTH), so its upper rows move with the hips' edge.
The texture's columns ease over COLUMN_DEPTH from the body's direction into the robe's fan, so patterns do not kink.

usage: python -I vrykul_robe_seam.py <VrykulPCFemale.m2>   (in place; its 00 skin defines the geosets)"""
import math
import os
import struct
import sys
from collections import Counter

ROBE, LEGS, BODY = 1302, 1301, 0
FADE = 0.9      # height below which the robe keeps its own texture mapping
COLUMN_DEPTH = 0.45   # how far below the seam the texture columns ease from the body's direction into the robe's fan
WEIGHT_DEPTH = 0.3   # how far below the seam the robe's bone weights blend towards the seam's
OUTSIDE, ABOVE = 0.005, -0.015  # the top edge ends up this far outside and above the seam (so just below it);
                                # vrykul_robe_zip.py then closes the small band between the two
VERTEX_SIZE = 48


def load(model):
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    with open(os.path.splitext(model)[0] + '00.skin', 'rb') as f:
        skin = f.read()
    return data, skin


def geosets(data, skin):
    """{geoset id: [(model vertex index a, b, c) per triangle]}"""
    nidx, oidx = struct.unpack_from('<II', skin, 0x04)
    ntri, otri = struct.unpack_from('<II', skin, 0x0C)
    nsec, osec = struct.unpack_from('<II', skin, 0x1C)
    lookup = struct.unpack_from('<%dH' % nidx, skin, oidx)
    triangles = struct.unpack_from('<%dH' % ntri, skin, otri)
    out = {}
    for i in range(nsec):
        sid, level, _, _, start, count = struct.unpack_from('<6H', skin, osec + 48 * i)
        start |= level << 16
        out.setdefault(sid, []).extend(tuple(lookup[triangles[t + j]] for j in range(3))
                                       for t in range(start, start + count, 3))
    return out


def position(data, v):
    return struct.unpack_from('<3f', data, struct.unpack_from('<I', data, 0x40)[0] + VERTEX_SIZE * v)


def key(p):
    return tuple(round(c, 3) for c in p)


def open_edge_vertices(data, triangles):
    """Model vertices on edges used by one triangle (vertices welded by position, as seams split them)."""
    edges = Counter()
    for t in triangles:
        k = [key(position(data, v)) for v in t]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            if k[a] != k[b]:
                edges[frozenset((k[a], k[b]))] += 1
    open_points = {p for e, n in edges.items() if n == 1 for p in e}
    return {v for t in triangles for v in t if key(position(data, v)) in open_points}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    data, skin = load(model)
    geo = geosets(data, skin)
    vertices = struct.unpack_from('<I', data, 0x40)[0]
    uv = lambda v: struct.unpack_from('<2f', data, vertices + VERTEX_SIZE * v + 32)

    # the seam: body open-edge vertices that the legs share, above the hanging hands
    legs = {key(position(data, v)) for t in geo[LEGS] for v in t}
    near_legs = lambda p: any(max(abs(p[i] - q[i]) for i in range(3)) < 0.01 for q in legs)
    seam_vertices = [v for v in open_edge_vertices(data, geo[BODY])
                     if position(data, v)[2] > 1.3 and near_legs(key(position(data, v)))]
    robe_top = sorted(v for v in open_edge_vertices(data, geo[ROBE]) if position(data, v)[2] > 1.2)
    if not seam_vertices or not robe_top:
        sys.exit('%s: no seam or robe top edge found' % model)
    tops = [position(data, v) for v in robe_top]
    cx = sum(p[0] for p in tops) / len(tops)
    cy = sum(p[1] for p in tops) / len(tops)
    angle = lambda p: math.atan2(p[1] - cy, p[0] - cx)

    # (angle, radius, height, u, v, vertex) along the seam, one entry per position
    seam = {}
    for v in seam_vertices:
        p = position(data, v)
        seam.setdefault(key(p), (angle(p), math.hypot(p[0] - cx, p[1] - cy), p[2]) + uv(v) + (v,))
    seam = sorted(seam.values())

    def around(points, a, fields):
        """Interpolates the given fields of (angle, ...) entries at angle a, between the two neighbouring entries."""
        after = next((i for i, s in enumerate(points) if s[0] >= a), 0)
        p, q = points[after - 1], points[after]
        span = (q[0] - p[0]) % (2 * math.pi) or 1.0
        f = ((a - p[0]) % (2 * math.pi)) / span
        return [p[i] + (q[i] - p[i]) * f for i in fields], (p if f < 0.5 else q)

    # the top edge onto the seam, with its texture coordinates and the nearest seam vertex's weights
    shifts = []
    old_top = []
    for v in robe_top:
        p = position(data, v)
        a = angle(p)
        (radius, height, u, w), nearest = around(seam, a, (1, 2, 3, 4))
        shifts.append((a, u - uv(v)[0]))
        old_top.append((a, math.hypot(p[0] - cx, p[1] - cy), p[2]))
        o = vertices + VERTEX_SIZE * v
        radius += OUTSIDE
        struct.pack_into('<3f', data, o, cx + radius * math.cos(a), cy + radius * math.sin(a), height + ABOVE)
        struct.pack_into('<2f', data, o + 32, u, w)
        so = vertices + VERTEX_SIZE * nearest[5]
        data[o + 12:o + 20] = data[so + 12:so + 20]
    shifts.sort()
    old_top.sort()

    # the robe below: its upper part reshaped along with the top edge (the seam's height varies around the hips, so
    # moving only the edge would leave rows above it, folding the robe over itself and through the body), and the
    # sideways texture shift fading out towards FADE
    top_set = set(robe_top)
    faded = 0
    for v in sorted({v for t in geo[ROBE] for v in t} - top_set):
        p = position(data, v)
        a = angle(p)
        (seam_radius, seam_height), _ = around(seam, a, (1, 2))
        (old_radius, old_height), _ = around(old_top, a, (1, 2))
        if p[2] > FADE and old_height > FADE:
            t = min((p[2] - FADE) / (old_height - FADE), 1.0)   # 0 at FADE, 1 at the old top edge
            z = FADE + t * (seam_height + ABOVE - FADE)
            r = math.hypot(p[0] - cx, p[1] - cy) * (1 + ((seam_radius + OUTSIDE) / old_radius - 1) * t)
            p = (cx + r * math.cos(a), cy + r * math.sin(a), z)
            struct.pack_into('<3f', data, vertices + VERTEX_SIZE * v, *p)
        f = (p[2] - FADE) / (seam_height - FADE)
        if f <= 0:
            continue
        (shift, ), _ = around(shifts, a, (1,))
        (seam_u,), _ = around(seam, a, (3,))
        u, w = uv(v)
        u += shift * min(f, 1.0)
        # just below the seam the texture's columns carry on in the body's direction (the seam's column in this
        # direction) and only gradually fan out with the flare: a sudden fan kinks any pattern crossing the seam
        t = min(max(seam_height - p[2], 0.0) / COLUMN_DEPTH, 1.0)
        u += (seam_u - u) * (1 - t * t * (3 - 2 * t))
        struct.pack_into('<2f', data, vertices + VERTEX_SIZE * v + 32, u, w)
        faded += 1
        # bone weights: towards the seam's (the pelvis) just below it, so the robe's upper rows move with the hips'
        # edge instead of swinging away from it with the thighs in the stand pose and other animations
        g = 1 - (seam_height - p[2]) / WEIGHT_DEPTH
        if g <= 0:
            continue
        _, nearest = around(seam, a, (1,))
        o, so = vertices + VERTEX_SIZE * v, vertices + VERTEX_SIZE * nearest[5]
        mixed = {}
        for wt, b in zip(data[o + 12:o + 16], data[o + 16:o + 20]):
            if wt:
                mixed[b] = mixed.get(b, 0) + wt * (1 - min(g, 1.0))
        for wt, b in zip(data[so + 12:so + 16], data[so + 16:so + 20]):
            if wt:
                mixed[b] = mixed.get(b, 0) + wt * min(g, 1.0)
        top4 = sorted(mixed.items(), key=lambda item: -item[1])[:4]
        total = sum(wt for _, wt in top4)
        weights = [int(round(wt * 255 / total)) for _, wt in top4]
        weights[0] += 255 - sum(weights)
        data[o + 12:o + 16] = bytes(weights + [0] * (4 - len(weights)))
        data[o + 16:o + 20] = bytes([b for b, _ in top4] + [0] * (4 - len(top4)))

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: %d robe top-edge vertices stitched to the hip seam (%d seam points), texture shift faded over %d more'
          % (model, len(robe_top), len(seam), faded))


if __name__ == '__main__':
    main()
