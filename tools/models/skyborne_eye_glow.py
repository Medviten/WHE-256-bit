#!/usr/bin/env python3
"""Give the native Skyborne models (F-103/F-104) the eye glows of Forever's Skyborne models.

Kalibro's native models have no eye glow geometry. Forever's (FileDataIDs 7478487 male, 7478494 female, in a
RetailPackBuild --forever pack) have retail's five: 1701 a smoke trail and 1702-1705 glowing orbs in yellow, orange,
pale violet and blue (see m2_retail_combiners.py). This copies the smoke and the yellow and blue orbs, numbered for the
3.3.5 client's group 17: yellow 1702 (the race's own glow, shown by facial styles whose CharFacialHairStyles geoset 5
is 2) and smoke plus blue 1703 (death knights).

The native models are conversions of these, with the same skeleton and eyes, so the vertices are copied unchanged
(positions, normals, bone weights, both UV sets); each glow section gets its own bone palette. The glow textures are
already in the native models (the same files under either sex's name). Batches get two layers on UV sets 0 and 1 and
no texture animation; run m2_retail_combiners.py afterwards for their shading.

usage: skyborne_eye_glow.py [--common PATH] [--pack PATH]
Patched in place; a model that already has the glows is left alone."""
import argparse, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_retail_combiners import glow_kind, pair_index, append_data, TEXTURE_COMBOS, UV_COMBOS, TRANSFORM_COMBOS  # noqa: E402

DONORS = {'male': 7478487, 'female': 7478494}
PORTED = {'smoke': 1703, 'yellow': 1702, 'blue': 1703}
SMOKE_TEXTURES = ('7479318.blp', '7479201.blp')
ATLAS_TEXTURES = ('7479319.blp', '7479202.blp')
GLOW_MATERIAL = (0x15, 4)                      # unlit, two-sided, no depth write; additive
TARGET_EYE = (0, 192)                          # the native eyes (geoset 0, 192 triangles): their batch is the template
BONE_COMBOS = 0x78
VERTEX, SECTION, BATCH = 48, 48, 24


def read_donor(pack, fid):
    d = open(os.path.join(pack, '%d.bin' % fid), 'rb').read()
    chunks, o = {}, 0
    while o + 8 <= len(d):
        size, = struct.unpack_from('<I', d, o + 4)
        chunks[d[o:o + 4]] = (o + 8, size)
        o += 8 + size
    mo, ms = chunks[b'MD21']
    skin, = struct.unpack_from('<I', d, chunks[b'SFID'][0])
    return bytes(d[mo:mo + ms]), open(os.path.join(pack, '%d.bin' % skin), 'rb').read()


def bones(m):
    n, o = struct.unpack_from('<II', m, 0x2C)
    # key bone id, parent and pivot: what the vertex weights depend on (the converter changes the flags)
    return [(bytes(m[o + 88 * i:o + 88 * i + 4]), bytes(m[o + 88 * i + 8:o + 88 * i + 10]),
             tuple(round(c, 4) for c in struct.unpack_from('<3f', m, o + 88 * i + 76))) for i in range(n)]


def sections(s):
    ns, osub = struct.unpack_from('<II', s, 0x1C)
    return [struct.unpack_from('<6H', s, osub + SECTION * i) for i in range(ns)]


def section_vertices(s, index):
    nl, ol = struct.unpack_from('<II', s, 0x04)
    lookup = struct.unpack_from('<%dH' % nl, s, ol)
    _, _, vs, vc, _, _ = sections(s)[index]
    return [lookup[vs + k] for k in range(vc)]


def section_triangles(s, index):
    """Model-vertex triangles of a section."""
    nl, ol = struct.unpack_from('<II', s, 0x04)
    lookup = struct.unpack_from('<%dH' % nl, s, ol)
    nt, ot = struct.unpack_from('<II', s, 0x0C)
    tri = struct.unpack_from('<%dH' % nt, s, ot)
    _, level, _, _, start, count = sections(s)[index]
    start |= level << 16
    return [tuple(lookup[tri[t + j]] for j in range(3)) for t in range(start, start + count, 3)]


