"""Give a tube-like geoset (a robe, 1302) of a 3.3.5 character model a consistent winding: its outermost layer faces
outward, any layer inside it faces inward (a lining, seen from inside).

The game culls back faces. A robe can be two layers, the outer seen from outside and the inner, facing inward, from
inside; if the layers are the wrong way round, or a layer is wound inconsistently, the robe shows holes and the wrong
layer, and looks like it wraps oddly. (The female Vrykul PC robe has its lining outside its outer layer.) Each
triangle's winding is first guessed from whether it faces away from the geoset's vertical centre line (per height
band), then settled by its neighbours (most triangles sharing its edges must agree), so each connected layer is wound
consistently. The layer furthest out (median distance from the centre line) then faces out and every other layer in.
Triangles are reversed in every skin profile, and the normals are recomputed from the faces (smooth, welded by
position within a layer). The geoset's vertices must not be used by other geosets.

usage: python -I m2_fix_winding.py <model.m2> <geoset>   (in place)"""
import math
import os
import struct
import sys
from collections import defaultdict

VERTEX_SIZE, SECTION_SIZE = 48, 48
BAND = 0.1


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    model, geoset = sys.argv[1], int(sys.argv[2])
    base = os.path.splitext(model)[0]
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    nvert, overt = struct.unpack_from('<II', data, 0x3C)
    profiles = struct.unpack_from('<I', data, 0x44)[0]
    pos = lambda v: struct.unpack_from('<3f', data, overt + VERTEX_SIZE * v)

    skins = []
    for profile in range(profiles):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            skins.append((path, bytearray(f.read())))

    def triangles(skin):
        """[(triangle index position in the skin's triangle list, (model vertex a, b, c))] of the geoset"""
        nlook, olook = struct.unpack_from('<II', skin, 0x04)
        lookup = struct.unpack_from('<%dH' % nlook, skin, olook)
        ntri, otri = struct.unpack_from('<II', skin, 0x0C)
        tri = struct.unpack_from('<%dH' % ntri, skin, otri)
        nsec, osec = struct.unpack_from('<II', skin, 0x1C)
        out = []
        for s in range(nsec):
            sid, level, _, _, start, count = struct.unpack_from('<6H', skin, osec + SECTION_SIZE * s)
            if sid == geoset:
                start |= level << 16
                out += [(t, tuple(lookup[tri[t + j]] for j in range(3))) for t in range(start, start + count, 3)]
        return out, otri

    first, _ = triangles(skins[0][1])
    if not first:
        sys.exit('%s: no geoset %d' % (model, geoset))
    verts = {v for _, t in first for v in t}

    # centre line per height band
    bands = defaultdict(list)
    for v in verts:
        p = pos(v)
        bands[int(p[2] // BAND)].append(p)
    centre = {b: (sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps)) for b, ps in bands.items()}

    def face(t):
        a, b, c = (pos(v) for v in t)
        u = [b[j] - a[j] for j in range(3)]
        w = [c[j] - a[j] for j in range(3)]
        return [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]], \
               [(a[j] + b[j] + c[j]) / 3 for j in range(3)]

    def inward(t):
        n, m = face(t)
        cx, cy = centre.get(int(m[2] // BAND), centre[min(centre, key=lambda b: abs(b - m[2] // BAND))])
        return n[0] * (m[0] - cx) + n[1] * (m[1] - cy) < 0

    # the guess by direction is unsure where the robe folds; settle those by their neighbours: a triangle takes the
    # winding most triangles sharing its edges agree with (an edge they share runs opposite ways in both)
    key = lambda v: tuple(round(c, 4) for c in pos(v))
    faces = [t for _, t in first]
    flip = [inward(t) for t in faces]
    by_edge = defaultdict(list)
    for i, t in enumerate(faces):
        k = [key(v) for v in t]
        for x, y in ((0, 1), (1, 2), (2, 0)):
            by_edge[frozenset((k[x], k[y]))].append(i)

    def directed(i):
        k = [key(v) for v in faces[i]]
        if flip[i]:
            k = [k[0], k[2], k[1]]
        return {(k[0], k[1]), (k[1], k[2]), (k[2], k[0])}

    for _ in range(50):
        changed = 0
        for i, t in enumerate(faces):
            mine = directed(i)
            agree = disagree = 0
            for x, y in mine:
                for j in by_edge[frozenset((x, y))]:
                    if j == i:
                        continue
                    if (y, x) in directed(j):
                        agree += 1
                    elif (x, y) in directed(j):
                        disagree += 1
            if disagree > agree:
                flip[i] = not flip[i]
                changed += 1
        if not changed:
            break

    # connected layers: the outermost faces out, the others in
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for t in faces:
        k = [key(v) for v in t]
        parent[find(k[1])] = find(k[0])
        parent[find(k[2])] = find(k[0])
    layer = [find(key(t[0])) for t in faces]
    members = defaultdict(list)
    for i, l in enumerate(layer):
        members[l].append(i)

    def facing_out(i):
        t = faces[i]
        n, m = face((t[0], t[2], t[1]) if flip[i] else t)
        cx, cy = centre.get(int(m[2] // BAND), centre[min(centre, key=lambda b: abs(b - m[2] // BAND))])
        return n[0] * (m[0] - cx) + n[1] * (m[1] - cy) > 0, math.hypot(m[0] - cx, m[1] - cy)

    radius = {}
    for l, idx in members.items():
        rs = sorted(facing_out(i)[1] for i in idx)
        radius[l] = rs[len(rs) // 2]
    outer = max(radius, key=radius.get)
    for l, idx in members.items():
        out = sum(facing_out(i)[0] for i in idx)
        want_out = l == outer
        if (out * 2 >= len(idx)) != want_out:
            for i in idx:
                flip[i] = not flip[i]
        print('layer of %d triangles (median radius %.3f): faces %s' % (len(idx), radius[l], 'out' if want_out else 'in'))
    flipped_faces = {frozenset(t) for t, f in zip(faces, flip) if f}
    for path, skin in skins:
        tris, otri = triangles(skin)
        flipped = 0
        for t, corners in tris:
            if frozenset(corners) in flipped_faces:
                a, b = struct.unpack_from('<HH', skin, otri + 2 * (t + 1))
                struct.pack_into('<HH', skin, otri + 2 * (t + 1), b, a)
                flipped += 1
        with open(path, 'wb') as f:
            f.write(skin)
        print('%s: %d of %d triangles of geoset %d reversed' % (path, flipped, len(tris), geoset))

    # normals from the corrected faces, welded by position within a layer
    summed = defaultdict(lambda: [0.0, 0.0, 0.0])
    layer_of = {}
    for i, t in enumerate(faces):
        a, b, c = (t[0], t[2], t[1]) if flip[i] else t
        n, _ = face((a, b, c))
        for v in t:
            layer_of[v] = layer[i]
            s = summed[(layer[i], key(v))]
            for j in range(3):
                s[j] += n[j]
    for v in verts:
        s = summed[(layer_of[v], key(v))]
        length = math.sqrt(sum(x * x for x in s)) or 1.0
        struct.pack_into('<3f', data, overt + VERTEX_SIZE * v + 20, *(x / length for x in s))
    with open(model, 'wb') as f:
        f.write(data)
    print('%s: normals of geoset %d recomputed (%d vertices)' % (model, geoset, len(verts)))


if __name__ == '__main__':
    main()
