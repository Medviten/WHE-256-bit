"""Join the female Vrykul PC robe (geoset 1302) to its body with a watertight strip of triangles at the hip seam.

The body (geoset 0) ends at a seam that the legs (1301) close, and a robe hides the legs. As long as the robe's top edge
and the seam are separate edges, some camera angle sees between them: an edge outside the hips shows a gap from above,
one tucked inside from below, and one exactly on the seam cracks (it has fewer points, so it runs straight where the
seam bends). So this adds triangles, drawn with the robe, between the two: the strip's upper edge is every seam point,
with the position, bone weights and texture coordinates of the body's own vertex there, so it can't open in any
animation; its lower edge is the robe's top edge (put just below the seam by vrykul_robe_seam.py, which must run first).
The two edges are zipped together in order around the hips.

The strip's vertices are added to the model; in every skin profile the robe's section gets them (its vertex list and
triangles are moved to the end of the file, as a section's vertices must be contiguous). The winding is the top edge's
neighbours' to be: run m2_fix_winding.py afterwards, which settles it and recomputes the robe's normals.

usage: python -I vrykul_robe_zip.py <VrykulPCFemale.m2>   (in place, with its skin profiles)"""
import math
import os
import struct
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vrykul_robe_seam import BODY, LEGS, ROBE, VERTEX_SIZE, geosets, key, load, open_edge_vertices, position   # noqa: E402

SECTION_SIZE = 48


def open_edges(data, triangles):
    count = Counter()
    for t in triangles:
        k = [key(position(data, v)) for v in t]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            if k[a] != k[b]:
                count[frozenset((k[a], k[b]))] += 1
    return {e for e, n in count.items() if n == 1}