def texture_slot(d, endings):
    nt, ot = struct.unpack_from('<II', d, 0x50)
    for i in range(nt):
        n, o = struct.unpack_from('<II', d, ot + 16 * i + 8)
        if d[o:o + n].rstrip(b'\0').decode('latin1').lower().endswith(endings):
            return i
    raise SystemExit('no texture slot ending in %s' % (endings,))


def port(target, pack, fid):
    d = bytearray(open(target, 'rb').read())
    skin_path = target[:-3] + '00.skin'
    sk = bytearray(open(skin_path, 'rb').read())
    osub = struct.unpack_from('<I', sk, 0x20)[0]
    if any(sid in (1702, 1703) and glow_kind(d, sk, osub + SECTION * i) for i, (sid, *_) in enumerate(sections(sk))):
        return 'already has the glows'
    m, ms = read_donor(pack, fid)
    if bones(m) != bones(d):
        return 'skipped: the skeleton differs from Forever model %d' % fid

    dsub = struct.unpack_from('<I', ms, 0x20)[0]
    glows = []
    for i in range(len(sections(ms))):
        kind = glow_kind(m, ms, dsub + SECTION * i)
        if kind and kind[0] in PORTED:
            glows.append((kind[0], i))
    if sorted(k for k, _ in glows) != sorted(PORTED):
        return 'skipped: Forever model %d lacks some glows (%s)' % (fid, glows)

    # the glows' vertices, unchanged, appended to the vertex array
    nvert, overt = struct.unpack_from('<II', d, 0x3C)
    dvert = struct.unpack_from('<I', m, 0x40)[0]
    added, index_of = bytearray(), {}
    for _, i in glows:
        for v in section_vertices(ms, i):
            if v not in index_of:
                index_of[v] = nvert + len(index_of)
                added += m[dvert + VERTEX * v:dvert + VERTEX * (v + 1)]
    if nvert + len(index_of) > 0xFFFF:
        return 'skipped: too many vertices for 16-bit indices'
    struct.pack_into('<II', d, 0x3C, nvert + len(index_of),
                     append_data(d, bytes(d[overt:overt + VERTEX * nvert]) + bytes(added)))
    overt = struct.unpack_from('<I', d, 0x40)[0]

    # materials, textures and lookups
    nm, om = struct.unpack_from('<II', d, 0x70)
    materials = [struct.unpack_from('<HH', d, om + 4 * i) for i in range(nm)]
    if GLOW_MATERIAL not in materials:
        return 'skipped: no unlit additive material to use'
    material = materials.index(GLOW_MATERIAL)
    smoke, atlas = texture_slot(d, SMOKE_TEXTURES), texture_slot(d, ATLAS_TEXTURES)
    tex_pairs = {slot: pair_index(d, TEXTURE_COMBOS, slot, slot, 'H') for slot in (smoke, atlas)}
    uv_pair = pair_index(d, UV_COMBOS, 0, 1, 'h')
    tf_pair = pair_index(d, TRANSFORM_COMBOS, -1, -1, 'h')

    # skin: vertex lookup, triangles, bone palette indices, sections and batches
    nl, ol = struct.unpack_from('<II', sk, 0x04)
    lookup = list(struct.unpack_from('<%dH' % nl, sk, ol))
    nt, ot = struct.unpack_from('<II', sk, 0x0C)
    tri = list(struct.unpack_from('<%dH' % nt, sk, ot))
    nprop, oprop = struct.unpack_from('<II', sk, 0x14)
    props = bytearray(sk[oprop:oprop + 4 * nprop])
    ns, _ = struct.unpack_from('<II', sk, 0x1C)
    secs = [bytearray(sk[osub + SECTION * i:osub + SECTION * (i + 1)]) for i in range(ns)]
    nb, ob = struct.unpack_from('<II', sk, 0x24)
    batches = [bytearray(sk[ob + BATCH * i:ob + BATCH * (i + 1)]) for i in range(nb)]
    eye = next(i for i, (sid, lvl, vs, vc, ist, ic) in enumerate(sections(sk)) if (sid, ic // 3) == TARGET_EYE)
    eye_batch = next(b for b in batches if struct.unpack_from('<H', b, 4)[0] == eye)
    combos = list(struct.unpack_from('<%dH' % struct.unpack_from('<I', d, BONE_COMBOS)[0], d,
                                     struct.unpack_from('<I', d, BONE_COMBOS + 4)[0]))
    nbd, obd = struct.unpack_from('<II', ms, 0x24)

    for kind, i in glows:
        used = sorted({index_of[v] for v in section_vertices(ms, i)})
        palette_bones = sorted({b for v in used for w, b in zip(d[overt + VERTEX * v + 12:overt + VERTEX * v + 16],
                                                                 d[overt + VERTEX * v + 16:overt + VERTEX * v + 20]) if w})
        palette = {b: k for k, b in enumerate(palette_bones)}
        palette_start = len(combos)
        combos += palette_bones
        local, vstart = {}, len(lookup)
        influences = 0
        for v in used:
            local[v] = len(lookup)
            lookup.append(v)
            o = overt + VERTEX * v
            ws, bs = d[o + 12:o + 16], d[o + 16:o + 20]
            props += bytes(palette[b] if w else 0 for w, b in zip(ws, bs))
            influences = max(influences, sum(1 for w in ws if w))
        start = len(tri)
        for t in section_triangles(ms, i):
            tri += [local[index_of[v]] for v in t]
        section = bytearray(secs[eye])
        struct.pack_into('<6H', section, 0, PORTED[kind], start >> 16, vstart, len(used), start & 0xFFFF, len(tri) - start)
        struct.pack_into('<HHHH', section, 12, len(palette_bones), palette_start, influences, palette_bones[0])
        donor_section = ms[dsub + SECTION * i:dsub + SECTION * (i + 1)]
        section[20:48] = donor_section[20:48]                            # centre, sort centre and radius
        secs.append(section)
        donor_batch = next(ms[obd + BATCH * b:obd + BATCH * (b + 1)] for b in range(nbd)
                           if struct.unpack_from('<H', ms, obd + BATCH * b + 4)[0] == i)
        batch = bytearray(eye_batch)
        batch[0:2] = donor_batch[0:2]                                    # flags, priority plane
        weight = struct.unpack_from('<H', eye_batch, 20)[0]
        struct.pack_into('<11H', batch, 2, 0, len(secs) - 1, len(secs) - 1, 0xFFFF, material, 0, 2,
                         tex_pairs[smoke if kind == 'smoke' else atlas], uv_pair, weight, tf_pair)
        batches.append(batch)
    if len(lookup) > 0xFFFF:
        return 'skipped: too many skin vertices'

    struct.pack_into('<II', d, BONE_COMBOS, len(combos), append_data(d, struct.pack('<%dH' % len(combos), *combos)))

    def put(field, n, payload):
        while len(sk) % 16:
            sk.append(0)
        struct.pack_into('<II', sk, field, n, len(sk))
        sk.extend(payload)
    put(0x04, len(lookup), struct.pack('<%dH' % len(lookup), *lookup))
    put(0x0C, len(tri), struct.pack('<%dH' % len(tri), *tri))
    put(0x14, len(props) // 4, bytes(props))
    put(0x1C, len(secs), b''.join(secs))
    put(0x24, len(batches), b''.join(batches))
    open(target, 'wb').write(d)
    open(skin_path, 'wb').write(sk)
    return 'glows %s added: %d vertices' % (', '.join(k for k, _ in glows), len(index_of))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common/patch-A.MPQ')
    ap.add_argument('--pack', default='D:/wow-scratch/skyborne-pack')
    a = ap.parse_args()
    for sex, fid in DONORS.items():
        target = os.path.join(a.common, 'custom', 'skyborne', 'native', sex, 'skyborne%s.m2' % sex)
        print(sex, port(target, a.pack, fid))


if __name__ == '__main__':
    main()
