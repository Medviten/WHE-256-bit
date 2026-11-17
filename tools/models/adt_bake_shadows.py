#!/usr/bin/env python3
"""Bake terrain shadow maps (MCSH) into converted 3.3.5a ADTs from the doodads and WMOs placed on them.

  python -I adt_bake_shadows.py MAP_DIR --assets DIR [--assets DIR ...] [--jobs N] [--force]

Stock maps carry a baked 64 x 64 shadow bit map per terrain chunk (MCSH, MCNK flag 0x1), which is what gives Elwynn
its tree shadows; tiles converted from later expansions (F-134's Wandering Isle) have none, so only the client's
camera-dependent real-time shadows show. This projects every opaque triangle of the tile's (and its neighbours')
M2 doodads and WMO groups along a fixed sun onto the terrain height grid and sets the shadow bits it covers.
Alpha-keyed and alpha-blended materials (leaves, fences) use their texture's alpha, so canopies don't cast solid
cards; additive materials (glows) cast nothing.

The sun comes from the north-west at 45 degrees (shadows fall south-east): measured on stock Elwynn
(Azeroth_32_48 .. 33_49), where shadowed texels around 780 trees peak about 16 texels toward +row, +column.

MAP_DIR's .adt files are rewritten in place: each chunk's MCSH (empty in converted tiles) gets 512 bytes, the later
subchunk offsets, MCIN and MHDR are updated. Tiles that already have shadows are skipped unless --force; keep a
backup. --assets are folders laid out like the client's Data (WHE-common's patch-A.MPQ, a modpak's folder); models
and textures found in none of them (stock MPQ files) cast no shadow / count as opaque."""
import argparse, glob, math, multiprocessing, os, re, struct, sys

TILE, CHUNK = 533.33333, 33.333333
UNIT, TEX = CHUNK / 8, CHUNK / 64
ORIGIN = 17066.666
GRID = 16 * 64
_h = (-0.639, -0.769)
SUN = (_h[0] * math.cos(math.pi / 4), _h[1] * math.cos(math.pi / 4), -math.sin(math.pi / 4))   # direction light travels
B = chr(92)


def chunks(d, start=0, end=None):
    p, end = start, len(d) if end is None else end
    while p + 8 <= end:
        t, n = d[p:p + 4], struct.unpack_from('<I', d, p + 4)[0]
        yield t, p, n
        p += 8 + n


def names_at(d, o, n):
    out, i = {}, 0
    for raw in d[o:o + n].split(b'\0'):
        out[i] = raw.decode('latin1')
        i += len(raw) + 1
    return out


# ------------------------------------------------------------------------------------------------ files
class Assets:
    def __init__(self, roots):
        self.index = {}
        for root in roots:
            for dirpath, _, files in os.walk(root):
                rel = os.path.relpath(dirpath, root).replace(os.sep, '/').lower()
                for f in files:
                    key = (f.lower() if rel == '.' else rel + '/' + f.lower())
                    self.index.setdefault(key, os.path.join(dirpath, f))

    def find(self, game_path):
        return self.index.get(game_path.replace(B, '/').lower())