def seam_loop(data, geo):
    """The body's and the legs' common open edges, walked into a closed loop of positions (the longest one; a stray
    pair by the hanging hand is not it)."""
    shared = open_edges(data, geo[BODY]) & open_edges(data, geo[LEGS])
    neighbours = defaultdict(list)
    for e in shared:
        a, b = tuple(e)
        neighbours[a].append(b)
        neighbours[b].append(a)
    best = []
    seen = set()
    for start in neighbours:
        if start in seen or len(neighbours[start]) != 2:
            continue
        loop, previous, current = [start], None, start
        while True:
            next_ = [q for q in neighbours[current] if q != previous]
            if not next_ or next_[0] == start:
                closed = bool(next_)
                break
            previous, current = current, next_[0]
            loop.append(current)
        seen.update(loop)
        if closed and len(loop) > len(best):
            best = loop
    return best


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    model = sys.argv[1]
    data, skin = load(model)
    geo = geosets(data, skin)
    nvert, overt = struct.unpack_from('<II', data, 0x3C)

    loop = seam_loop(data, geo)
    if len(loop) < 8:
        sys.exit('%s: no closed hip seam found' % model)
    body_at = {}
    for t in geo[BODY]:
        for v in t:
            body_at.setdefault(key(position(data, v)), v)

    # the robe's top edge, one vertex per position
    top = {}
    for v in sorted(open_edge_vertices(data, geo[ROBE])):
        p = position(data, v)
        if p[2] > 1.2:
            top.setdefault(key(p), v)
    tops = list(top.values())
    cx = sum(position(data, v)[0] for v in tops) / len(tops)
    cy = sum(position(data, v)[1] for v in tops) / len(tops)
    angle = lambda p: math.atan2(p[1] - cy, p[0] - cx) % (2 * math.pi)

    # both edges in the same direction, starting from the same place
    if sum(((angle(loop[(i + 1) % len(loop)]) - angle(loop[i]) + math.pi) % (2 * math.pi)) - math.pi
           for i in range(len(loop))) < 0:
        loop.reverse()
    first = min(range(len(loop)), key=lambda i: angle(loop[i]))
    loop = loop[first:] + loop[:first]
    start = angle(loop[0])
    along = lambda p: (angle(p) - start) % (2 * math.pi)
    tops.sort(key=lambda v: along(position(data, v)))

    # the strip's upper vertices: copies of the body's seam vertices
    index_of = {}
    added = bytearray()
    for i, p in enumerate(loop):
        o = overt + VERTEX_SIZE * body_at[p]
        added += data[o:o + VERTEX_SIZE]
        index_of[p] = nvert + i

    # zip: walk both edges, always advancing the one whose next point comes first
    strip = []
    i = j = 0
    n, m = len(loop), len(tops)
    unwrapped = lambda idx, count, pts: along(pts(idx % count)) + (2 * math.pi if idx >= count else 0)
    while i < n or j < m:
        upper, lower = index_of[loop[i % n]], tops[j % m]
        next_upper = unwrapped(i + 1, n, lambda k: loop[k]) if i < n else float('inf')
        next_lower = unwrapped(j + 1, m, lambda k: position(data, tops[k])) if j < m else float('inf')
        if next_upper <= next_lower:
            strip.append((upper, index_of[loop[(i + 1) % n]], lower))
            i += 1
        else:
            strip.append((upper, tops[(j + 1) % m], lower))
            j += 1

    data += b'\0' * (-len(data) % 16)
    blob = bytes(data[overt:overt + VERTEX_SIZE * nvert]) + bytes(added)
    struct.pack_into('<II', data, 0x3C, nvert + n, len(data))
    data += blob
    overt = struct.unpack_from('<I', data, 0x40)[0]

    ncombo, ocombo = struct.unpack_from('<II', data, 0x78)
    combos = struct.unpack_from('<%dH' % ncombo, data, ocombo)
    base = os.path.splitext(model)[0]
    for profile in range(struct.unpack_from('<I', data, 0x44)[0]):
        path = '%s%02d.skin' % (base, profile)
        with open(path, 'rb') as f:
            sk = bytearray(f.read())
        nlook, olook = struct.unpack_from('<II', sk, 0x04)
        lookup = list(struct.unpack_from('<%dH' % nlook, sk, olook))
        ntri, otri = struct.unpack_from('<II', sk, 0x0C)
        tri = list(struct.unpack_from('<%dH' % ntri, sk, otri))
        nprop, oprop = struct.unpack_from('<II', sk, 0x14)
        props = bytearray(sk[oprop:oprop + 4 * nprop])
        nsec, osec = struct.unpack_from('<II', sk, 0x1C)
        sections = [bytearray(sk[osec + SECTION_SIZE * s:osec + SECTION_SIZE * (s + 1)]) for s in range(nsec)]
        section = max((s for s in sections if struct.unpack_from('<H', s, 0)[0] == ROBE),
                      key=lambda s: struct.unpack_from('<H', s, 10)[0])
        sid, level, vstart, vcount, istart, icount = struct.unpack_from('<6H', section, 0)
        istart |= level << 16
        bone_count, combo_index = struct.unpack_from('<HH', section, 12)
        palette = {combos[combo_index + i]: i for i in range(bone_count)}

        # the section's vertices again at the end, then the strip's, and its triangles remapped plus the strip's
        first_vertex = len(lookup)
        shift = first_vertex - vstart
        lookup += lookup[vstart:vstart + vcount]
        # palette indices from the model's bones: vrykul_robe_seam.py changed those, and the client skins by these
        for v in lookup[first_vertex:first_vertex + vcount]:
            o = overt + VERTEX_SIZE * v
            weights, bones = data[o + 12:o + 16], data[o + 16:o + 20]
            props += bytes(palette[b] if w else 0 for w, b in zip(weights, bones))
        local = {lookup[first_vertex + i]: first_vertex + i for i in range(vcount)}
        for i in range(n):
            local[nvert + i] = len(lookup)
            lookup.append(nvert + i)
            o = overt + VERTEX_SIZE * (nvert + i)
            weights, bones = data[o + 12:o + 16], data[o + 16:o + 20]
            try:
                props += bytes(palette[b] if w else 0 for w, b in zip(weights, bones))
            except KeyError:
                sys.exit('%s: a seam vertex uses a bone outside the robe\'s palette' % path)
        first_index = len(tri)
        tri += [t + shift for t in tri[istart:istart + icount]]
        for a, b, c in strip:
            tri += [local[a], local[b], local[c]]
        if len(lookup) > 0xFFFF:
            sys.exit('%s: too many vertices for 16-bit indices' % path)
        struct.pack_into('<6H', section, 0, sid, first_index >> 16, first_vertex, vcount + n, first_index & 0xFFFF,
                         icount + 3 * len(strip))

        def append(offset_field, count, payload):
            sk.extend(b'\0' * (-len(sk) % 16))
            struct.pack_into('<II', sk, offset_field, count, len(sk))
            sk.extend(payload)

        append(0x04, len(lookup), struct.pack('<%dH' % len(lookup), *lookup))
        append(0x0C, len(tri), struct.pack('<%dH' % len(tri), *tri))
        append(0x14, len(props) // 4, bytes(props))
        append(0x1C, len(sections), b''.join(sections))
        with open(path, 'wb') as f:
            f.write(sk)
        print('%s: %d strip triangles added to the robe' % (path, len(strip)))

    with open(model, 'wb') as f:
        f.write(data)
    print('%s: seam of %d points zipped to the robe\'s top edge of %d' % (model, n, m))


if __name__ == '__main__':
    main()
