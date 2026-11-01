"""Replace a geoset of a 3.3.5 (version 264) character model with the same geoset from another character model.

Made to give the female Vrykul PC model the Kul Tiran female robe (1302): hers is a sparse retail conversion whose
layers and hip join gave endless trouble, the Kul Tiran one a clean single-layer robe built to hang from the hip seam,
with the same (WotLK) texture layout.

The donor geoset is fitted onto the one it replaces: heights are scaled so its top and bottom match the old geoset's
(the floor stays at 0), and across, it is scaled separately front-to-back and side-to-side so its top ring matches
the old geoset's top ring (its open edges in the top tenth of its height) and its hem the old hem, blending between
the two by height (the old geoset's flare is kept). Each new vertex takes its texture
coordinates and normal from the donor and its bone weights blended from the nearest vertices of the old geoset (by
inverse distance), so no bones have
to be matched between the two skeletons and the target's bone palettes stay valid. The model's vertex array grows (the
old geoset's vertices are left unused); in every skin profile each section of the geoset gets the donor's triangles,
its vertex list and palette indices, appended to the file.

Afterwards run vrykul_robe_seam.py etc. to stitch the new robe's top edge to the body.

usage: python -I m2_transplant_geoset.py <target.m2> <donor.m2> <geoset>   (target and its skins in place)"""
import math
import os
import struct
import sys
from collections import Counter

VERTEX_SIZE, SECTION_SIZE = 48, 48
NEAREST = 6   # old vertices whose bone weights a new vertex blends


def read(model):
    with open(model, 'rb') as f:
        data = bytearray(f.read())
    with open(os.path.splitext(model)[0] + '00.skin', 'rb') as f:
        skin = f.read()
    return data, skin


def triangles(data, skin, geoset):
    """[(model vertex a, b, c)] of the geoset in a skin profile."""
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
            out += [tuple(lookup[tri[t + j]] for j in range(3)) for t in range(start, start + count, 3)]
    return out


def vertex(data, v):
    o = struct.unpack_from('<I', data, 0x40)[0] + VERTEX_SIZE * v
    return bytes(data[o:o + VERTEX_SIZE])


