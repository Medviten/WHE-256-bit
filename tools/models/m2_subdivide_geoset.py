"""Smooth one geoset of a 3.3.5 (version 264) character model by Loop subdivision.

Each pass splits every triangle of the geoset into four and moves the vertices towards the smooth (Loop) surface, so a
sparse mesh with long flat faces (e.g. the female Vrykul PC robe, 1302) gets rounded. The geoset's open edges (a robe's
hem and its top at the hip seam) stay where they are; new vertices on them are plain midpoints.

New vertices get the averages of the two vertices they lie between: texture coordinates, normal, and bone weights
(the four largest kept, rescaled to 255). Vertices are welded by position for the topology only, so texture seams stay
seams. Normals of the geoset are recomputed from the result (smooth shading). The geoset's vertices must not be used by
any other geoset (they move); the script checks.

Every skin profile (<model>NN.skin) is rewritten: each section of the geoset gets the subdivided triangles of the
triangles it had, its vertex list and per-vertex bone palette indices, all appended to the file (the old ones are left
unused). The model's vertex array grows and moves to the end of the .m2.

usage: python -I m2_subdivide_geoset.py <model.m2> <geoset> [passes]   (in place; default 1 pass)"""
import math
import os
import struct
import sys
from collections import defaultdict

VERTEX_SIZE, SECTION_SIZE = 48, 48


def arr(data, pos):
    return struct.unpack_from('<II', data, pos)


class Vertex:
    __slots__ = ('pos', 'weights', 'bones', 'normal', 'uv', 'uv2')

    @classmethod
    def read(cls, data, offset):
        v = cls()
        v.pos = list(struct.unpack_from('<3f', data, offset))
        v.weights = list(data[offset + 12:offset + 16])
        v.bones = list(data[offset + 16:offset + 20])
        v.normal = list(struct.unpack_from('<3f', data, offset + 20))
        v.uv = list(struct.unpack_from('<2f', data, offset + 32))
        v.uv2 = list(struct.unpack_from('<2f', data, offset + 40))
        return v

    def pack(self):
        return (struct.pack('<3f', *self.pos) + bytes(self.weights) + bytes(self.bones)
                + struct.pack('<3f', *self.normal) + struct.pack('<2f', *self.uv) + struct.pack('<2f', *self.uv2))

    @staticmethod
    def between(a, b):
        v = Vertex()
        v.pos = [(x + y) / 2 for x, y in zip(a.pos, b.pos)]
        v.normal = [(x + y) / 2 for x, y in zip(a.normal, b.normal)]
        v.uv = [(x + y) / 2 for x, y in zip(a.uv, b.uv)]
        v.uv2 = [(x + y) / 2 for x, y in zip(a.uv2, b.uv2)]
        influence = defaultdict(float)
        for vertex in (a, b):
            for w, bone in zip(vertex.weights, vertex.bones):
                if w:
                    influence[bone] += w / 2
        top = sorted(influence.items(), key=lambda item: -item[1])[:4]
        total = sum(w for _, w in top)
        weights = [int(round(w * 255 / total)) for _, w in top]
        weights[0] += 255 - sum(weights)
        v.weights = weights + [0] * (4 - len(weights))
        v.bones = [bone for bone, _ in top] + [0] * (4 - len(top))
        return v


