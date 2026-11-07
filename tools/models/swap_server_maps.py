#!/usr/bin/env python3
"""Build the server's terrain for a terrain swap map: maps/<swap><Y><X>.map from its 3.3.5a ADTs.

  python swap_server_maps.py SWAP_MAP_ID ADT_DIR SERVER_DATA_DIR [--base-map 1] [--stage-navmesh DIR]

ADT_DIR holds the swap map's tiles as WHE-common ships them (cata_adt_to_wotlk.py output, e.g.
patch-A.MPQ/World/Maps/LostIslesPhase1). SERVER_DATA_DIR is the worldserver's DataDir: the base map's .map files are
read from its maps/ (each swap tile keeps the base tile's AREA section, so a swap never changes zone or area), the
liquid kinds from dbc/LiquidType.dbc, and the swap tiles are written to its maps/. The F-102 core patch loads a swap
tile wherever one exists, as an overlay of the base grid, for players and creatures in a swapped phase.

The map_extractor can't do this: it finds MCNKs through MCIN and expects the base map's own files, while a swap map
only has the tiles that change. This writes the same version 9 .map the extractor does (heights always as floats,
holes, liquid from MH2O), without a flight box (MFBO), like the Cataclysm tiles.

--stage-navmesh DIR builds an input tree for mmaps_generator in DIR: maps/ with the swap tiles and a copy of the base
tile for every other tile around them (ISLAND below), so a path can leave a swapped tile, and vmaps/ hard-linked from
the base map's collision under the swap id. Run mmaps_generator there for the swap map and copy the result from its
mmaps/ into the server's mmaps/. Without a swap navmesh, paths use the base map's.

A port of Zeppelin-Craft's zpaks/zep-lost-isles-terrain/build_server_maps.py for WHE's converted tiles: their
liquids are already readable by 3.3.5a, so its liquid remap tables aren't needed."""
import argparse, os, re, shutil, struct

CELLS, CELL, GRID = 16, 8, 128
MAP_VERSION, BUILD = 9, 12340
USE_MIN_HEIGHT = -500.0
LIQ_WATER, LIQ_OCEAN, LIQ_MAGMA, LIQ_SLIME, LIQ_DARK = 0x01, 0x02, 0x04, 0x08, 0x10
# Tiles around the Lost Isles the navmesh covers (ADT X 50-55, Y 28-33)
ISLAND_X, ISLAND_Y = range(50, 56), range(28, 34)


def liquid_kinds(dbc_dir):
    """LiquidType id -> Type (0 water, 1 ocean, 2 magma, 3 slime)."""
    d = open(os.path.join(dbc_dir, "LiquidType.dbc"), "rb").read()
    _, n, f, size, _ = struct.unpack_from("<4s4I", d)
    return {r[0]: r[3] for r in (struct.unpack_from("<4I", d, 20 + i * size) for i in range(n))}


def map_name(map_id, x, y):
    return f"{map_id:03}{y:02}{x:02}.map"


def base_area(path):
    d = open(path, "rb").read()
    off, size = struct.unpack_from("<II", d, 12)
    return d[off:off + size]


