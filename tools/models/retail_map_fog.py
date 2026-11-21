#!/usr/bin/env python3
"""Make a fog of war for a ported retail zone map that has none (Exile's Reach, F-137).

  python -I retail_map_fog.py ART TILES MODPAK OUT --uimap 1409 --first-id 21751 [--skip 10639,13377] [--preview DIR]

Retail draws Exile's Reach's map (UiMap 1409, art 1193) fully uncovered: it has no WorldMapOverlay rows. 3.3.5a
draws a zone's base art as its unexplored look and an overlay per explored area over it, so this script makes
both from the retail art:

- ART holds the 12 retail tiles retail_map_art.py downloaded (<name>1..12.blp, 4 x 3 tiles of 256 laid out as
  the 1002 x 668 map). They are read, never written.
- Which map pixel belongs to which area comes from the 3.3.5a tiles in TILES (<name>_X_Y.adt): each MCNK's area
  id, at the resolution of its 8 x 8 cells, with cells under water (MH2O) left out, so the sea is never fogged.
  Land cells of the zone itself (no subarea) go to the nearest subarea's land; areas listed in --skip (the
  North Sea's) get no overlay and stay unfogged.
- OUT/Interface/WorldMap/<name>/<name>1..12.blp: the base art, faded towards parchment over the land.
- OUT/Interface/WorldMap/<name>/<Area>1..N.blp: per area, the original art over its land, its edge fading out
  past the area's border, cut into the 256 x 256 pieces (the last row and column at the power of two the
  client's WorldMapFrame asks for) of its bounding box.
- MODPAK/dbc/[<tag>]_worldmapoverlay_fog.sql: the WorldMapOverlay rows, ids from --first-id in area id order.

The UiMap's WorldMapArea (name, bounds) and the areas (names, zone) are read from MODPAK's generated
[<tag>]_worldmaparea.sql and [<tag>]_areatable.sql (tools/races/retail_map_port.py). --preview writes PNG images
of the fogged map, the fully explored map and the area grid."""
import argparse, collections, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maghar_modern_prep import write_blp  # noqa: E402
from mop_map_art import read_rgba  # noqa: E402

W, H = 1002, 668                    # the 3.3.5a zone map canvas, in the base art's pixels
CELL = 533.33333 / 128              # an MCNK cell, in yards
EDGE = 6                            # an overlay fades out over this many pixels past its area's border
FADE_EDGE = 3                       # the base art's fading ends this many pixels past the land


def sql_rows(path, table):
    rows = []
    for block in re.findall(r"INSERT INTO `%s` SET(.*?);\n" % table, open(path, encoding="utf-8").read(), re.S):
        row = {}
        for k, v in re.findall(r"`(\w+)` = ('(?:[^']|'')*'|[-\d.]+)", block):
            row[k] = v[1:-1].replace("''", "'") if v.startswith("'") else float(v) if "." in v else int(v)
        rows.append(row)
    return rows


