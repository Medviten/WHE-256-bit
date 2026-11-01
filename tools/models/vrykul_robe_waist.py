"""Make the female Vrykul PC robe (geoset 1302) start at the waist and run smoothly over the hips.

The robe begins at the hip seam, below the widest part of the hips and buttocks, which bulge out over its top edge:
a ledge at the waist. Stock robes start at the waist (and a robe paints the hips in its own texture anyway). This
stretches only the robe's top band, above LOWER, upwards so its top edge sits at WAIST, and gives the band a smooth
outline: in each direction and at each height its outer radius becomes the larger of
  - a blend from the robe's own outer radius at LOWER up to the body's at the waist, and
  - a smoothed outline of the body there (widened over neighbouring directions and heights, then blurred) plus MARGIN,
so it rises from the skirt, over the hips, to the waist without steps. Band vertices are scaled towards the robe's
centre line in proportion (each layer's own outline, smoothed the same way: the robe is an outer layer and a lining
that cross each other), so folds keep their shape. The robe below LOWER keeps its shape.

The robe only follows the pelvis and thighs, while the waist follows the lower spine, which leans the belly about 12 cm
forward in the stand pose. Band vertices therefore blend their bone weights towards those of the nearest body vertex,
from none at LOWER to all at the waist (the robe's bone palette, the same in every skin profile, gets the bones it
lacks appended and every skin's palette indices for the robe are rewritten), and the outline is fitted in the stand
pose (frame 0), each moved vertex mapped back through its own blended bone transform. MARGIN is generous because only
vertices are fitted: the faces between them cut across the hips' curve.
Run m2_fix_winding.py afterwards to recompute the robe's normals.

usage: python -I vrykul_robe_waist.py <VrykulPCFemale.m2>   (in place, with its skin profiles)"""
import math
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_pose import apply, blended, stand_matrices, unapply, vertex_skin   # noqa: E402
from vrykul_robe_seam import BODY, ROBE, VERTEX_SIZE, geosets, load, open_edge_vertices, position   # noqa: E402

WAIST = 1.68        # where the robe's top edge goes (the narrowest point above the hips is about 1.70)
LOWER = 1.35        # the robe below this keeps its shape
MARGIN = 0.035      # how far outside the (smoothed) body the robe stays
ARM_BONES = (17, 19)
ANGLE_BIN, HEIGHT_BIN = 10, 0.025
WIDEN = (2, 2)      # bins (direction, height) the body outline is widened over before blurring
BLUR = (2, 2)       # bins (direction, height) of the box blur


