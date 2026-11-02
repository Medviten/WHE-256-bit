#!/usr/bin/env python3
"""Convert F-037's modern (BfA) Mag'har models and textures to the layout the character compositor paints on.

The models use retail's 1024x512 atlas: the left half is the stock atlas squeezed to half width, the right half the
whole head. The compositor pastes at the stock section rectangles (s_sectionInfoRaw) and only takes palettized BLPs
(TextureCacheGetPal), so faces land on the shins, underwear and armour on the head and the DXT skins don't paste.

Models (all skin profiles, patched in place because wotlkconv's write path isn't byte-identical):
- UVs of skin-textured batches: body u * 2, head into the stock head rectangles (u - 0.5, 0.625 + v * 0.375)
- geosets the stock path doesn't manage: head, eyes, tusks, feet and torso defaults become 0, other variants of those
  groups are parked in group 19 (hidden by SetGeometryVisible(0, 2000, 0), never shown again)
- texture slots: retail eye slots (type 11) and the custom\\maghar\\ paths point at files that exist

Textures (rewritten as 8-bit palette + 8-bit alpha with full mip chains):
- skin: the left half, with the head painted into the stock head rectangles
- face: each whole-head file split into an upper (256x64) and a new lower (256x128) texture
- underwear: same layout as stock, palettized only

usage: maghar_modern_prep.py [--common PATH] [--jobs N]
Already converted files are skipped, so it can be rerun; restore with git in WHE-common to start over."""
import argparse, glob, multiprocessing, os, shutil, struct, sys

SLASH = chr(92)
PARKED = 1999
KEEP = {3202, 3301, 4001, 2001, 2201}                # head with ear holes, eyes, smallest tusks, bare feet, bare torso
MODELS = (('male', 'orcmaleupright'), ('male', 'orcmale_hd'), ('female', 'orcfemale_hd'))
EYE_COLOR = 'male/orcmale_hd_eye_color_5273683.blp'
# gender -> {name part of the missing custom\maghar\ slot: file in the model's folder}
SLOTS = {
    'male': {'3548970': 'orcmale_hd_3548970.blp', '3623305': 'orcmale_hd_3548970.blp',
             '4531025': 'orcmale_hd_eyesight_5148993.blp', 'eyereflect': 'orcmale_hd_eyereflect.blp'},
    'female': {'3540975': 'orcfemale_hd_3540975.blp', '3687546': 'orcfemale_hd_3540975.blp',
               '3687547': 'orcfemale_hd_3540975.blp', '4531027': 'orcfemale_hd_eyesight_5148991.blp',
               'eyereflect': 'orcfemale_hd_eyereflect.blp'},
}
PACKAGE = 'D:/Downloads/Downloads/Races/Kalibros_Races_20261012/Character/orc'     # source of the slot files above