def adt_cells(path):
    """{(chunk x, chunk y): (area, [[land? per cell column] per cell row])} of one 3.3.5a ADT."""
    b = open(path, "rb").read()
    water, chunks, i = {}, [], 0
    while i < len(b) - 8:
        tag, size = b[i:i + 4], struct.unpack_from("<I", b, i + 4)[0]
        if tag == b"O2HM":
            base = i + 8
            for n in range(256):
                ofs, layers, _ = struct.unpack_from("<3I", b, base + n * 12)
                for k in range(layers if ofs else 0):
                    _, _, _, top, xo, yo, w, h, ex, _ = struct.unpack_from("<HHff4BII", b, base + ofs + k * 24)
                    bits = b[base + ex:base + ex + (w * h + 7) // 8] if ex else None
                    for r in range(h):
                        for c in range(w):
                            if bits is None or bits[(r * w + c) >> 3] >> ((r * w + c) & 7) & 1:
                                cell = (n, yo + r, xo + c)
                                water[cell] = max(water.get(cell, -1e9), top)
        elif tag == b"KNCM":
            chunks.append(i)
        i += 8 + size
    out = {}
    for i in chunks:
        ix, iy = struct.unpack_from("<II", b, i + 12)
        area = struct.unpack_from("<I", b, i + 8 + 0x34)[0]
        ofs_height = struct.unpack_from("<I", b, i + 8 + 0x14)[0]
        z = struct.unpack_from("<f", b, i + 8 + 0x70)[0]
        v = struct.unpack_from("<145f", b, i + ofs_height + 8)
        land = []
        for r in range(8):
            row = []
            for c in range(8):
                hgt = z + (v[r * 17 + c] + v[r * 17 + c + 1] + v[r * 17 + c + 17] + v[r * 17 + c + 18]
                           + v[r * 17 + c + 9]) / 5
                row.append(hgt > water.get((iy * 16 + ix, r, c), -1e9))
            land.append(row)
        out[(ix, iy)] = (area, land)
    return out


def box_alpha(mask, x0, y0, x1, y1, radius, gain):
    """min(1, gain * share of mask in the (2 radius + 1)^2 box around each pixel) over the box x0..x1, y0..y1."""
    w, h = x1 - x0, y1 - y0
    pad = [[0] * (w + 2 * radius + 1) for _ in range(h + 2 * radius + 1)]   # summed-area table, one row/col of 0
    for y in range(h + 2 * radius):
        my, acc, row, prev = y0 - radius + y, 0, pad[y + 1], pad[y]
        src = mask[my] if 0 <= my < H else None
        for x in range(w + 2 * radius):
            mx = x0 - radius + x
            acc += 1 if src is not None and 0 <= mx < W and src[mx] else 0
            row[x + 1] = prev[x + 1] + acc
    n, d = (2 * radius + 1) ** 2, 2 * radius + 1
    return [[min(1.0, gain * (pad[y + d][x + d] - pad[y][x + d] - pad[y + d][x] + pad[y][x]) / n)
             for x in range(w)] for y in range(h)]


def faded(r, g, b):
    """The unexplored look: washed out towards the parchment of 3.3.5a's unexplored zones."""
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    return tuple(int(0.25 * c + 0.75 * (95 + 0.5 * lum) * t) for c, t in ((r, 1.0), (g, 0.9), (b, 0.72)))


def save_png(path, rgba, w, h):
    import zlib
    raw = b"".join(b"\0" + bytes(rgba[y * w * 4:(y + 1) * w * 4]) for y in range(h))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def pow2(n):
    p = 16
    while p < n:
        p *= 2
    return p


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("art")
    p.add_argument("tiles")
    p.add_argument("modpak")
    p.add_argument("out")
    p.add_argument("--uimap", type=int, required=True)
    p.add_argument("--first-id", type=int, required=True)
    p.add_argument("--skip", default="", help="area ids that get no overlay (the sea's)")
    p.add_argument("--preview")
    a = p.parse_args()
    tag = re.match(r"(F-\d+)", os.path.basename(a.modpak.rstrip("/\\"))).group(1)
    dbc = os.path.join(a.modpak, "dbc")
    wma = next(r for r in sql_rows(os.path.join(dbc, f"[{tag}]_worldmaparea.sql"), "worldmaparea") if r["id"] == a.uimap)
    areas = {r["id"]: r for r in sql_rows(os.path.join(dbc, f"[{tag}]_areatable.sql"), "areatable")
             if r["id"] == wma["area_id"] or r["zone_id"] == wma["area_id"]}
    skip = {int(s) for s in a.skip.split(",") if s}
    name, left, right, top, bottom = wma["area_name"], wma["loc_left"], wma["loc_right"], wma["loc_top"], wma["loc_bottom"]

    # the cell under each map pixel's centre: map x runs from loc_left to loc_right in world Y, map y from loc_top
    # to loc_bottom in world X; cell (gx, gy) counts from the map's corner at +17066.67 yards in both
    def cell(px, py):
        wy, wx = left + (right - left) * (px + 0.5) / W, top + (bottom - top) * (py + 0.5) / H
        return int((17066.6667 - wy) / CELL), int((17066.6667 - wx) / CELL)

    gx0, gy0 = cell(0, 0)
    gx1, gy1 = cell(W - 1, H - 1)
    grid = {}                                         # (gx, gy) -> area of a land cell
    for tx in range(gx0 // 128, gx1 // 128 + 1):
        for ty in range(gy0 // 128, gy1 // 128 + 1):
            path = os.path.join(a.tiles, f"{name}_{tx}_{ty}.adt")
            if not os.path.exists(path):
                continue
            for (ix, iy), (area, land) in adt_cells(path).items():
                for r in range(8):
                    for c in range(8):
                        if land[r][c] and area in areas and area not in skip:
                            grid[((tx * 16 + ix) * 8 + c, (ty * 16 + iy) * 8 + r)] = area
    # the zone's own land goes to the nearest subarea, breadth first over land cells
    queue = collections.deque(k for k, v in grid.items() if v != wma["area_id"])
    while queue:
        gx, gy = queue.popleft()
        for k in ((gx + 1, gy), (gx - 1, gy), (gx, gy + 1), (gx, gy - 1)):
            if grid.get(k) == wma["area_id"]:
                grid[k] = grid[(gx, gy)]
                queue.append(k)
    owner = [[grid.get(cell(x, y)) for x in range(W)] for y in range(H)]
    owner = [[v if v != wma["area_id"] else None for v in row] for row in owner]

    art = bytearray(1024 * 768 * 4)
    for n in range(12):
        tw, th, src = read_rgba(os.path.join(a.art, f"{name}{n + 1}.blp"))
        assert (tw, th) == (256, 256), (n, tw, th)
        ox, oy = n % 4 * 256, n // 4 * 256
        for y in range(256):
            k = ((oy + y) * 1024 + ox) * 4
            art[k:k + 1024] = src[y * 1024:(y + 1) * 1024]

    dest = os.path.join(a.out, "Interface", "WorldMap", name)
    os.makedirs(dest, exist_ok=True)
    land = [[v is not None for v in row] for row in owner]
    fade = box_alpha(land, 0, 0, W, H, FADE_EDGE, 2.0)
    base = bytearray(art)
    for y in range(H):
        for x in range(W):
            f = fade[y][x]
            if f:
                k = (y * 1024 + x) * 4
                for c, v in enumerate(faded(*art[k:k + 3])):
                    base[k + c] = int(art[k + c] * (1 - f) + v * f)
    for n in range(12):
        ox, oy = n % 4 * 256, n // 4 * 256
        tile = b"".join(bytes(base[((oy + y) * 1024 + ox) * 4:((oy + y) * 1024 + ox + 256) * 4]) for y in range(256))
        write_blp(os.path.join(dest, f"{name}{n + 1}.blp"), 256, 256, tile)

    sql = [f"-- Generated by tools/models/retail_map_fog.py: change the script, not this file.\n"]
    explored = bytearray(base)
    oid = a.first_id
    for area in sorted({v for row in owner for v in row if v is not None}):
        mask = [[v == area for v in row] for row in owner]
        ys = [y for y in range(H) if any(mask[y])]
        xs = [x for x in range(W) if any(mask[y][x] for y in ys)]
        x0, y0 = max(0, xs[0] - EDGE), max(0, ys[0] - EDGE)
        x1, y1 = min(W, xs[-1] + EDGE + 1), min(H, ys[-1] + EDGE + 1)
        alpha = box_alpha(mask, x0, y0, x1, y1, EDGE, 4.0)
        w, h = x1 - x0, y1 - y0
        tex = re.sub(r"[^A-Za-z0-9]", "", areas[area]["name_enus"])
        across, down = (w + 255) // 256, (h + 255) // 256
        for j in range(down):
            for i in range(across):
                pw, ph = min(256, w - i * 256), min(256, h - j * 256)
                fw, fh = 256 if pw == 256 else pow2(pw), 256 if ph == 256 else pow2(ph)
                piece = bytearray(fw * fh * 4)
                for y in range(ph):
                    for x in range(pw):
                        sx, sy = x0 + i * 256 + x, y0 + j * 256 + y
                        al = alpha[sy - y0][sx - x0]
                        k, s = (y * fw + x) * 4, (sy * 1024 + sx) * 4
                        piece[k:k + 4] = bytes((art[s], art[s + 1], art[s + 2], int(255 * al)))
                        for c in range(3):
                            explored[s + c] = int(explored[s + c] * (1 - al) + art[s + c] * al)
                write_blp(os.path.join(dest, f"{tex}{j * across + i + 1}.blp"), fw, fh, piece)
        sql.append(f"""
-- {areas[area]['name_enus']}
DELETE FROM `worldmapoverlay` WHERE `id` = {oid};
INSERT INTO `worldmapoverlay` SET
  `id` = {oid},
  `map_area_id` = {a.uimap},
  `area_id_1` = {area},
  `area_id_2` = 0,
  `area_id_3` = 0,
  `area_id_4` = 0,
  `map_point_x` = 0,
  `map_point_y` = 0,
  `texture_name` = '{tex}',
  `texture_width` = {w},
  `texture_height` = {h},
  `offset_x` = {x0},
  `offset_y` = {y0},
  `hit_rect_top` = {y0},
  `hit_rect_left` = {x0},
  `hit_rect_bottom` = {y1},
  `hit_rect_right` = {x1};
""")
        print(f"{oid} {tex}: {w} x {h} at {x0}, {y0}, {across * down} pieces")
        oid += 1
    with open(os.path.join(dbc, f"[{tag}]_worldmapoverlay_fog.sql"), "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(sql))

    if a.preview:
        os.makedirs(a.preview, exist_ok=True)
        save_png(os.path.join(a.preview, "fogged.png"), base, 1024, 768)
        save_png(os.path.join(a.preview, "explored.png"), explored, 1024, 768)
        colours = {}
        grid_img = bytearray(1024 * 768 * 4)
        for y in range(H):
            for x in range(W):
                v = owner[y][x]
                if v is not None:
                    colours.setdefault(v, ((v * 97) % 200 + 55, (v * 57) % 200 + 55, (v * 31) % 200 + 55))
                    grid_img[(y * 1024 + x) * 4:(y * 1024 + x) * 4 + 4] = bytes(colours[v] + (255,))
        save_png(os.path.join(a.preview, "areas.png"), grid_img, 1024, 768)
        # the explored map must match the original art wherever there is land
        diff = max(abs(explored[(y * 1024 + x) * 4 + c] - art[(y * 1024 + x) * 4 + c])
                   for y in range(H) for x in range(W) if land[y][x] for c in range(3))
        print(f"explored vs original over land: max difference {diff}")


if __name__ == "__main__":
    main()