def outline(points, centre, zlo, zhi):
    """Max radius per (direction bin, height bin) of points around centre, within zlo..zhi."""
    cx, cy = centre
    na = 360 // ANGLE_BIN
    nh = int(math.ceil((zhi - zlo) / HEIGHT_BIN)) + 1
    grid = [[0.0] * nh for _ in range(na)]
    for p in points:
        if not zlo <= p[2] <= zhi:
            continue
        a = int((math.degrees(math.atan2(p[1] - cy, p[0] - cx)) % 360) // ANGLE_BIN) % na
        h = int((p[2] - zlo) // HEIGHT_BIN)
        grid[a][h] = max(grid[a][h], math.hypot(p[0] - cx, p[1] - cy))
    return grid


def widen_blur(grid, widen, blur, fill_empty=False):
    na, nh = len(grid), len(grid[0])
    wide = [[max(grid[(a + da) % na][h + dh] for da in range(-widen[0], widen[0] + 1)
                 for dh in range(-widen[1], widen[1] + 1) if 0 <= h + dh < nh) for h in range(nh)] for a in range(na)]
    out = []
    for a in range(na):
        row = []
        for h in range(nh):
            vals = [wide[(a + da) % na][h + dh] for da in range(-blur[0], blur[0] + 1)
                    for dh in range(-blur[1], blur[1] + 1) if 0 <= h + dh < nh]
            vals = [v for v in vals if v > 0] if fill_empty else vals
            row.append(sum(vals) / len(vals) if vals else 0.0)
        out.append(row)
    return out


def sample(grid, a, z, zlo):
    """Bilinear lookup in a (direction, height) grid."""
    na, nh = len(grid), len(grid[0])
    fa = (a % 360) / ANGLE_BIN - 0.5
    fh = min(max((z - zlo) / HEIGHT_BIN - 0.5, 0), nh - 1)
    a0, h0 = int(math.floor(fa)), int(math.floor(fh))
    ta, th = fa - a0, fh - h0
    h1 = min(h0 + 1, nh - 1)
    g = lambda i, j: grid[i % na][j]
    return ((g(a0, h0) * (1 - ta) + g(a0 + 1, h0) * ta) * (1 - th)
            + (g(a0, h1) * (1 - ta) + g(a0 + 1, h1) * ta) * th)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    data, skin = load(model)
    data = bytearray(data)
    geo = geosets(data, skin)
    nbones, obones = struct.unpack_from('<II', data, 0x2C)
    overt = struct.unpack_from('<I', data, 0x40)[0]
    parent = lambda b: struct.unpack_from('<h', data, obones + 88 * b + 8)[0]

    def arm(v):
        o = overt + VERTEX_SIZE * v
        weights, bones = data[o + 12:o + 16], data[o + 16:o + 20]
        b = bones[weights.index(max(weights))]
        while b != -1:
            if b in ARM_BONES:
                return True
            b = parent(b)
        return False

    robe = sorted({v for t in geo[ROBE] for v in t})
    pos = {v: position(data, v) for v in robe}
    cx = sum(p[0] for p in pos.values()) / len(robe)
    cy = sum(p[1] for p in pos.values()) / len(robe)
    polar = lambda p: (math.degrees(math.atan2(p[1] - cy, p[0] - cx)) % 360, math.hypot(p[0] - cx, p[1] - cy))

    # the top edge's height by direction (it is lower at the front than at the sides)
    edge = sorted((polar(position(data, v))[0], position(data, v)[2])
                  for v in open_edge_vertices(data, geo[ROBE]) if position(data, v)[2] > 1.2)

    def top_at(a):
        after = next((i for i, e in enumerate(edge) if e[0] >= a), 0)
        (a0, z0), (a1, z1) = edge[after - 1], edge[after]
        span = (a1 - a0) % 360 or 360.0
        return z0 + (z1 - z0) * ((a - a0) % 360) / span

    # new positions: heights stretched in the band, then the outlines
    raised = {}
    for v, p in pos.items():
        if p[2] <= LOWER:
            continue
        a, _ = polar(p)
        z = LOWER + (p[2] - LOWER) * (WAIST - LOWER) / max(top_at(a) - LOWER, p[2] - LOWER, 1e-6)
        raised[v] = (p[0], p[1], z)

    body_vertices = [v for v in {v for t in geo[BODY] for v in t} if not arm(v)]
    body_cells = {}
    for v in body_vertices:
        p = position(data, v)
        body_cells.setdefault(tuple(int(c // 0.05) for c in p), []).append(v)

    def nearest_body(p):
        c = tuple(int(x // 0.05) for x in p)
        best, best_d = None, 1e9
        for reach_ in (1, 2, 3):
            for dx in range(-reach_, reach_ + 1):
                for dy in range(-reach_, reach_ + 1):
                    for dz in range(-reach_, reach_ + 1):
                        for v in body_cells.get((c[0] + dx, c[1] + dy, c[2] + dz), ()):
                            dd = math.dist(p, position(data, v))
                            if dd < best_d:
                                best, best_d = v, dd
            if best is not None:
                return best
        return None

    def influences(v):
        o = overt + VERTEX_SIZE * v
        return {b: w for w, b in zip(data[o + 12:o + 16], data[o + 16:o + 20]) if w}

    # bone weights of the band: towards the nearest body vertex's, more the higher up the band
    fraction = {v: (p[2] - LOWER) / (WAIST - LOWER) for v, p in raised.items()}
    for v, p in raised.items():
        near = nearest_body(p)
        if near is None:
            continue
        f = fraction[v]
        mixed = {}
        for b, w in influences(v).items():
            mixed[b] = mixed.get(b, 0) + w * (1 - f)
        for b, w in influences(near).items():
            mixed[b] = mixed.get(b, 0) + w * f
        top4 = sorted(mixed.items(), key=lambda item: -item[1])[:4]
        total = sum(w for _, w in top4)
        weights = [int(round(w * 255 / total)) for _, w in top4]
        weights[0] += 255 - sum(weights)
        o = overt + VERTEX_SIZE * v
        data[o + 12:o + 16] = bytes(weights + [0] * (4 - len(weights)))
        data[o + 16:o + 20] = bytes([b for b, _ in top4] + [0] * (4 - len(top4)))

    # the outline is fitted in the stand pose (the spine leans the belly forward there, which a bind-pose fit misses)
    # and the moved vertices are mapped back through their own blended bone transform
    mats = stand_matrices(data)
    transform = {v: blended(mats, *vertex_skin(data, v)) for v in robe}
    posed = {v: apply(transform[v], raised.get(v, pos[v])) for v in robe}
    pcx = sum(p[0] for p in posed.values()) / len(robe)
    pcy = sum(p[1] for p in posed.values()) / len(robe)
    ppolar = lambda p: (math.degrees(math.atan2(p[1] - pcy, p[0] - pcx)) % 360, math.hypot(p[0] - pcx, p[1] - pcy))
    posed_body = [apply(blended(mats, *vertex_skin(data, v)), position(data, v)) for v in body_vertices]
    zlo = min(posed[v][2] for v in raised) - 4 * HEIGHT_BIN
    zhi = max(posed[v][2] for v in raised) + 2 * HEIGHT_BIN
    body_grid = widen_blur(outline(posed_body, (pcx, pcy), zlo, zhi), WIDEN, BLUR)

    # the robe can be several layers (an outer one and a lining) that cross each other; each gets its own outline, so
    # every layer reaches the target, not just whichever is furthest out in a place
    key = lambda p: tuple(round(c, 4) for c in p)
    parent_of = {}

    def find(x):
        while parent_of.setdefault(x, x) != x:
            parent_of[x] = parent_of[parent_of[x]]
            x = parent_of[x]
        return x

    for t in geo[ROBE]:
        k = [key(pos[v]) for v in t]
        parent_of[find(k[1])] = find(k[0])
        parent_of[find(k[2])] = find(k[0])
    layer = {v: find(key(p)) for v, p in pos.items()}
    band_grids = {}
    for l in set(layer.values()):
        points = [posed[v] for v in robe if layer[v] == l]
        band_grids[l] = widen_blur(outline(points, (pcx, pcy), zlo, zhi), (1, 1), (1, 1), fill_empty=True)

    moved = 0
    for v, p in raised.items():
        q = posed[v]
        a, r = ppolar(q)
        if r < 1e-6:
            continue
        f = fraction[v]
        band_grid = band_grids[layer[v]]
        low_z = q[2] - (p[2] - LOWER)    # where the band starts and ends, at this vertex's place in the pose
        waist_z = q[2] + (WAIST - p[2])
        start = sample(band_grid, a, low_z, zlo)
        waist = sample(body_grid, a, waist_z, zlo) + MARGIN
        target = max(start + (waist - start) * f, sample(body_grid, a, q[2], zlo) + MARGIN)
        current = sample(band_grid, a, q[2], zlo)
        s = target / current if current > 1e-6 else 1.0
        new_posed = (pcx + (q[0] - pcx) * s, pcy + (q[1] - pcy) * s, q[2])
        struct.pack_into('<3f', data, overt + VERTEX_SIZE * v, *unapply(transform[v], new_posed))
        moved += 1

    # the robe's bone palette: append the bones it now needs, as a new slice of the model's bone combos
    ncombo, ocombo = struct.unpack_from('<II', data, 0x78)
    combos = list(struct.unpack_from('<%dH' % ncombo, data, ocombo))
    base = os.path.splitext(model)[0]
    profiles = struct.unpack_from('<I', data, 0x44)[0]
    needed = sorted({b for v in robe for b in influences(v)})
    skins = []
    palette = None
    for profile in range(profiles):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            skins.append((path, bytearray(f.read())))
    for path, sk in skins:
        nsec, osec = struct.unpack_from('<II', sk, 0x1C)
        for s_ in range(nsec):
            sid, _, _, _, _, _, count, index = struct.unpack_from('<8H', sk, osec + 48 * s_)
            if sid == ROBE:
                old = combos[index:index + count]
                if palette is None:
                    palette = old + [b for b in needed if b not in old]
                elif old != palette[:len(old)]:
                    sys.exit('%s: the robe\'s sections have different bone palettes' % path)
    if palette is None:
        sys.exit('%s: no robe sections' % model)
    first = len(combos)
    combos += palette
    data += b'\0' * (-len(data) % 16)
    struct.pack_into('<II', data, 0x78, len(combos), len(data))
    data += struct.pack('<%dH' % len(combos), *combos)
    index_of = {b: i for i, b in enumerate(palette)}
    for path, sk in skins:
        nlook, olook = struct.unpack_from('<II', sk, 0x04)
        lookup = struct.unpack_from('<%dH' % nlook, sk, olook)
        oprop = struct.unpack_from('<I', sk, 0x18)[0]
        nsec, osec = struct.unpack_from('<II', sk, 0x1C)
        for s_ in range(nsec):
            o = osec + 48 * s_
            sid, _, vstart, vcount = struct.unpack_from('<4H', sk, o)
            if sid != ROBE:
                continue
            struct.pack_into('<HH', sk, o + 12, len(palette), first)
            for i in range(vstart, vstart + vcount):
                vo = overt + VERTEX_SIZE * lookup[i]
                weights, bones = data[vo + 12:vo + 16], data[vo + 16:vo + 20]
                sk[oprop + 4 * i:oprop + 4 * i + 4] = bytes(index_of[b] if w else 0 for w, b in zip(weights, bones))
        with open(path, 'wb') as f:
            f.write(sk)

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: %d robe vertices: top band raised to the waist (%.2f), smooth outline, weights towards the waist; '
          'robe palette %d bones' % (model, moved, WAIST, len(palette)))


if __name__ == '__main__':
    main()
