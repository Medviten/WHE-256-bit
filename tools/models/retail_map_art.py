#!/usr/bin/env python3
"""Download a retail zone map's art for the 3.3.5a world map (Exile's Reach, F-137).

  python -I retail_map_art.py CSV_DIR UIMAP NAME OUT [--version 12.1.5.70961]

CSV_DIR holds wago.tools' UiMapXMapArt, UiMapArt and UiMapArtTile exports of --version. A zone map of art style 1
(1002 x 668 in 4 x 3 tiles of 256, UiMapArtStyleLayer 1) is laid out as 3.3.5a's WorldMapArea art, so its tiles
are saved as they are: row r, column c -> OUT/Interface/WorldMap/NAME/NAME<r * 4 + c + 1>.blp, the files the client
asks for the WorldMapArea named NAME (tools/races/retail_map_port.py). Files already in OUT are kept."""
import argparse, csv, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retail_fetch import API, get  # noqa: E402


def table(csv_dir, name):
    with open(os.path.join(csv_dir, name + ".csv"), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv_dir")
    p.add_argument("uimap")
    p.add_argument("name")
    p.add_argument("out")
    p.add_argument("--version", default="12.1.5.70961")
    a = p.parse_args()
    arts = [r["UiMapArtID"] for r in table(a.csv_dir, "UiMapXMapArt") if r["UiMapID"] == a.uimap and r["PhaseID"] == "0"]
    if len(arts) != 1:
        sys.exit(f"UiMap {a.uimap} has art {arts}, not one")
    style = next(r["UiMapArtStyleID"] for r in table(a.csv_dir, "UiMapArt") if r["ID"] == arts[0])
    if style != "1":
        sys.exit(f"art {arts[0]} has style {style}, not 3.3.5a's 4 x 3 layout")
    tiles = [r for r in table(a.csv_dir, "UiMapArtTile") if r["UiMapArtID"] == arts[0] and r["LayerIndex"] == "0"]
    dest = os.path.join(a.out, "Interface", "WorldMap", a.name)
    os.makedirs(dest, exist_ok=True)
    done = 0
    for r in tiles:
        target = os.path.join(dest, "%s%d.blp" % (a.name, int(r["RowIndex"]) * 4 + int(r["ColIndex"]) + 1))
        if os.path.exists(target):
            continue
        data = get(f"{API}/casc/{r['FileDataID']}?download&version={a.version}")
        if not data or data[:4] != b"BLP2":
            sys.exit(f"tile {r['FileDataID']}: no BLP at {a.version}")
        with open(target, "wb") as fh:
            fh.write(data)
        done += 1
    print(f"{done} of {len(tiles)} tiles into {dest}")


if __name__ == "__main__":
    main()