def subdivide(vertices, triangles):
    """One Loop pass. vertices: list of Vertex (changed in place, new ones appended); triangles: [(a, b, c, parent)].
    Returns the new triangles with the same parents."""
    key = lambda i: tuple(round(c, 4) for c in vertices[i].pos)
    point_of = {}
    points = []
    for t in triangles:
        for i in t[:3]:
            k = key(i)
            if k not in point_of:
                point_of[k] = len(points)
                points.append(vertices[i].pos[:])
    tri_points = [tuple(point_of[key(i)] for i in t[:3]) for t in triangles]

    edge_faces = defaultdict(list)
    for f, (a, b, c) in enumerate(tri_points):
        for x, y, opposite in ((a, b, c), (b, c, a), (c, a, b)):
            edge_faces[frozenset((x, y))].append(opposite)
    boundary = {e for e, opposite in edge_faces.items() if len(opposite) != 2}
    pinned = {p for e in boundary for p in e}
    neighbours = defaultdict(set)
    for e in edge_faces:
        x, y = tuple(e)
        neighbours[x].add(y)
        neighbours[y].add(x)

    def edge_point(e):
        x, y = tuple(e)
        if e in boundary:
            return [(points[x][i] + points[y][i]) / 2 for i in range(3)]
        c, d = edge_faces[e]
        return [3 / 8 * (points[x][i] + points[y][i]) + 1 / 8 * (points[c][i] + points[d][i]) for i in range(3)]

    def vertex_point(p):
        if p in pinned:
            return points[p]
        n = len(neighbours[p])
        beta = 3 / (8 * n) if n > 3 else 3 / 16
        return [(1 - n * beta) * points[p][i] + beta * sum(points[q][i] for q in neighbours[p]) for i in range(3)]

    moved = {p: vertex_point(p) for p in range(len(points))}
    for i in {i for t in triangles for i in t[:3]}:
        vertices[i].pos = moved[point_of[key(i)]][:]

    middles = {}

    def middle(i, j, e):
        k = (e, frozenset((i, j)))
        if k not in middles:
            v = Vertex.between(vertices[i], vertices[j])
            v.pos = edge_point(e)
            middles[k] = len(vertices)
            vertices.append(v)
        return middles[k]

    out = []
    for (a, b, c, parent), (pa, pb, pc) in zip(triangles, tri_points):
        ab = middle(a, b, frozenset((pa, pb)))
        bc = middle(b, c, frozenset((pb, pc)))
        ca = middle(c, a, frozenset((pc, pa)))
        out += [(a, ab, ca, parent), (ab, b, bc, parent), (ca, bc, c, parent), (ab, bc, ca, parent)]
    return out