def convert(adt_path, area_section, kinds):
    d = open(adt_path, "rb").read()
    mhdr = struct.unpack_from("<16I", d, 20)
    mcin = 20 + mhdr[1] + 8

    v9 = [[0.0] * (GRID + 1) for _ in range(GRID + 1)]
    v8 = [[0.0] * GRID for _ in range(GRID)]
    holes = [[0] * CELLS for _ in range(CELLS)]
    for k in range(256):
        ofs = struct.unpack_from("<I", d, mcin + k * 16)[0]
        h = ofs + 8
        ix, iy = struct.unpack_from("<II", d, h + 4)
        i, j = iy, ix
        holes[i][j] = struct.unpack_from("<H", d, h + 0x3C)[0]
        base_z = struct.unpack_from("<f", d, h + 0x68 + 8)[0]
        mcvt = struct.unpack_from("<145f", d, ofs + struct.unpack_from("<I", d, h + 0x14)[0] + 8)
        for y in range(CELL + 1):
            for x in range(CELL + 1):
                v9[i * CELL + y][j * CELL + x] = base_z + mcvt[y * 17 + x]
        for y in range(CELL):
            for x in range(CELL):
                v8[i * CELL + y][j * CELL + x] = base_z + mcvt[y * 17 + 9 + x]
    lo_h = min(min(min(r) for r in v9), min(min(r) for r in v8))
    hi_h = max(max(max(r) for r in v9), max(max(r) for r in v8))

    entry = [[0] * CELLS for _ in range(CELLS)]
    flags = [[0] * CELLS for _ in range(CELLS)]
    show = [[False] * GRID for _ in range(GRID)]
    level = [[0.0] * (GRID + 1) for _ in range(GRID + 1)]
    if mhdr[10]:
        b = 20 + mhdr[10] + 8
        for i in range(CELLS):
            for j in range(CELLS):
                first, used, attrs = struct.unpack_from("<III", d, b + (i * CELLS + j) * 12)
                if not used or not first:
                    continue
                ltype, fmt, mn, _, ox, oy, w, hgt, exists_ofs, data_ofs = struct.unpack_from("<HHffBBBBII", d, b + first)
                deep = struct.unpack_from("<Q", d, b + attrs + 8)[0] if attrs else 0xFFFFFFFFFFFFFFFF
                exists = struct.unpack_from("<Q", d, b + exists_ofs)[0] if exists_ofs else 0xFFFFFFFFFFFFFFFF
                for y in range(hgt):
                    for x in range(w):
                        if exists & 1:
                            show[i * CELL + y + oy][j * CELL + x + ox] = True
                        exists >>= 1
                entry[i][j] = ltype
                kind = kinds.get(ltype)
                flags[i][j] |= {0: LIQ_WATER, 2: LIQ_MAGMA, 3: LIQ_SLIME}.get(kind, 0)
                if kind == 1:
                    flags[i][j] |= LIQ_OCEAN | (LIQ_DARK if deep else 0)
                if kind is None:
                    print(f"  {os.path.basename(adt_path)} chunk {i},{j}: liquid type {ltype} isn't in LiquidType.dbc")
                pos = 0
                for y in range(hgt + 1):
                    for x in range(w + 1):
                        value = mn  # no heights stored (depth only): the layer is flat at its minimum
                        if data_ofs and fmt in (0, 1, 3):
                            value = struct.unpack_from("<f", d, b + data_ofs + pos * 4)[0]
                        level[i * CELL + y + oy][j * CELL + x + ox] = value
                        pos += 1

    height = struct.pack("<4sIff", b"MHGT", 0 if hi_h != lo_h else 0x1, lo_h, hi_h)
    if hi_h != lo_h:
        height += b"".join(struct.pack(f"<{GRID + 1}f", *r) for r in v9)
        height += b"".join(struct.pack(f"<{GRID}f", *r) for r in v8)

    first_t, first_f = entry[0][0], flags[0][0]
    mixed = any(entry[y][x] != first_t or flags[y][x] != first_f for y in range(CELLS) for x in range(CELLS))
    liquid = b""
    if first_f or mixed:
        min_x = min_y = 255
        max_x = max_y = 0
        top, bottom = -20000.0, 20000.0
        for y in range(GRID):
            for x in range(GRID):
                if show[y][x]:
                    min_x, max_x, min_y, max_y = min(min_x, x), max(max_x, x), min(min_y, y), max(max_y, y)
                    top, bottom = max(top, level[y][x]), min(bottom, level[y][x])
                else:
                    level[y][x] = USE_MIN_HEIGHT
                    bottom = min(bottom, USE_MIN_HEIGHT)
        w, hgt = max_x - min_x + 2, max_y - min_y + 2
        fl = (0x2 if top == bottom else 0) | (0 if mixed else 0x1)
        liquid = struct.pack("<4sBBHBBBBf", b"MLIQ", fl, 0 if mixed else first_f, 0 if mixed else first_t,
                             min_x, min_y, w, hgt, bottom)
        if mixed:
            liquid += b"".join(struct.pack(f"<{CELLS}H", *r) for r in entry)
            liquid += b"".join(struct.pack(f"<{CELLS}B", *r) for r in flags)
        if not fl & 0x2:
            for y in range(hgt):
                liquid += struct.pack(f"<{w}f", *level[y + min_y][min_x:min_x + w])

    hole_bytes = b""
    if any(holes[i][j] for i in range(CELLS) for j in range(CELLS)):
        hole_bytes = b"".join(struct.pack(f"<{CELLS}H", *r) for r in holes)

    area_off = 44
    height_off = area_off + len(area_section)
    liquid_off = height_off + len(height) if liquid else 0
    holes_off = height_off + len(height) + len(liquid) if hole_bytes else 0
    header = struct.pack("<4sIIIIIIIIII", b"MAPS", MAP_VERSION, BUILD, area_off, len(area_section), height_off,
                         len(height), liquid_off, len(liquid), holes_off, len(hole_bytes))
    return header + area_section + height + liquid + hole_bytes, (lo_h, hi_h)


