#!/usr/bin/env python3
"""Download Mists of Pandaria's world map art for a map (and the World map) into a client patch folder.

  python mop_map_art.py MOP_DBC_DIR OUT [--map 870] [--world] [--version 5.5.4.70631]

OUT is a patch-shaped folder, for F-133 WHE-common's modpaks/F-133_mop-pandaria: files go to
OUT/Interface/WorldMap/<map>/<file>.blp, named as the 3.3.5 client asks for them. Which files: for every WorldMapArea of --map that F-133 keeps (no dungeon floors or
phase copies), its 12 tiles (<name>1..12) and the highlight the parent map shows on hover (<name>Highlight:
a zone's on its continent, a continent's on the World map); for every WorldMapOverlay of those, its 256 x 256 pieces (<texture>1..N, N = tiles across x down);
with --world, the World map's 12 tiles and the Eastern Kingdoms', Kalimdor's and Northrend's highlights (MoP's,
drawn for the continent placement F-133 moves them to). MOP_DBC_DIR holds the 5.4.8 DBCs the rows come from.

The files come from wago.tools at --version, by default MoP Classic's (its map art is MoP's; the newest version of
the World tiles is Legion's, with the Broken Isles). Their community listfile names are looked up per folder.
Files already in OUT are kept.

--uimap CSV (MoP Classic's UiMapAssignment, https://wago.tools/db2/UiMapAssignment/csv?build=5.5.4.70631; give
mop_map_port.py the same file) re-lays the continents' World map highlights for the 3.3.5 client. MoP Classic draws
one in a box of the World map's 3:2 aspect, as tall as the continent's UiMapAssignment region and centred on it, from
the texture's top 512 x 341 band; 3.3.5 samples the top-left square part the region's tile aspect gives
(Script_UpdateMapHighlight) over the region itself, so tall continents came out a third too small and shifted. Each
highlight still in MoP's band is resampled so the 3.3.5 rectangle shows what MoP Classic draws there."""
import argparse, csv, math, os, sys, urllib.parse, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "races"))
from retail_fetch import API, get  # noqa: E402
from cata406_dbc_port import Dbc  # noqa: E402


def wanted(mop_dbc, map_id, world):
    """{folder: [file names without .blp]}"""
    wma = Dbc(os.path.join(mop_dbc, "WorldMapArea.dbc"))
    wmo = Dbc(os.path.join(mop_dbc, "WorldMapOverlay.dbc"))
    out, folder_of = {}, {}
    for r in wma.records:
        if r[1] != map_id or r[9] or r[10] not in (0, -1):
            continue
        name = wma.s(r[3])
        folder_of[r[0]] = name
        out[name] = [f"{name}{i}" for i in range(1, 13)] + [f"{name}Highlight"]
    for r in wmo.records:
        if r[1] in folder_of:
            tex = wmo.s(r[6])
            n = math.ceil(r[7] / 256) * math.ceil(r[8] / 256)
            out[folder_of[r[1]]] += [f"{tex}{i}" for i in range(1, n + 1)]
    if world:
        out["World"] = [f"World{i}" for i in range(1, 13)]
        # the other continents' World map highlights: drawn for MoP's WorldMapContinent bounds, which F-133 uses
        for r in wma.records:
            if r[1] in (0, 1, 571) and not r[2] and r[10] in (0, -1):
                out.setdefault(wma.s(r[3]), []).append(f"{wma.s(r[3])}Highlight")
    return out


CONTINENT_FOLDERS = {0: "Azeroth", 1: "Kalimdor", 571: "Northrend", 870: "Pandaria"}


def read_rgba(path):
    from maghar_modern_prep import read_dxt
    from mop_bake_prep import read_pal
    b = open(path, "rb").read()
    if b[8] == 2 and b[10] == 0 and b[9]:     # DXT1 with 1-bit alpha: read_dxt takes alpha depth for 16-byte blocks
        tmp = path + ".dxt1.tmp"
        open(tmp, "wb").write(b[:9] + b"\0" + b[10:])
        try:
            return read_dxt(tmp)
        finally:
            os.remove(tmp)
    return read_dxt(path) or read_pal(path)