def blp_alpha(path):
    """(w, h, alpha bytes) of a small mip of a BLP2 with alpha, or None (opaque or unreadable)."""
    try:
        b = open(path, 'rb').read()
    except OSError:
        return None
    if b[:4] != b'BLP2':
        return None
    enc, depth, atype = b[8], b[9], b[10]
    w, h = struct.unpack_from('<II', b, 12)
    offs, sizes = struct.unpack_from('<16I', b, 20), struct.unpack_from('<16I', b, 84)
    level = 0
    while max(w, h) > 64 and level + 1 < 16 and offs[level + 1]:
        w, h, level = max(w // 2, 1), max(h // 2, 1), level + 1
    data = b[offs[level]:offs[level] + sizes[level]]
    if enc == 1:
        if depth == 0:
            return None
        a = data[w * h:]
        if depth == 8:
            alpha = bytes(a[:w * h])
        elif depth == 4:
            alpha = bytes(((a[i >> 1] >> (4 * (i & 1))) & 15) * 17 for i in range(w * h))
        else:
            alpha = bytes(255 if a[i >> 3] >> (i & 7) & 1 else 0 for i in range(w * h))
        return w, h, alpha
    if enc == 3:
        return w, h, bytes(data[3::4][:w * h])
    if enc != 2:
        return None
    if depth == 0:
        bs = 8
    else:
        bs = 16
    alpha = bytearray(w * h)
    p = 0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            block = data[p:p + bs]
            p += bs
            if len(block) < bs:
                return None
            if bs == 8:
                c0, c1, bits = struct.unpack_from('<HHI', block)
                vals = [0 if (c0 <= c1 and (bits >> (2 * n)) & 3 == 3) else 255 for n in range(16)]
            elif atype == 7:
                a0, a1 = block[0], block[1]
                pal = [a0, a1] + ([((6 - i) * a0 + (i + 1) * a1) // 7 for i in range(6)] if a0 > a1
                                  else [((4 - i) * a0 + (i + 1) * a1) // 5 for i in range(4)] + [0, 255])
                bits = int.from_bytes(block[2:8], 'little')
                vals = [pal[(bits >> (3 * n)) & 7] for n in range(16)]
            else:
                bits = int.from_bytes(block[:8], 'little')
                vals = [((bits >> (4 * n)) & 15) * 17 for n in range(16)]
            for j in range(4):
                for i in range(4):
                    if y + j < h and x + i < w:
                        alpha[(y + j) * w + x + i] = vals[j * 4 + i]
    if all(v >= 128 for v in alpha):
        return None
    return w, h, bytes(alpha)


class Library:
    """Triangles of models and WMOs in model space: [(alpha or None, ((x, y, z, u, v) * 3))]."""

    def __init__(self, assets):
        self.assets, self.cache, self.tex = assets, {}, {}

    def texture(self, name):
        if name not in self.tex:
            path = self.assets.find(name)
            self.tex[name] = blp_alpha(path) if path else None
        return self.tex[name]

    def m2(self, name):
        name = re.sub(r'\.(mdx|mdl)$', '.m2', name, flags=re.I)
        if name in self.cache:
            return self.cache[name]
        out = []
        path, skin_path = self.assets.find(name), self.assets.find(name[:-3] + '00.skin')
        if path and skin_path:
            d, s = open(path, 'rb').read(), open(skin_path, 'rb').read()
            if d[:4] == b'MD20' and s[:4] == b'SKIN':
                out = self._m2(d, s)
        self.cache[name] = out
        return out

    def _m2(self, d, s):
        nv, ov = struct.unpack_from('<II', d, 0x3C)
        verts = [struct.unpack_from('<3f', d, ov + 48 * i) + struct.unpack_from('<2f', d, ov + 48 * i + 32)
                 for i in range(nv)]
        nt, ot = struct.unpack_from('<II', d, 0x50)
        tex_names = []
        for i in range(nt):
            kind, _, ln, so = struct.unpack_from('<IIII', d, ot + 16 * i)
            tex_names.append(d[so:so + ln].rstrip(b'\0').decode('latin1') if kind == 0 and ln else None)
        nm, om = struct.unpack_from('<II', d, 0x70)
        blend = [struct.unpack_from('<HH', d, om + 4 * i)[1] for i in range(nm)]
        nl, ol = struct.unpack_from('<II', d, 0x80)
        lookup = struct.unpack_from('<%dH' % nl, d, ol) if nl else ()
        nlk, olk = struct.unpack_from('<II', s, 0x04)
        skin_verts = struct.unpack_from('<%dH' % nlk, s, olk)
        ni, oi = struct.unpack_from('<II', s, 0x0C)
        idx = struct.unpack_from('<%dH' % ni, s, oi)
        ns, osub = struct.unpack_from('<II', s, 0x1C)
        nb, ob = struct.unpack_from('<II', s, 0x24)
        out, seen = [], set()
        for b in range(nb):
            _, _, _, section, _, _, material, layer, count, combo = struct.unpack_from('<BbHHHhHHHH', s, ob + 24 * b)
            if layer or section in seen or section >= ns or material >= len(blend) or blend[material] >= 3:
                continue
            seen.add(section)
            alpha = None
            if blend[material] in (1, 2) and count and combo < len(lookup) and lookup[combo] < len(tex_names):
                tn = tex_names[lookup[combo]]
                alpha = self.texture(tn) if tn else None
            _, level, _, _, start, icount = struct.unpack_from('<6H', s, osub + 48 * section)
            start |= level << 16
            tri = []
            for k in range(start, min(start + icount, ni) - 2, 3):
                try:
                    tri.append(tuple(verts[skin_verts[idx[k + j]]] for j in range(3)))
                except IndexError:
                    break
            out.append((alpha, tri))
        return out

    def wmo(self, name):
        if name in self.cache:
            return self.cache[name]
        out = []
        path = self.assets.find(name)
        if path:
            d = open(path, 'rb').read()
            mats, motx, groups = [], {}, 0
            for t, p, n in chunks(d):
                if t == b'XTOM':
                    motx = names_at(d, p + 8, n)
                elif t == b'TMOM':
                    for i in range(n // 64):
                        _, _, blend, tex1 = struct.unpack_from('<IIII', d, p + 8 + 64 * i)
                        mats.append((blend, motx.get(tex1)))
                elif t == b'DHOM':
                    groups = struct.unpack_from('<I', d, p + 8 + 4)[0]
            for g in range(groups):
                gp = self.assets.find('%s_%03d.wmo' % (name[:-4], g))
                if gp:
                    out += self._group(open(gp, 'rb').read(), mats)
        self.cache[name] = out
        return out

    def _group(self, d, mats):
        mopy, movi, movt, motv = b'', (), [], []
        for t, p, n in chunks(d):
            if t != b'PGOM':
                continue
            for st, sp, sn in chunks(d, p + 8 + 0x44, p + 8 + n):
                if st == b'YPOM':
                    mopy = d[sp + 8:sp + 8 + sn]
                elif st == b'IVOM':
                    movi = struct.unpack_from('<%dH' % (sn // 2), d, sp + 8)
                elif st == b'TVOM':
                    movt = [struct.unpack_from('<3f', d, sp + 8 + 12 * i) for i in range(sn // 12)]
                elif st == b'VTOM' and not motv:
                    motv = [struct.unpack_from('<2f', d, sp + 8 + 8 * i) for i in range(sn // 8)]
        by_mat = {}
        for k in range(len(movi) // 3):
            mat = mopy[2 * k + 1] if 2 * k + 1 < len(mopy) else 0xFF
            if mat == 0xFF:
                continue
            tri = []
            for j in range(3):
                i = movi[3 * k + j]
                if i >= len(movt):
                    break
                uv = motv[i] if i < len(motv) else (0.0, 0.0)
                tri.append(movt[i] + uv)
            if len(tri) == 3:
                by_mat.setdefault(mat, []).append(tuple(tri))
        out = []
        for mat, tris in by_mat.items():
            blend, tex = mats[mat] if mat < len(mats) else (0, None)
            if blend >= 3:
                continue
            alpha = self.texture(tex) if blend in (1, 2) and tex else None
            out.append((alpha, tris))
        return out


# ------------------------------------------------------------------------------------------------ placement
def matrix(pos, rot, scale):
    """CMap::CreateDoodadDef / CreateMapObjDef: rows of v * S * Rx * Ry * Rz(+180) * T, as (3x3, translation)."""
    tx, ty, tz = ORIGIN - pos[2], ORIGIN - pos[0], pos[1]
    ax, ay, az = math.radians(rot[2]), math.radians(rot[0]), math.radians(rot[1]) + math.pi

    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    rx = [[1, 0, 0], [0, cx, sx], [0, -sx, cx]]
    ry = [[cy, 0, -sy], [0, 1, 0], [sy, 0, cy]]
    rz = [[cz, sz, 0], [-sz, cz, 0], [0, 0, 1]]
    m = mul(mul(rx, ry), rz)
    return [[v * scale for v in row] for row in m], (tx, ty, tz)


def placements(d):
    """[(kind, uniqueId, name, matrix)] of an ADT's MDDF and MODF."""
    mmdx = mwmo = {}
    mmid = mwid = ()
    out = []
    for t, p, n in chunks(d):
        if t == b'XDMM':
            mmdx = names_at(d, p + 8, n)
        elif t == b'DIMM':
            mmid = struct.unpack_from('<%dI' % (n // 4), d, p + 8)
        elif t == b'OMWM':
            mwmo = names_at(d, p + 8, n)
        elif t == b'DIWM':
            mwid = struct.unpack_from('<%dI' % (n // 4), d, p + 8)
        elif t == b'FDDM':
            for k in range(n // 36):
                nid, uid = struct.unpack_from('<II', d, p + 8 + 36 * k)
                pos, rot = struct.unpack_from('<3f', d, p + 16 + 36 * k), struct.unpack_from('<3f', d, p + 28 + 36 * k)
                scale = struct.unpack_from('<H', d, p + 40 + 36 * k)[0] / 1024.0
                if nid < len(mmid) and mmid[nid] in mmdx:
                    out.append(('m2', uid, mmdx[mmid[nid]], matrix(pos, rot, scale)))
        elif t == b'FDOM':
            for k in range(n // 64):
                nid, uid = struct.unpack_from('<II', d, p + 8 + 64 * k)
                pos, rot = struct.unpack_from('<3f', d, p + 16 + 64 * k), struct.unpack_from('<3f', d, p + 28 + 64 * k)
                if nid < len(mwid) and mwid[nid] in mwmo:
                    out.append(('wmo', uid, mwmo[mwid[nid]], matrix(pos, rot, 1.0)))
    return out


# ------------------------------------------------------------------------------------------------ terrain
class Terrain:
    """Outer height grid (129 x 129) of one tile, in world units."""

    def __init__(self, d, tx, ty):
        self.top_x, self.top_y = ORIGIN - ty * TILE, ORIGIN - tx * TILE
        self.h = [[0.0] * 129 for _ in range(129)]
        for t, p, n in chunks(d):
            if t != b'KNCM':
                continue
            ix, iy = struct.unpack_from('<II', d, p + 8 + 4)
            base = struct.unpack_from('<f', d, p + 8 + 0x70)[0]
            for st, sp, sn in chunks(d, p + 8 + 128, p + 8 + n):
                if st == b'TVCM':
                    v = struct.unpack_from('<145f', d, sp + 8)
                    for r in range(9):
                        for c in range(9):
                            self.h[iy * 8 + r][ix * 8 + c] = base + v[r * 17 + c]
                    break
                if st == b'RNCM':
                    break

    def at(self, x, y):
        r, c = (self.top_x - x) / UNIT, (self.top_y - y) / UNIT
        r, c = min(max(r, 0.0), 127.999), min(max(c, 0.0), 127.999)
        r0, c0 = int(r), int(c)
        fr, fc = r - r0, c - c0
        h = self.h
        return (h[r0][c0] * (1 - fr) * (1 - fc) + h[r0 + 1][c0] * fr * (1 - fc)
                + h[r0][c0 + 1] * (1 - fr) * fc + h[r0 + 1][c0 + 1] * fr * fc)


def bake(job):
    path, placed, roots, force = job
    d = bytearray(open(path, 'rb').read())
    tx, ty = (int(v) for v in re.search(r'_(\d+)_(\d+)\.adt$', path, re.I).groups())
    if not force and has_shadows(d):
        return os.path.basename(path), 'already has shadows'
    terrain = Terrain(d, tx, ty)
    occluders, seen = [], set()
    for kind, uid, name, mat in placed:
        if (kind, uid) not in seen:
            seen.add((kind, uid))
            occluders.append((kind, name, mat))
    if not occluders:
        return os.path.basename(path), 'nothing placed'
    lib = Library(Assets(roots))
    bits = bytearray(GRID * GRID)
    lx, ly, lz = SUN
    lo, hi = -40.0, GRID + 40.0

    def project(v, m, t):
        x = v[0] * m[0][0] + v[1] * m[1][0] + v[2] * m[2][0] + t[0]
        y = v[0] * m[0][1] + v[1] * m[1][1] + v[2] * m[2][1] + t[1]
        z = v[0] * m[0][2] + v[1] * m[1][2] + v[2] * m[2][2] + t[2]
        g = terrain.at(x, y)
        if z <= g:
            return None
        k = (z - g) / -lz
        k = max((z - terrain.at(x + k * lx, y + k * ly)) / -lz, 0.0)
        return (terrain.top_x - x - k * lx) / TEX, (terrain.top_y - y - k * ly) / TEX

    tris = 0
    for kind, name, (m, t) in occluders:
        parts = lib.m2(name) if kind == 'm2' else lib.wmo(name)
        for alpha, tri_list in parts:
            for tri in tri_list:
                pts = [project(v, m, t) for v in tri]
                if None in pts:
                    continue
                (r0, c0), (r1, c1), (r2, c2) = pts
                rmin, rmax = max(int(min(r0, r1, r2)), 0), min(int(max(r0, r1, r2)) + 1, GRID - 1)
                cmin, cmax = max(int(min(c0, c1, c2)), 0), min(int(max(c0, c1, c2)) + 1, GRID - 1)
                if rmin > rmax or cmin > cmax or min(r0, r1, r2) > hi or max(r0, r1, r2) < lo:
                    continue
                den = (r1 - r0) * (c2 - c0) - (r2 - r0) * (c1 - c0)
                if abs(den) < 1e-9:
                    continue
                tris += 1
                for r in range(rmin, rmax + 1):
                    pr = r + 0.5
                    row = r * GRID
                    for c in range(cmin, cmax + 1):
                        pc = c + 0.5
                        w1 = ((pr - r0) * (c2 - c0) - (r2 - r0) * (pc - c0)) / den
                        w2 = ((r1 - r0) * (pc - c0) - (pr - r0) * (c1 - c0)) / den
                        if w1 < 0 or w2 < 0 or w1 + w2 > 1:
                            continue
                        if alpha:
                            w0 = 1 - w1 - w2
                            u = tri[0][3] * w0 + tri[1][3] * w1 + tri[2][3] * w2
                            v = tri[0][4] * w0 + tri[1][4] * w1 + tri[2][4] * w2
                            aw, ah, ab = alpha
                            if ab[(int(v * ah) % ah) * aw + int(u * aw) % aw] < 128:
                                continue
                        bits[row + c] = 1
    write_shadows(d, bits)
    open(path, 'wb').write(d)
    return os.path.basename(path), '%d occluders, %d triangles, %d shadowed texels' % (len(occluders), tris, sum(bits))


# ------------------------------------------------------------------------------------------------ writing
def has_shadows(d):
    for t, p, n in chunks(d):
        if t == b'KNCM' and struct.unpack_from('<I', d, p + 8)[0] & 1 and struct.unpack_from('<I', d, p + 8 + 0x30)[0]:
            return True
    return False


def write_shadows(d, bits):
    """Rebuild d in place with each MCNK's MCSH filled from bits (GRID x GRID, row = north-south)."""
    out, moved = bytearray(), {}
    mcnks = []
    for t, p, n in chunks(d):
        moved[p] = len(out)
        if t != b'KNCM':
            out += d[p:p + 8 + n]
            continue
        hdr = bytearray(d[p + 8:p + 8 + 128])
        ix, iy = struct.unpack_from('<II', hdr, 4)
        mcsh = bytearray(512)
        for r in range(64):
            row = (iy * 64 + r) * GRID + ix * 64
            for c in range(64):
                if bits[row + c]:
                    mcsh[r * 8 + (c >> 3)] |= 1 << (c & 7)
        body, q, end = bytearray(), p + 8 + 128, p + 8 + n
        shadow_at = None
        while q + 8 <= end:
            st, sn = d[q:q + 4], struct.unpack_from('<I', d, q + 4)[0]
            real = 448 if st == b'RNCM' and sn == 435 else sn
            if st == b'HSCM':
                shadow_at, old = 8 + 128 + len(body), real
                body += b'HSCM' + struct.pack('<I', 512) + mcsh
            else:
                body += d[q:q + 8 + real]
            q += 8 + real
        if shadow_at is None:
            shadow_at, old = 8 + 128 + len(body), -8
            body += b'HSCM' + struct.pack('<I', 512) + mcsh
        grow = 512 - old
        # offsets (from the MCNK's own header) of subchunks after the shadow map move by its growth
        for field in (0x14, 0x18, 0x1C, 0x20, 0x24, 0x58, 0x60, 0x74):
            v = struct.unpack_from('<I', hdr, field)[0]
            if v > shadow_at:
                struct.pack_into('<I', hdr, field, v + grow)
        struct.pack_into('<II', hdr, 0x2C, shadow_at, 512)
        struct.pack_into('<I', hdr, 0, struct.unpack_from('<I', hdr, 0)[0] | 1)
        mcnks.append((len(out), 8 + 128 + len(body), iy * 16 + ix))
        out += b'KNCM' + struct.pack('<I', 128 + len(body)) + hdr + body
    for t, p, n in chunks(out):
        if t == b'NICM':
            for start, size, k in mcnks:
                struct.pack_into('<II', out, p + 8 + 16 * k, start, size)
        elif t == b'RDHM':
            for i in range(1, 12):
                v = struct.unpack_from('<I', out, p + 8 + 4 * i)[0]
                if v and v + 20 in moved:
                    struct.pack_into('<I', out, p + 8 + 4 * i, moved[v + 20] - 20)
    d[:] = out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('map_dir')
    ap.add_argument('--assets', action='append', required=True)
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    tiles = {}
    for f in glob.glob(os.path.join(a.map_dir, '*.adt')):
        m = re.search(r'_(\d+)_(\d+)\.adt$', f, re.I)
        if m:
            tiles[(int(m.group(1)), int(m.group(2)))] = f
    # read before any tile is rewritten: workers would otherwise read neighbours mid-write
    placed = {k: placements(open(f, 'rb').read()) for k, f in tiles.items()}
    jobs = []
    for (x, y), f in sorted(tiles.items()):
        near = [e for i in (-1, 0, 1) for j in (-1, 0, 1) for e in placed.get((x + i, y + j), [])]
        jobs.append((f, near, a.assets, a.force))
    with multiprocessing.Pool(a.jobs) as pool:
        for name, result in pool.imap_unordered(bake, jobs):
            print(name, result, flush=True)


if __name__ == '__main__':
    main()