def stage_navmesh(stage, maps_dir, vmaps_dir, swap_id, base_map):
    for sub in ("maps", "vmaps", "mmaps"):
        path = os.path.join(stage, sub)
        if sub != "mmaps" and os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)
    smaps, svmaps = os.path.join(stage, "maps"), os.path.join(stage, "vmaps")
    for x in ISLAND_X:
        for y in ISLAND_Y:
            own, base = os.path.join(maps_dir, map_name(swap_id, x, y)), os.path.join(maps_dir, map_name(base_map, x, y))
            src = own if os.path.exists(own) else base
            if os.path.exists(src):
                shutil.copyfile(src, os.path.join(smaps, map_name(swap_id, x, y)))
            # vmtile names are ADT X_Y order, the opposite of the .map names (Zeppelin-Craft I-385)
            tile = os.path.join(vmaps_dir, f"{base_map:03}_{x:02}_{y:02}.vmtile")
            if os.path.exists(tile):
                os.link(tile, os.path.join(svmaps, f"{swap_id:03}_{x:02}_{y:02}.vmtile"))
    os.link(os.path.join(vmaps_dir, f"{base_map:03}.vmtree"), os.path.join(svmaps, f"{swap_id:03}.vmtree"))
    for f in os.listdir(vmaps_dir):
        if not f.endswith((".vmtree", ".vmtile")):
            os.link(os.path.join(vmaps_dir, f), os.path.join(svmaps, f))
    print(f"staged {stage}: run mmaps_generator {swap_id} there, then copy mmaps/ into the server's mmaps/")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("swap_map", type=int)
    p.add_argument("adt_dir")
    p.add_argument("data_dir")
    p.add_argument("--base-map", type=int, default=1)
    p.add_argument("--stage-navmesh")
    a = p.parse_args()
    maps_dir = os.path.join(a.data_dir, "maps")
    kinds = liquid_kinds(os.path.join(a.data_dir, "dbc"))
    for f in sorted(os.listdir(a.adt_dir)):
        m = re.fullmatch(r".+_(\d+)_(\d+)\.adt", f, re.I)
        if not m:
            continue
        x, y = int(m.group(1)), int(m.group(2))
        base = os.path.join(maps_dir, map_name(a.base_map, x, y))
        if not os.path.exists(base):
            print(f"{f}: no {os.path.basename(base)} to take the area from, skipped")
            continue
        data, (lo, hi) = convert(os.path.join(a.adt_dir, f), base_area(base), kinds)
        out = os.path.join(maps_dir, map_name(a.swap_map, x, y))
        with open(out, "wb") as fh:
            fh.write(data)
        print(f"{f} -> {os.path.basename(out)}  height {lo:.1f}..{hi:.1f}")
    if a.stage_navmesh:
        stage_navmesh(a.stage_navmesh, maps_dir, os.path.join(a.data_dir, "vmaps"), a.swap_map, a.base_map)


if __name__ == "__main__":
    main()
