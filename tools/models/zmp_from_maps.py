#!/usr/bin/env python3
"""Set a continent .zmp's zone cells from the terrain, so zones can be hovered and clicked on the continent map.

  python zmp_from_maps.py MAP_ID DATA_DIR OUT.zmp [--in IN.zmp] [--zones ID,ID,...]

A continent .zmp (Interface\\WorldMap\\<continent>.zmp) is the 128 x 128 grid CGWorldMap::GetMapAreaFromPos reads: the
client turns the cursor into world coordinates with the continent's WorldMapArea bounds, then looks up the cell for
that position. The grid covers the whole 64 x 64 tile map, rows north to south (world X) and columns west to east
(world Y), so each cell is half an ADT tile: 8 x 8 map chunks. A cell holds an AreaTable id (the client uses its zone).

DATA_DIR is a worldserver DataDir: the zone of every chunk comes from the AREA sections of maps/<MAP_ID>*.map, and
subareas are resolved to their zone with dbc/AreaTable.dbc. Each cell gets the zone most of its chunks belong to.
--zones only changes the cells of those zones (cells they win are set, cells they held but no longer win are cleared),
and leaves the rest of IN.zmp as it is; without --zones every cell is written. IN.zmp defaults to an empty grid.
It prints how many of IN.zmp's other cells agree with the terrain, as a check that the grid lines up.

Used for Open Azeroth's Kalimdor.zmp (WHE-common's Interface\\WorldMap\\Kalimdor.zmp, from OA's patch-4.MPQ), whose
grid has no Kezan cells and puts the Lost Isles' east of the island:
  python zmp_from_maps.py 1 /games/wow/256-bit-ac/data Kalimdor.zmp --in Kalimdor.oa.zmp --zones 4720,4737
An earlier version placed hand-fitted ellipses by map-image pixels, which is not how the grid is indexed."""
import argparse, collections, os, re, struct


def parents(dbc_path):
    d = open(dbc_path, "rb").read()
    _, n, fields, size, _ = struct.unpack_from("<4s4I", d)
    out = {}
    for i in range(n):
        area, _, parent = struct.unpack_from("<3I", d, 20 + i * size)
        out[area] = parent
    return out


def chunk_areas(path):
    """16 x 16 area ids of a .map tile, [chunk row][chunk column]."""
    d = open(path, "rb").read()
    off, size = struct.unpack_from("<II", d, 12)
    _, flags, grid = struct.unpack_from("<4sHH", d, off)
    if flags & 0x1:
        return [[grid] * 16 for _ in range(16)]
    v = struct.unpack_from("<256H", d, off + 8)
    return [list(v[r * 16:(r + 1) * 16]) for r in range(16)]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("map_id", type=int)
    p.add_argument("data_dir")
    p.add_argument("out")
    p.add_argument("--in", dest="inp")
    p.add_argument("--zones")
    a = p.parse_args()
    parent = parents(os.path.join(a.data_dir, "dbc", "AreaTable.dbc"))
    zone = lambda area: parent.get(area) or area  # noqa: E731

    votes = collections.defaultdict(collections.Counter)
    pat = re.compile(rf"{a.map_id:03}(\d\d)(\d\d)\.map")
    for f in os.listdir(os.path.join(a.data_dir, "maps")):
        m = pat.fullmatch(f)
        if not m:
            continue
        ty, tx = int(m.group(1)), int(m.group(2))
        for r, row in enumerate(chunk_areas(os.path.join(a.data_dir, "maps", f))):
            for c, area in enumerate(row):
                if area:
                    votes[(2 * ty + r // 8, 2 * tx + c // 8)][zone(area)] += 1
    terrain = {cell: v.most_common(1)[0][0] for cell, v in votes.items()}

    cells = list(struct.unpack("<16384I", open(a.inp, "rb").read())) if a.inp else [0] * 16384
    old = list(cells)
    zones = {int(z) for z in a.zones.split(",")} if a.zones else None
    for i in range(16384):
        t = terrain.get(divmod(i, 128), 0)
        if zones is None:
            cells[i] = t
        elif t in zones:
            cells[i] = t
        elif zone(cells[i]) in zones:
            cells[i] = 0

    others = [(i, zone(v)) for i, v in enumerate(old) if v and (zones is None or zone(v) not in zones)]
    agree = sum(1 for i, z in others if terrain.get(divmod(i, 128)) == z)
    print(f"check: {agree} of {len(others)} existing cells of other zones match the terrain")
    print(f"{sum(x != y for x, y in zip(old, cells))} cells changed"
          + ("".join(f", zone {z}: {sum(1 for v in cells if v == z)} cells" for z in sorted(zones)) if zones else ""))
    with open(a.out, "wb") as fh:
        fh.write(struct.pack("<16384I", *cells))


if __name__ == "__main__":
    main()