def recompute_normals(vertices, triangles):
    key = lambda i: tuple(round(c, 4) for c in vertices[i].pos)
    summed = defaultdict(lambda: [0.0, 0.0, 0.0])
    agree = 0
    for a, b, c, _ in triangles:
        pa, pb, pc = vertices[a].pos, vertices[b].pos, vertices[c].pos
        u = [pb[i] - pa[i] for i in range(3)]
        w = [pc[i] - pa[i] for i in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        agree += sum(n[i] * (vertices[a].normal[i] + vertices[b].normal[i] + vertices[c].normal[i]) for i in range(3))
        for i in (a, b, c):
            s = summed[key(i)]
            for j in range(3):
                s[j] += n[j]
    sign = 1 if agree >= 0 else -1   # follow the winding the old normals agree with
    for i in {i for t in triangles for i in t[:3]}:
        s = summed[key(i)]
        length = math.sqrt(sum(x * x for x in s)) or 1.0
        vertices[i].normal = [sign * x / length for x in s]


def main():
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    model, geoset = sys.argv[1], int(sys.argv[2])
    passes = int(sys.argv[3]) if len(sys.argv) == 4 else 1
    base = os.path.splitext(model)[0]
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    if data[:4] != b'MD20' or struct.unpack_from('<I', data, 4)[0] != 264:
        sys.exit('%s: not a version 264 M2' % model)
    nvert, overt = arr(data, 0x3C)
    vertices = [Vertex.read(data, overt + VERTEX_SIZE * i) for i in range(nvert)]
    combos_count, combos_offset = arr(data, 0x78)
    combos = struct.unpack_from('<%dH' % combos_count, data, combos_offset)
    profiles = struct.unpack_from('<I', data, 0x44)[0]

    skins = []
    for profile in range(profiles):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            skins.append((path, bytearray(f.read())))

    # the geoset's triangles over all profiles, in model vertex indices, tagged (profile, section)
    triangles = []
    used_elsewhere = set()
    mine = set()
    for profile, (_, skin) in enumerate(skins):
        nlook, olook = arr(skin, 0x04)
        lookup = struct.unpack_from('<%dH' % nlook, skin, olook)
        ntri, otri = arr(skin, 0x0C)
        tri = struct.unpack_from('<%dH' % ntri, skin, otri)
        nsec, osec = arr(skin, 0x1C)
        for s in range(nsec):
            sid, level, _, _, start, count = struct.unpack_from('<6H', skin, osec + SECTION_SIZE * s)
            start |= level << 16
            corners = [lookup[tri[t]] for t in range(start, start + count)]
            if sid == geoset:
                mine.update(corners)
                if profile == 0:
                    triangles += [tuple(corners[t:t + 3]) + ((0, s),) for t in range(0, count, 3)]
            else:
                used_elsewhere.update(corners)
    if not triangles:
        sys.exit('%s: no geoset %d' % (model, geoset))
    if mine & used_elsewhere:
        sys.exit('%s: geoset %d shares %d vertices with other geosets' % (model, geoset, len(mine & used_elsewhere)))

    # subdivide profile 0's triangles; other profiles reuse the result, matching their triangles by vertices
    parents = {frozenset(t[:3]): i for i, t in enumerate(triangles)}
    work = [(a, b, c, i) for i, (a, b, c, _) in enumerate(triangles)]
    for _ in range(passes):
        work = subdivide(vertices, work)
    recompute_normals(vertices, work)
    children = defaultdict(list)
    for a, b, c, parent in work:
        children[parent].append((a, b, c))

    # model: the grown vertex array at the end
    data += b'\0' * (-len(data) % 16)
    struct.pack_into('<II', data, 0x3C, len(vertices), len(data))
    data += b''.join(v.pack() for v in vertices)
    with open(model, 'wb') as f:
        f.write(data)
    print('%s: geoset %d, %d triangles -> %d, %d vertices added' % (model, geoset, len(triangles), len(work),
                                                                    len(vertices) - nvert))

    for path, skin in skins:
        nlook, olook = arr(skin, 0x04)
        lookup = list(struct.unpack_from('<%dH' % nlook, skin, olook))
        ntri, otri = arr(skin, 0x0C)
        tri = list(struct.unpack_from('<%dH' % ntri, skin, otri))
        nprop, oprop = arr(skin, 0x14)
        props = bytearray(skin[oprop:oprop + 4 * nprop])
        nsec, osec = arr(skin, 0x1C)
        sections = [bytearray(skin[osec + SECTION_SIZE * s:osec + SECTION_SIZE * (s + 1)]) for s in range(nsec)]
        changed = 0
        for section in sections:
            sid, level, vstart, vcount, start, count = struct.unpack_from('<6H', section, 0)
            if sid != geoset:
                continue
            start |= level << 16
            bone_count, combo_index = struct.unpack_from('<HH', section, 12)
            palette = {combos[combo_index + i]: i for i in range(bone_count)}
            new_tris = []
            for t in range(start, start + count, 3):
                corners = frozenset(lookup[tri[t + j]] for j in range(3))
                new_tris += children[parents[corners]]
            used = sorted({i for t in new_tris for i in t})
            first = len(lookup)
            local = {}
            for i in used:
                local[i] = len(lookup)
                lookup.append(i)
                v = vertices[i]
                try:
                    props += bytes(palette[b] if w else 0 for b, w in zip(v.bones, v.weights))
                except KeyError:
                    sys.exit('%s: a new vertex uses a bone outside its section\'s palette' % path)
            index_start = len(tri)
            for t in new_tris:
                tri += [local[i] for i in t]
            if len(lookup) > 0xFFFF:
                sys.exit('%s: too many vertices for 16-bit indices' % path)
            struct.pack_into('<HHHHHH', section, 0, sid, index_start >> 16, first, len(used),
                             index_start & 0xFFFF, len(new_tris) * 3)
            changed += 1

        def append(blob, offset_field, count, payload):
            blob += b'\0' * (-len(blob) % 16)
            struct.pack_into('<II', blob, offset_field, count, len(blob))
            blob += payload

        append(skin, 0x04, len(lookup), struct.pack('<%dH' % len(lookup), *lookup))
        append(skin, 0x0C, len(tri), struct.pack('<%dH' % len(tri), *tri))
        append(skin, 0x14, len(props) // 4, bytes(props))
        append(skin, 0x1C, len(sections), b''.join(sections))
        with open(path, 'wb') as f:
            f.write(skin)
        print('%s: %d section(s) rewritten' % (path, changed))


if __name__ == '__main__':
    main()
