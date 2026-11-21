#!/usr/bin/env python3
"""Place a WMO (MODF) in converted 3.3.5a ADTs, the way adt_add_doodads.py places M2s.

  python -I adt_add_wmo.py MAP_DIR WMO X Y Z YAW --uid N [--radius 60] [--like-stock]

WMO is the client path (World\\wmo\\...\\x.wmo); X Y Z are world coordinates of the WMO's origin as the server has them
(.gps), YAW the MODF rotation about the vertical in degrees (the value the ADT stores: the stock Durotar zeppelin tower
has -74.53). The placement goes into every tile of MAP_DIR within --radius yards of X Y, under one uniqueId (the client
keeps one instance per uniqueId), and is referenced from every chunk within that radius so it isn't culled. The tile's
MWMO/MWID/MODF, the chunks' MCRF and map-object counts, MCIN and MHDR are rewritten. A tile already holding the uniqueId
is left alone, so reruns change nothing.

The MODF bounding box is a square of --radius around the origin, from Z - 5 to Z + --height (default 80): only used
for culling, so it errs on the large side."""
import argparse, math, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adt_add_doodads import chunks, ORIGIN, TILE, CHUNK  # noqa: E402

MCNK_DOODAD_REFS, MCNK_MAPOBJ_REFS = 0x10, 0x38


def add(path, model, x, y, z, yaw, uid, radius, height):
    d = bytearray(open(path, 'rb').read())
    tops = {bytes(t): (p, n) for t, p, n in chunks(d)}
    mwmo_p, mwmo_n = tops[b'OMWM']
    modf_p, modf_n = tops[b'FDOM']
    for k in range(modf_n // 64):
        if struct.unpack_from('<I', d, modf_p + 8 + 64 * k + 4)[0] == uid:
            return 'uid %d already placed' % uid
    names = bytes(d[mwmo_p + 8:mwmo_p + 8 + mwmo_n])
    mwid = list(struct.unpack_from('<%dI' % (tops[b'DIWM'][1] // 4), d, tops[b'DIWM'][0] + 8))
    key = model.encode('latin1') + b'\0'
    low = names.lower()
    offset = 0 if low.startswith(key.lower()) else None
    if offset is None:
        at = low.find(b'\0' + key.lower())
        offset = at + 1 if at >= 0 else None
    if offset is None:
        offset, names = len(names), names + key
    name_id = mwid.index(offset) if offset in mwid else len(mwid)
    if name_id == len(mwid):
        mwid.append(offset)
    index = modf_n // 64
    # MODF: position in ADT axes (ORIGIN - y, z, ORIGIN - x), rotation in degrees, extents in the same axes
    px, pz = ORIGIN - y, ORIGIN - x
    entry = struct.pack('<II3f3f3f3fHHHH', name_id, uid, px, z, pz, 0.0, yaw, 0.0,
                        px - radius, z - 5.0, pz - radius, px + radius, z + height, pz + radius, 0, 0, 0, 1024)

    m = re.search(r'_(\d+)_(\d+)\.adt$', path, re.I)
    tx, ty = int(m.group(1)), int(m.group(2))
    top_x, top_y = ORIGIN - ty * TILE, ORIGIN - tx * TILE
    out, moved, mcnks, refd = bytearray(), {}, [], 0
    for t, p, n in chunks(d):
        moved[p] = len(out)
        if t == b'OMWM':
            out += b'OMWM' + struct.pack('<I', len(names)) + names
        elif t == b'DIWM':
            out += b'DIWM' + struct.pack('<I', 4 * len(mwid)) + struct.pack('<%dI' % len(mwid), *mwid)
        elif t == b'FDOM':
            out += b'FDOM' + struct.pack('<I', n + 64) + d[p + 8:p + 8 + n] + entry
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
                    refs = list(struct.unpack_from('<%dI' % (sn // 4), d, q + 8))
                    refs.append(index)          # doodad refs first, then map objects: the new one goes last
                    refs_at = 8 + 128 + len(body)
                    body += b'FRCM' + struct.pack('<I', 4 * len(refs)) + struct.pack('<%dI' % len(refs), *refs)
                    grow = 4
                else:
                    body += d[q:q + 8 + real]
                q += 8 + real
            if grow:
                refd += 1
                struct.pack_into('<I', hdr, MCNK_MAPOBJ_REFS, struct.unpack_from('<I', hdr, MCNK_MAPOBJ_REFS)[0] + 1)
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
    assert refd, 'no chunk of %s within %d yards' % (path, radius)
    open(path, 'wb').write(out)
    return 'placed %s as map object %d (uid %d), referenced from %d chunks' % (os.path.basename(model), index, uid, refd)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('map_dir')
    ap.add_argument('model')
    for c in ('x', 'y', 'z', 'yaw'):
        ap.add_argument(c, type=float)
    ap.add_argument('--uid', type=int, required=True)
    ap.add_argument('--radius', type=float, default=60.0)
    ap.add_argument('--height', type=float, default=80.0)
    a = ap.parse_args()
    for f in sorted(os.listdir(a.map_dir)):
        m = re.search(r'_(\d+)_(\d+)\.adt$', f, re.I)
        if not m:
            continue
        tx, ty = int(m.group(1)), int(m.group(2))
        x0, y0 = ORIGIN - (ty + 1) * TILE, ORIGIN - (tx + 1) * TILE
        dx = max(x0 - a.x, 0, a.x - (x0 + TILE))
        dy = max(y0 - a.y, 0, a.y - (y0 + TILE))
        if math.hypot(dx, dy) <= a.radius:
            print(f, add(os.path.join(a.map_dir, f), a.model, a.x, a.y, a.z, a.yaw, a.uid, a.radius, a.height))


if __name__ == '__main__':
    main()