# ------------------------------------------------------------------------------------------------ BLP
def read_dxt(path):
    """(w, h, rgba) of a BLP's top level; None when it isn't DXT (already converted)."""
    b = open(path, 'rb').read()
    enc, adepth, atype = b[8], b[9], b[10]
    w, h = struct.unpack_from('<II', b, 12)
    if enc != 2:
        return None
    off, size = struct.unpack_from('<I', b, 20)[0], struct.unpack_from('<I', b, 84)[0]
    data = b[off:off + size]
    bs = 8 if adepth == 0 else 16
    out = bytearray(w * h * 4)
    p = 0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            block = data[p:p + bs]
            p += bs
            alpha = None
            if bs == 16:
                if atype == 7:                                   # DXT5
                    a0, a1 = block[0], block[1]
                    pal = [a0, a1] + ([((6 - i) * a0 + (i + 1) * a1) // 7 for i in range(6)] if a0 > a1
                                      else [((4 - i) * a0 + (i + 1) * a1) // 5 for i in range(4)] + [0, 255])
                    bits = int.from_bytes(block[2:8], 'little')
                    alpha = [pal[(bits >> (3 * i)) & 7] for i in range(16)]
                else:                                            # DXT3
                    bits = int.from_bytes(block[:8], 'little')
                    alpha = [((bits >> (4 * i)) & 15) * 17 for i in range(16)]
            c0, c1, bits = struct.unpack_from('<HHI', block, bs - 8)
            e0 = ((c0 >> 11) * 255 // 31, ((c0 >> 5) & 63) * 255 // 63, (c0 & 31) * 255 // 31)
            e1 = ((c1 >> 11) * 255 // 31, ((c1 >> 5) & 63) * 255 // 63, (c1 & 31) * 255 // 31)
            if c0 > c1 or bs == 16:
                cols = [e0, e1, tuple((2 * a + b_) // 3 for a, b_ in zip(e0, e1)), tuple((a + 2 * b_) // 3 for a, b_ in zip(e0, e1))]
            else:
                cols = [e0, e1, tuple((a + b_) // 2 for a, b_ in zip(e0, e1)), (0, 0, 0)]
            for j in range(4):
                if y + j >= h:
                    break
                for i in range(4):
                    if x + i >= w:
                        break
                    n = j * 4 + i
                    r, g, b_ = cols[(bits >> (2 * n)) & 3]
                    k = ((y + j) * w + x + i) * 4
                    out[k], out[k + 1], out[k + 2] = r, g, b_
                    out[k + 3] = alpha[n] if alpha else 255
    return w, h, out


def crop_scale(src, sw, sx, sy, cw, ch, dw, dh):
    """Box-filtered copy of the crop (sx, sy, cw, ch) of an RGBA image of width sw, at dw x dh."""
    out = bytearray(dw * dh * 4)
    for y in range(dh):
        y0, y1 = sy + y * ch // dh, sy + max((y + 1) * ch // dh, y * ch // dh + 1)
        for x in range(dw):
            x0, x1 = sx + x * cw // dw, sx + max((x + 1) * cw // dw, x * cw // dw + 1)
            total = [0, 0, 0, 0]
            for yy in range(y0, y1):
                row = yy * sw * 4
                for xx in range(x0, x1):
                    k = row + xx * 4
                    total[0] += src[k]
                    total[1] += src[k + 1]
                    total[2] += src[k + 2]
                    total[3] += src[k + 3]
            n = (y1 - y0) * (x1 - x0)
            k = (y * dw + x) * 4
            out[k], out[k + 1], out[k + 2], out[k + 3] = total[0] // n, total[1] // n, total[2] // n, total[3] // n
    return out


def palette_of(rgba):
    """Median cut over a 5-6-5 colour histogram: up to 256 (r, g, b)."""
    hist = {}
    for k in range(0, len(rgba), 4):
        key = (rgba[k] >> 3, rgba[k + 1] >> 2, rgba[k + 2] >> 3)
        hist[key] = hist.get(key, 0) + 1
    boxes = [list(hist.items())]
    while len(boxes) < 256:
        best, axis, spread = None, 0, -1
        for i, box in enumerate(boxes):
            if len(box) < 2:
                continue
            for a in range(3):
                vals = [c[0][a] << (3 if a != 1 else 2) for c in box]
                s = max(vals) - min(vals)
                if s > spread:
                    best, axis, spread = i, a, s
        if best is None:
            break
        box = sorted(boxes[best], key=lambda c: c[0][axis])
        half, seen, cut = sum(c[1] for c in box) / 2, 0, 1
        for i, c in enumerate(box):
            seen += c[1]
            if seen >= half:
                cut = max(1, min(i, len(box) - 1))
                break
        boxes[best:best + 1] = [box[:cut], box[cut:]]
    pal = []
    for box in boxes:
        n = sum(c[1] for c in box)
        pal.append(tuple(min(255, round(sum(((c[0][a] << (3 if a != 1 else 2)) + (4 if a != 1 else 2)) * c[1] for c in box) / n)) for a in range(3)))
    return pal


def write_blp(path, w, h, rgba):
    """BLP2, palette + 8-bit alpha, full mip chain: the format of the working races' compositor textures."""
    pal = palette_of(rgba)
    cache = {}

    def nearest(r, g, b):
        key = (r >> 2, g >> 2, b >> 2)
        hit = cache.get(key)
        if hit is None:
            hit = min(range(len(pal)), key=lambda i: (pal[i][0] - r) ** 2 + (pal[i][1] - g) ** 2 + (pal[i][2] - b) ** 2)
            cache[key] = hit
        return hit

    levels = []
    cur, cw, ch = rgba, w, h
    while True:
        idx = bytearray(cw * ch)
        alpha = bytearray(cw * ch)
        for i in range(cw * ch):
            k = i * 4
            idx[i] = nearest(cur[k], cur[k + 1], cur[k + 2])
            alpha[i] = cur[k + 3]
        levels.append(bytes(idx) + bytes(alpha))
        if cw == 1 and ch == 1:
            break
        nw, nh = max(cw // 2, 1), max(ch // 2, 1)
        cur, cw, ch = crop_scale(cur, cw, 0, 0, cw, ch, nw, nh), nw, nh
    offs, sizes, at = [0] * 16, [0] * 16, 148 + 1024
    for i, level in enumerate(levels):
        offs[i], sizes[i] = at, len(level)
        at += len(level)
    head = struct.pack('<4sIBBBBII', b'BLP2', 1, 1, 8, 8, 1, w, h) + struct.pack('<16I', *offs) + struct.pack('<16I', *sizes)
    palette = b''.join(struct.pack('<4B', c[2], c[1], c[0], 255) for c in pal) + b'\0' * (4 * (256 - len(pal)))
    with open(path + '.tmp', 'wb') as f:
        f.write(head + palette + b''.join(levels))
    os.replace(path + '.tmp', path)


def convert_skin(path):
    img = read_dxt(path)
    if img is None:
        return 0
    w, h, src = img
    assert (w, h) == (1024, 512), path
    out = crop_scale(src, w, 0, 0, 512, 512, 512, 512)
    head = crop_scale(src, w, 512, 0, 512, 512, 256, 192)
    for y in range(192):
        k = (320 + y) * 512 * 4
        out[k:k + 256 * 4] = head[y * 256 * 4:(y + 1) * 256 * 4]
    write_blp(path, 512, 512, out)
    return 1


def convert_face(path):
    img = read_dxt(path)
    if img is None:
        return 0
    w, h, src = img
    assert (w, h) == (512, 512), path
    third = h // 3
    lower = os.path.join(os.path.dirname(path), os.path.basename(path).replace('faceupper', 'facelower'))
    write_blp(lower, 256, 128, crop_scale(src, w, 0, third, w, h - third, 256, 128))
    write_blp(path, 256, 64, crop_scale(src, w, 0, 0, w, third, 256, 64))
    return 1


def convert_plain(path):
    img = read_dxt(path)
    if img is None:
        return 0
    write_blp(path, *img)
    return 1


def convert(job):
    kind, path = job
    return {'skin': convert_skin, 'face': convert_face, 'plain': convert_plain}[kind](path)


# ---------------------------------------------------------------------------------------------- model
def convert_model(folder, gender, base):
    m2 = os.path.join(folder, gender, base + '.m2')
    d = bytearray(open(m2, 'rb').read())
    skins = [os.path.join(folder, gender, '%s0%d.skin' % (base, p)) for p in range(4)]
    skins = [s for s in skins if os.path.exists(s)]
    nv, ov = struct.unpack_from('<II', d, 0x3C)
    nt, ot = struct.unpack_from('<II', d, 0x50)
    nl, ol = struct.unpack_from('<II', d, 0x80)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    lookup = struct.unpack_from('<%dH' % nl, d, ol)

    body = set()
    changed = 0
    for path in skins:
        s = bytearray(open(path, 'rb').read())
        (cv, ov2, ci, oi, _, _, ns, os_, nb, ob, _) = struct.unpack_from('<11I', s, 4)
        vmap = struct.unpack_from('<%dH' % cv, s, ov2)
        idx = struct.unpack_from('<%dH' % ci, s, oi)
        for b in range(nb):
            field = struct.unpack_from('<BBHHHhHHHHHHH', s, ob + 24 * b)
            if types[lookup[field[9]]] == 1:
                sid, level, _, _, ts, tc = struct.unpack_from('<6H', s, os_ + 48 * field[3])
                start = ts | (level << 16)
                body.update(vmap[idx[j]] for j in range(start, start + tc))
        for i in range(ns):
            at = os_ + 48 * i
            sid = struct.unpack_from('<H', s, at)[0]
            new = 0 if sid in KEEP else (PARKED if sid >= 2000 else sid)
            if new != sid:
                struct.pack_into('<H', s, at, new)
                changed += 1
        open(path, 'wb').write(s)
    if not changed:
        return 'already converted'

    head = 0
    for v in body:
        at = ov + 48 * v + 32
        u, w = struct.unpack_from('<2f', d, at)
        if u < 0.5:
            struct.pack_into('<2f', d, at, u * 2, w)
        else:
            struct.pack_into('<2f', d, at, u - 0.5, 0.625 + w * 0.375)
            head += 1

    # texture slots: file names go at the end of the file, the loader relocates them like any other
    prefix = SLASH.join(('Character', 'magharorc'))
    for i in range(nt):
        at = ot + 16 * i
        typ, flags, length, offset = struct.unpack_from('<4I', d, at)
        name = bytes(d[offset:offset + length]).rstrip(b'\0').decode('latin1') if length else ''
        target = None
        if typ == 0 and name.lower().startswith('custom'):
            part = name.rsplit(SLASH, 1)[-1].lower()
            hit = [v for k, v in SLOTS[gender].items() if k in part]
            assert len(hit) == 1, name
            target = SLASH.join((prefix, gender, hit[0]))
        if target is not None or (typ == 11 and is_eye_slot(s_for_eyes(skins[0]), lookup, i)):
            target = target or SLASH.join((prefix, *EYE_COLOR.split('/')))
            raw = target.encode('latin1') + b'\0'
            struct.pack_into('<4I', d, at, 0, flags, len(raw), len(d))
            d += raw
    open(m2, 'wb').write(d)
    return 'sections changed %d, body verts %d (head %d)' % (changed, len(body), head)


def fix_eye_batches(folder, gender, base):
    """The eye batch samples its texture twice (retail's two-layer eye shader), which multiplies the dark orange towards
    black: draw it once."""
    d = open(os.path.join(folder, gender, base + '.m2'), 'rb').read()
    nt, ot = struct.unpack_from('<II', d, 0x50)
    nl, ol = struct.unpack_from('<II', d, 0x80)
    lookup = struct.unpack_from('<%dH' % nl, d, ol)
    eye = set()
    for i in range(nt):
        _, _, length, offset = struct.unpack_from('<4I', d, ot + 16 * i)
        if b'eye_color' in d[offset:offset + length]:
            eye.add(i)
    fixed = 0
    for path in glob.glob(os.path.join(folder, gender, base + '0?.skin')):
        s = bytearray(open(path, 'rb').read())
        (_, _, _, _, _, _, _, _, nb, ob, _) = struct.unpack_from('<11I', s, 4)
        for b in range(nb):
            field = struct.unpack_from('<BBHHHhHHHHHHH', s, ob + 24 * b)
            if field[8] == 2 and lookup[field[9]] in eye:
                struct.pack_into('<H', s, ob + 24 * b + 14, 1)
                fixed += 1
        if fixed:
            open(path, 'wb').write(s)
    return fixed


def fix_eye_glow(folder, gender, base):
    """The client shows geoset 1703 for death knights, but on these models that's a gold glow and the blue one is 1701,
    which the client also leaves on for a facial style without a row (m_geosets[17] keeps its 1701 default). Make the blue
    one 1703 and park the rest, so only death knights glow, in blue."""
    moved = 0
    for path in glob.glob(os.path.join(folder, gender, base + '0?.skin')):
        s = bytearray(open(path, 'rb').read())
        (_, _, _, _, _, _, ns, os_, _, _, _) = struct.unpack_from('<11I', s, 4)
        ids = [struct.unpack_from('<H', s, os_ + 48 * i)[0] for i in range(ns)]
        if 1701 not in ids:
            continue
        for i, sid in enumerate(ids):
            new = {1701: 1703, 1702: PARKED, 1703: PARKED, 1704: PARKED, 1705: PARKED}.get(sid, sid)
            if new != sid:
                struct.pack_into('<H', s, os_ + 48 * i, new)
                moved += 1
        open(path, 'wb').write(s)
    return moved


def s_for_eyes(path):
    return open(path, 'rb').read()


def is_eye_slot(s, lookup, slot):
    """Whether the eye geoset (kept as 0 by now, found by its original 192-triangle batch) samples this texture slot."""
    (_, _, _, _, _, _, ns, os_, nb, ob, _) = struct.unpack_from('<11I', s, 4)
    for b in range(nb):
        field = struct.unpack_from('<BBHHHhHHHHHHH', s, ob + 24 * b)
        if lookup[field[9]] == slot and struct.unpack_from('<H', s, os_ + 48 * field[3])[0] == 0:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common')
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    folder = os.path.join(a.common, 'patch-A.MPQ', 'Character', 'magharorc')
    for gender, files in SLOTS.items():
        for name in set(files.values()):
            dst = os.path.join(folder, gender, name)
            if not os.path.exists(dst):
                shutil.copy2(os.path.join(PACKAGE, gender, name), dst)
    for gender, base in MODELS:
        print(base, convert_model(folder, gender, base), '- eye batches fixed:', fix_eye_batches(folder, gender, base),
              '- glow sections moved:', fix_eye_glow(folder, gender, base), flush=True)
    jobs = []
    for gender in ('male', 'female'):
        g = os.path.join(folder, gender)
        jobs += [('skin', f) for f in glob.glob(os.path.join(g, 'orc%sclanskin*.blp' % gender))]
        jobs += [('face', f) for f in glob.glob(os.path.join(g, 'orc%sclanfaceupper*.blp' % gender))]
        jobs += [('plain', f) for pat in ('nakedtorsoskin', 'nakedpelvisskin') for f in glob.glob(os.path.join(g, 'orc%sclan%s*.blp' % (gender, pat)))]
    with multiprocessing.Pool(a.jobs) as pool:
        done = sum(pool.imap_unordered(convert, jobs, 4))
    print('textures: %d jobs, %d converted' % (len(jobs), done))


if __name__ == '__main__':
    sys.exit(main())
