#!/usr/bin/env python3
"""Place M2 models as doodads (MDDF) in converted 3.3.5a ADTs, so the client always draws them.

  python -I adt_add_doodads.py MAP_DIR MODEL X Y Z ORIENTATION [--scale 1.0] [--radius R] [--uid N] [--dry-run]

MODEL is the client path (World\\..\\x.m2 or Creature\\..\\x.m2); X Y Z ORIENTATION are world coordinates as the
server has them (a gameobject or creature spawn). The doodad goes into every tile within --radius yards (default 600)
under one uniqueId, referenced from each chunk within that radius, so it isn't culled with a single chunk. The tile's MMDX/MMID/MDDF, the chunks' MCRF and doodad counts, MCIN and MHDR are rewritten.
Rerunning with the same --uid replaces nothing: a placement whose uniqueId is already in the tile is skipped.

Why: MoP's Wandering Isle has Shen-zin Su's flippers as door gameobjects spawned out at sea. The core sends a
gameobject only once the cell it stands in is loaded, which happens near players, so the 600-yard limbs showed only
when someone passed their sea-floor origin. As map doodads the client draws them from the tile itself."""
import argparse, math, os, re, struct

ORIGIN, TILE, CHUNK = 17066.666, 533.33333, 533.33333 / 16


def chunks(d, start=0, end=None):
    p, end = start, len(d) if end is None else end
    while p + 8 <= end:
        t, n = d[p:p + 4], struct.unpack_from('<I', d, p + 4)[0]
        yield t, p, n
        p += 8 + n


def add(path, model, x, y, z, orientation, scale, radius, uid):
    d = bytearray(open(path, 'rb').read())
    tops = {bytes(t): (p, n) for t, p, n in chunks(d)}
    mmdx_p, mmdx_n = tops[b'XDMM']
    mddf_p, mddf_n = tops[b'FDDM']
    for k in range(mddf_n // 36):
        if struct.unpack_from('<I', d, mddf_p + 8 + 36 * k + 4)[0] == uid:
            return 'uid %d already placed' % uid
    names = bytes(d[mmdx_p + 8:mmdx_p + 8 + mmdx_n])
    mmid = list(struct.unpack_from('<%dI' % (tops[b'DIMM'][1] // 4), d, tops[b'DIMM'][0] + 8))
    key = model.encode('latin1') + b'\0'
    low = names.lower()
    if low.startswith(key.lower()):
        offset = 0
    else:
        at = low.find(b'\0' + key.lower())
        offset = at + 1 if at >= 0 else None
    if offset is None:
        offset, names = len(names), names + key
    name_id = mmid.index(offset) if offset in mmid else len(mmid)
    if name_id == len(mmid):
        mmid.append(offset)
    index = mddf_n // 36
    # CMap::CreateDoodadDef: world x = ORIGIN - pos.z, y = ORIGIN - pos.x, z = pos.y; yaw = rot.y + 180 degrees
    entry = struct.pack('<II3f3fHH', name_id, uid, ORIGIN - y, z, ORIGIN - x, 0.0,
                        math.degrees(orientation) - 180.0, 0.0, max(1, min(65535, round(scale * 1024))), 0)

    m = re.search(r'_(\d+)_(\d+)\.adt$', path, re.I)
    tx, ty = int(m.group(1)), int(m.group(2))
    top_x, top_y = ORIGIN - ty * TILE, ORIGIN - tx * TILE
    out, moved, mcnks = bytearray(), {}, []
    for t, p, n in chunks(d):
        moved[p] = len(out)
        if t == b'XDMM':
            out += b'XDMM' + struct.pack('<I', len(names)) + names
        elif t == b'DIMM':
            out += b'DIMM' + struct.pack('<I', 4 * len(mmid)) + struct.pack('<%dI' % len(mmid), *mmid)
        elif t == b'FDDM':
            out += b'FDDM' + struct.pack('<I', n + 36) + d[p + 8:p + 8 + n] + entry
        elif t == b'KNCM':
            hdr = bytearray(d[p + 8:p + 8 + 128])
            ix, iy = struct.unpack_from('<II', hdr, 4)
            cx, cy = top_x - (iy + 0.5) * CHUNK, top_y - (ix + 0.5) * CHUNK
            near = math.hypot(cx - x, cy - y) <= radius + CHUNK * 0.75
            body, q, end, grow, refs_at = bytearray(), p + 8 + 128, p + 8 + n, 0, None
            while q + 8 <= end:
                st, sn = d[q:q + 4], struct.unpack_from('<I', d, q + 4)[0]
                real = 448 if st == b'RNCM' and sn == 435 else sn
                if st == b'FRCM' and near:
                    ndood = struct.unpack_from('<I', hdr, 0x10)[0]
                    refs = list(struct.unpack_from('<%dI' % (sn // 4), d, q + 8))
                    refs.insert(ndood, index)
                    refs_at = 8 + 128 + len(body)
                    body += b'FRCM' + struct.pack('<I', 4 * len(refs)) + struct.pack('<%dI' % len(refs), *refs)
                    grow = 4
                else:
                    body += d[q:q + 8 + real]
                q += 8 + real
            if grow:
                struct.pack_into('<I', hdr, 0x10, struct.unpack_from('<I', hdr, 0x10)[0] + 1)
                for field in (0x14, 0x18, 0x1C, 0x20, 0x24, 0x2C, 0x58, 0x60, 0x74):
                    v = struct.unpack_from('<I', hdr, field)[0]
                    if v > refs_at:
                        struct.pack_into('<I', hdr, field, v + grow)
            mcnks.append((len(out), 8 + 128 + len(body), iy * 16 + ix))
            out += b'KNCM' + struct.pack('<I', 128 + len(body)) + hdr + body
        else:
            out += d[p:p + 8 + n]
    for t, p, n in chunks(out):
        if t == b'NICM':
            for start, size, k in mcnks:
                struct.pack_into('<II', out, p + 8 + 16 * k, start, size)
        elif t == b'RDHM':
            for i in range(1, 12):
                v = struct.unpack_from('<I', out, p + 8 + 4 * i)[0]
                if v and v + 20 in moved:
                    struct.pack_into('<I', out, p + 8 + 4 * i, moved[v + 20] - 20)
    open(path, 'wb').write(out)
    return 'placed %s as doodad %d (uid %d)' % (os.path.basename(model), index, uid)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('map_dir')
    ap.add_argument('model')
    for c in ('x', 'y', 'z', 'orientation'):
        ap.add_argument(c, type=float)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--radius', type=float, default=600.0)
    ap.add_argument('--uid', type=int, required=True)
    a = ap.parse_args()
    # every tile the radius reaches gets the doodad under the same uniqueId: the client keeps one instance per
    # uniqueId (CMap::CreateDoodadDef), and each tile's chunks then keep it from being culled with another tile
    for f in sorted(os.listdir(a.map_dir)):
        m = re.search(r'_(\d+)_(\d+)\.adt$', f, re.I)
        if not m:
            continue
        tx, ty = int(m.group(1)), int(m.group(2))
        x0, y0 = ORIGIN - (ty + 1) * TILE, ORIGIN - (tx + 1) * TILE
        dx = max(x0 - a.x, 0, a.x - (x0 + TILE))
        dy = max(y0 - a.y, 0, a.y - (y0 + TILE))
        if math.hypot(dx, dy) <= a.radius:
            print(f, add(os.path.join(a.map_dir, f), a.model, a.x, a.y, a.z, a.orientation, a.scale, a.radius,
                         a.uid))


if __name__ == '__main__':
    main()
