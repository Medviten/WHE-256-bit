#!/usr/bin/env python3
"""Give a map's WDL the low-detail heights of tiles added by copying other tiles (ocean filler tiles).

  python wdl_fill.py MAP_DIR [MAP_DIR ...]

MAP_DIR is a patch's World/Maps/<map> folder holding the map's WDL and its tiles. The client draws the distant
"horizon" (CMapLowDetail) only for tiles with a MARE height block in the WDL. Tiles added to a map as byte-copies of
its existing tiles (the squished client's ocean patch fills the continents' grids with copies of open-sea tiles)
have none, so the ocean ends where the loaded tiles end. Each such tile gets the MARE (and MAHO) block of the tile
it copies; the MAOF offsets are rebuilt. The original WDL is kept as <name>.orig (move it out of the patch
folder before packing it)."""
import collections, hashlib, os, re, shutil, struct, sys


def chunks(d):
    out, at = [], 0
    while at + 8 <= len(d):
        tag = d[at:at + 4][::-1].decode("latin1")
        size = struct.unpack_from("<I", d, at + 4)[0]
        out.append((tag, at, size))
        at += 8 + size
    return out


def area_blocks(d, maof):
    """Tile index -> its MARE chunk and the MAHO chunk right after it, if any (raw bytes)."""
    out = {}
    for i, o in enumerate(maof):
        if not o:
            continue
        size = struct.unpack_from("<I", d, o + 4)[0]
        end = o + 8 + size
        if d[end:end + 4] == b"OHAM":
            end += 8 + struct.unpack_from("<I", d, end + 4)[0]
        out[i] = d[o:end]
    return out


def fill(folder):
    files = {f.lower(): f for f in os.listdir(folder)}
    wdl_name = next((f for low, f in files.items() if low.endswith(".wdl")), None)
    if not wdl_name:
        sys.exit(f"no WDL in {folder}")
    path = os.path.join(folder, wdl_name)
    original = path + ".orig"
    if not os.path.exists(original):
        shutil.copyfile(path, original)
    d = open(original, "rb").read()
    found = chunks(d)
    maof_at = next(at for tag, at, _ in found if tag == "MAOF")
    maof = struct.unpack_from("<4096I", d, maof_at + 8)
    blocks = area_blocks(d, maof)

    by_content = collections.defaultdict(list)
    for low, f in files.items():
        m = re.fullmatch(r".+_(\d+)_(\d+)\.adt", low)
        if m:
            x, y = int(m.group(1)), int(m.group(2))
            by_content[hashlib.md5(open(os.path.join(folder, f), "rb").read()).hexdigest()].append(y * 64 + x)
    added = unmatched = 0
    for tiles in by_content.values():
        source = next((blocks[t] for t in tiles if t in blocks), None)
        for t in tiles:
            if t in blocks:
                continue
            if source is None:
                unmatched += 1
                continue
            blocks[t] = source
            added += 1

    head = d[:maof_at]  # MVER and the map objects (MWMO, MWID, MODF) as they were
    at = len(head) + 8 + 4096 * 4
    offsets, body = [], bytearray()
    for i in range(4096):
        if i in blocks:
            offsets.append(at + len(body))
            body.extend(blocks[i])
        else:
            offsets.append(0)
    out = head + b"FOAM" + struct.pack("<I", 4096 * 4) + struct.pack("<4096I", *offsets) + bytes(body)
    with open(path, "wb") as fh:
        fh.write(out)
    print(f"{wdl_name}: {len(blocks) - added} tiles had heights, {added} copies given theirs"
          + (f", {unmatched} tiles copy no tile with heights" if unmatched else ""))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for folder in sys.argv[1:]:
        fill(folder)