def ring(data, tris, top_end=True):
    """(centre x, centre y, half width x, half width y, ring z, other end z) of the geoset: its open edges in the top
    (or bottom) tenth of its height."""
    pos = lambda v: struct.unpack_from('<3f', data, struct.unpack_from('<I', data, 0x40)[0] + VERTEX_SIZE * v)
    key = lambda v: tuple(round(c, 4) for c in pos(v))
    edges = Counter()
    for t in tris:
        k = [key(v) for v in t]
        for a, b in ((0, 1), (1, 2), (2, 0)):
            edges[frozenset((k[a], k[b]))] += 1
    zs = [pos(v)[2] for t in tris for v in t]
    top, bottom = max(zs), min(zs)
    tenth = (top - bottom) * 0.1
    points = [p for e, n in edges.items() if n == 1 for p in e
              if (p[2] > top - tenth if top_end else p[2] < bottom + tenth)]
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2,
            sum(p[2] for p in points) / len(points), bottom if top_end else top)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    target, donor, geoset = sys.argv[1], sys.argv[2], int(sys.argv[3])
    data, skin = read(target)
    ddata, dskin = read(donor)
    old = triangles(data, skin, geoset)
    new = triangles(ddata, dskin, geoset)
    if not old or not new:
        sys.exit('geoset %d missing in %s' % (geoset, target if not old else donor))

    tcx, tcy, thx, thy, ttop, tbottom = ring(data, old)
    dcx, dcy, dhx, dhy, dtop, dbottom = ring(ddata, new)
    bcx, bcy, bhx, bhy, _, _ = ring(data, old, False)          # the old hem
    ecx, ecy, ehx, ehy, _, _ = ring(ddata, new, False)         # the donor's hem
    kz = (ttop - tbottom) / (dtop - dbottom)

    def fit(p):
        """Across, the scale and centre run from matching the top rings at the top to matching the hems at the bottom,
        so the new geoset keeps the old one's flare."""
        f = min(1.0, max(0.0, (p[2] - dbottom) / (dtop - dbottom)))
        sx = (bhx / ehx) * (1 - f) + (thx / dhx) * f
        sy = (bhy / ehy) * (1 - f) + (thy / dhy) * f
        ox, oy = (bcx * (1 - f) + tcx * f), (bcy * (1 - f) + tcy * f)
        ix, iy = (ecx * (1 - f) + dcx * f), (ecy * (1 - f) + dcy * f)
        return (ox + (p[0] - ix) * sx, oy + (p[1] - iy) * sy, tbottom + (p[2] - dbottom) * kz)

    kx, ky = thx / dhx, thy / dhy   # for the normals (the top's scale)

    overt = struct.unpack_from('<I', data, 0x40)[0]
    old_vertices = sorted({v for t in old for v in t})
    old_pos = {v: struct.unpack_from('<3f', data, overt + VERTEX_SIZE * v) for v in old_vertices}

    def blended_weights(p):
        """Bone weights blended from the NEAREST closest old vertices, by inverse distance (one nearest vertex alone
        lets neighbouring new vertices follow different bones, which kinks the geoset when posed)."""
        near = sorted(old_vertices, key=lambda v: math.dist(p, old_pos[v]))[:NEAREST]
        mixed = {}
        for v in near:
            k = 1.0 / (math.dist(p, old_pos[v]) + 1e-3)
            o = overt + VERTEX_SIZE * v
            for w, b in zip(data[o + 12:o + 16], data[o + 16:o + 20]):
                if w:
                    mixed[b] = mixed.get(b, 0.0) + w * k
        top4 = sorted(mixed.items(), key=lambda item: -item[1])[:4]
        total = sum(w for _, w in top4)
        weights = [int(round(w * 255 / total)) for _, w in top4]
        weights[0] += 255 - sum(weights)
        return bytes(weights + [0] * (4 - len(weights))) + bytes([b for b, _ in top4] + [0] * (4 - len(top4)))

    # the donor's vertices, fitted, with the nearest old vertex's bone weights
    donor_vertices = sorted({v for t in new for v in t})
    nvert = struct.unpack_from('<I', data, 0x3C)[0]
    index_of = {}
    added = bytearray()
    for i, v in enumerate(donor_vertices):
        raw = bytearray(vertex(ddata, v))
        p = fit(struct.unpack_from('<3f', raw, 0))
        struct.pack_into('<3f', raw, 0, *p)
        n = struct.unpack_from('<3f', raw, 20)
        n = (n[0] / kx, n[1] / ky, n[2] / kz)          # normals transform by the inverse scale
        length = math.sqrt(sum(c * c for c in n)) or 1.0
        struct.pack_into('<3f', raw, 20, *(c / length for c in n))
        raw[12:20] = blended_weights(p)
        index_of[v] = nvert + i
        added += raw
    vertices_blob = bytes(data[overt:overt + VERTEX_SIZE * nvert]) + bytes(added)
    data += b'\0' * (-len(data) % 16)
    struct.pack_into('<II', data, 0x3C, nvert + len(donor_vertices), len(data))
    data += vertices_blob
    new_tris = [tuple(index_of[v] for v in t) for t in new]

    ncombo, ocombo = struct.unpack_from('<II', data, 0x78)
    combos = struct.unpack_from('<%dH' % ncombo, data, ocombo)
    profiles = struct.unpack_from('<I', data, 0x44)[0]
    base = os.path.splitext(target)[0]
    overt = struct.unpack_from('<I', data, 0x40)[0]
    for profile in range(profiles):
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
        mine = [s for s in sections if struct.unpack_from('<H', s, 0)[0] == geoset]
        if not mine:
            continue
        # the first section of the geoset gets all the new triangles; any others are emptied
        for s in mine[1:]:
            struct.pack_into('<H', s, 10, 0)
        section = mine[0]
        count, index = struct.unpack_from('<HH', section, 12)
        palette = {combos[index + i]: i for i in range(count)}
        used = sorted({v for t in new_tris for v in t})
        first = len(lookup)
        local = {}
        for v in used:
            local[v] = len(lookup)
            lookup.append(v)
            o = overt + VERTEX_SIZE * v
            weights, bones = data[o + 12:o + 16], data[o + 16:o + 20]
            props += bytes(palette[b] if w else 0 for w, b in zip(weights, bones))
        start = len(tri)
        for t in new_tris:
            tri += [local[v] for v in t]
        if len(lookup) > 0xFFFF:
            sys.exit('%s: too many vertices for 16-bit indices' % path)
        struct.pack_into('<HHHHHH', section, 0, geoset, start >> 16, first, len(used), start & 0xFFFF, 3 * len(new_tris))

        def append(offset_field, count_, payload):
            sk.extend(b'\0' * (-len(sk) % 16))
            struct.pack_into('<II', sk, offset_field, count_, len(sk))
            sk.extend(payload)

        append(0x04, len(lookup), struct.pack('<%dH' % len(lookup), *lookup))
        append(0x0C, len(tri), struct.pack('<%dH' % len(tri), *tri))
        append(0x14, len(props) // 4, bytes(props))
        append(0x1C, len(sections), b''.join(sections))
        with open(path, 'wb') as f:
            f.write(sk)
        print('%s: geoset %d replaced (%d triangles, %d vertices)' % (path, geoset, len(new_tris), len(used)))

    with open(target, 'wb') as f:
        f.write(data)
    print('%s: geoset %d from %s fitted (across x %.2f, y %.2f, height %.2f)' % (target, geoset, donor, kx, ky, kz))


if __name__ == '__main__':
    main()
