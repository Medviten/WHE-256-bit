#!/usr/bin/env python3
"""Make Kezan and the Lost Isles clickable on Open Azeroth's Kalimdor map (WHE-common's Interface\\WorldMap\\Kalimdor.zmp).

  python kalimdor_zmp.py OA_PATCH.mpq OUT.zmp [PREVIEW.png]     (needs Pillow, for the map tiles)

A continent .zmp is the 128 x 128 grid the client uses to tell which zone is under the cursor (CGWorldMap::
GetMapHighlight): each cell holds an AreaTable id, which the client turns into the zone's WorldMapArea. Open Azeroth's
grid has no Kezan cells, so its island is drawn but can't be clicked, and its Lost Isles cells sit east of the island
as drawn, so the west half opens Durotar or Azshara (their sea subareas, The Great Sea and others, are there).

The script reads OA's Kalimdor.zmp and its 12 Kalimdor map tiles from OA_PATCH.mpq (OA's patch-4.MPQ), clears the
Lost Isles cells and sets every cell whose centre falls inside an island's ellipse to that island. The ellipses were
fitted by hand to the islands as drawn (shore included); the island art and the parchment sea are too close in colour
to separate automatically. The preview shows the new cells on the map. Other zones' cells are left alone.

The grid is a client file, so the result goes in WHE-common, after OA's patch; without F-013 the Kezan cells do
nothing, as the client finds no WorldMapArea for them."""
import io, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpq_extract import extract  # noqa: E402

LOST_ISLES, KEZAN = 4720, 4737
# Ellipses in map pixels (the visible 1002 x 668 of the 1024 x 768 tiles): centre x, centre y, radius x, radius y
ELLIPSES = {LOST_ISLES: (756, 325, 56, 44), KEZAN: (764, 599, 47, 44)}
W, H = 1002, 668


def main(archive, out, preview=None):
    data = extract(archive, "Interface\\WorldMap\\Kalimdor.zmp")
    if data is None or len(data) != 128 * 128 * 4:
        sys.exit(f"no 128 x 128 Kalimdor.zmp in {archive}")
    cells = [0 if v == LOST_ISLES else v for v in struct.unpack("<16384I", data)]
    for zone, (cx, cy, rx, ry) in ELLIPSES.items():
        for row in range(128):
            for col in range(128):
                x, y = (col + 0.5) * W / 128, (row + 0.5) * H / 128
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    cells[row * 128 + col] = zone
    with open(out, "wb") as f:
        f.write(struct.pack("<16384I", *cells))
    old = struct.unpack("<16384I", data)
    print(f"{sum(a != b for a, b in zip(old, cells))} cells changed: "
          f"{cells.count(LOST_ISLES)} Lost Isles, {cells.count(KEZAN)} Kezan")
    if preview:
        from PIL import Image, ImageDraw
        img = Image.new("RGBA", (1024, 768))
        for i in range(12):
            tile = extract(archive, f"Interface\\WorldMap\\Kalimdor\\Kalimdor{i + 1}.blp")
            img.paste(Image.open(io.BytesIO(tile)).convert("RGBA"), ((i % 4) * 256, (i // 4) * 256))
        img = img.crop((0, 0, W, H))
        over = Image.new("RGBA", img.size)
        d = ImageDraw.Draw(over)
        for i, v in enumerate(cells):
            if v in ELLIPSES:
                r, c = divmod(i, 128)
                d.rectangle([c * W / 128, r * H / 128, (c + 1) * W / 128 - 1, (r + 1) * H / 128 - 1],
                            fill=(0, 255, 0, 80) if v == LOST_ISLES else (255, 0, 0, 80))
        Image.alpha_composite(img, over).convert("RGB").save(preview)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(*sys.argv[1:])