def relayout_highlights(out, uimap):
    from maghar_modern_prep import write_blp
    done = 0
    for r in csv.DictReader(open(uimap, encoding="utf-8")):
        if r["UiMapID"] != "947" or int(r["MapID"]) not in CONTINENT_FOLDERS:
            continue
        name = CONTINENT_FOLDERS[int(r["MapID"])]
        path = os.path.join(out, "Interface", "WorldMap", name, name + "Highlight.blp")
        if not os.path.exists(path):
            continue
        w, h, src = read_rgba(path)
        band = h * 668 / 1002                              # the part of the texture MoP Classic uses
        if any(src[(y * w + x) * 4 + c] > 60 for y in range(int(band) + 6, h) for x in range(0, w, 4) for c in range(3)):
            continue                                       # already re-laid: content below the band
        f = {k: float(v) for k, v in r.items() if k.startswith(("Ui", "Region"))}
        tiles_w = (f["Region_4"] - f["Region_1"]) / 533.3333       # region size in ADT tiles
        tiles_h = (f["Region_3"] - f["Region_0"]) / 533.3333
        tcx, tcy = (tiles_w / tiles_h, 1.0) if tiles_h >= tiles_w else (1.0, tiles_h / tiles_w)
        rx0, ry0 = f["UiMin_0"] * 1002, f["UiMin_1"] * 668
        rw, rh = (f["UiMax_0"] - f["UiMin_0"]) * 1002, (f["UiMax_1"] - f["UiMin_1"]) * 668
        bh = rh                                            # MoP Classic's box: 3:2, region height, centred
        bw = bh * 1002 / 668
        bx0 = rx0 + rw / 2 - bw / 2
        dst = bytearray(w * h * 4)
        for j in range(int(tcy * h)):
            py = ry0 + (j + 0.5) / (tcy * h) * rh
            v = int((py - ry0) / bh * band)
            for i in range(int(tcx * w)):
                px = rx0 + (i + 0.5) / (tcx * w) * rw
                u = int((px - bx0) / bw * w)
                if 0 <= u < w and 0 <= v < h:
                    k, s = (j * w + i) * 4, (v * w + u) * 4
                    dst[k:k + 4] = src[s:s + 4]
        write_blp(path, w, h, dst)
        done += 1
    print(f"re-laid {done} continent highlights for the 3.3.5 World map")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mop_dbc")
    p.add_argument("out")
    p.add_argument("--map", type=int, default=870)
    p.add_argument("--world", action="store_true")
    p.add_argument("--version", default="5.5.4.70631")
    p.add_argument("--uimap")
    a = p.parse_args()
    missing = []
    count = 0
    for folder, names in wanted(a.mop_dbc, a.map, a.world).items():
        term = f"interface/worldmap/{folder.lower()}/"
        found = json.loads(get(f"{API}/files?search={urllib.parse.quote(term)}&limit=5000") or b"{}")
        by_path = {path.lower(): int(fdid) for fdid, path in found.items()}
        dest = os.path.join(a.out, "Interface", "WorldMap", folder)
        os.makedirs(dest, exist_ok=True)
        for name in names:
            target = os.path.join(dest, name + ".blp")
            if os.path.exists(target):
                continue
            fdid = by_path.get(f"{term}{name.lower()}.blp")
            if fdid is None:
                missing.append(f"{folder}/{name}")
                continue
            data = get(f"{API}/casc/{fdid}?download&version={a.version}")
            if not data or data[:4] != b"BLP2":
                missing.append(f"{folder}/{name} ({fdid}: not a BLP at {a.version})")
                continue
            with open(target, "wb") as fh:
                fh.write(data)
            count += 1
        print(f"{folder}: {len(names)} files")
    print(f"downloaded {count}; missing {len(missing)}")
    for m in missing:
        print("  missing", m)
    if a.uimap:
        relayout_highlights(a.out, a.uimap)


if __name__ == "__main__":
    main()
