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
mop_map_port.py the same file) re-lays the continents' World map highlights for the 3.3.5 client. A MoP highlight
holds its outline in the texture's top 512 x 341 band, at a scale and place per continent that follows neither the
UiMapAssignment region nor 5.4.8's WorldMapContinent row, so HIGHLIGHT_BOX gives where each band lands on the
1002 x 668 World map, fitted to the coastlines of the World tiles. 3.3.5 draws the highlight over the WorldMapContinent
rectangle mop_map_port.py writes (Script_UpdateMapHighlight: the top-left part the boundaries' aspect gives); each
highlight still as downloaded (DXT, the re-laid ones are palettized) is resampled so that rectangle shows the band at
its box."""
import argparse, math, os, sys, urllib.parse, json

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


# (scale, left, top): a MoP highlight's texture pixel (u, v) shows at World map pixel (left + u * scale,
# top + v * scale); fitted to the MoP Classic World tiles' coastlines
HIGHLIGHT_BOX = {"Azeroth": (1.2257, 534.5, 117.5), "Kalimdor": (1.1475, -97.0, 125.5),
                 "Northrend": (0.5937, 384.5, 9.5), "Pandaria": (0.5227, 388.0, 461.0)}


def relayout_highlights(out, uimap):
    from maghar_modern_prep import write_blp
    from mop_map_port import uimap_placement
    done = 0
    for map_id, (L, R, T, B, ox, oy, sc) in uimap_placement(uimap).items():
        name = CONTINENT_FOLDERS.get(map_id)
        path = os.path.join(out, "Interface", "WorldMap", name or "", f"{name}Highlight.blp")
        if not name or not os.path.exists(path) or open(path, "rb").read(9)[8] != 2:
            continue                                       # not downloaded, or already re-laid
        w, h, src = read_rgba(path)
        scale, bx0, by0 = HIGHLIGHT_BOX[name]
        # the rectangle and texture part Script_UpdateMapHighlight gives, in World map pixels (16 per unit)
        tw, th = R - L + 1, B - T + 1
        tcx, tcy = (tw / th, 1.0) if th >= tw else (1.0, th / tw)
        rx0, ry0 = (L * sc + 31.3125 - sc * 32 + ox) * 16, (T * sc + 20.875 - sc * 32 + oy) * 16
        rw, rh = sc * tw * 16, sc * th * 16
        dst = bytearray(w * h * 4)
        for j in range(int(tcy * h)):
            v = int((ry0 + (j + 0.5) / (tcy * h) * rh - by0) / scale)
            for i in range(int(tcx * w)):
                u = int((rx0 + (i + 0.5) / (tcx * w) * rw - bx0) / scale)
                if 0 <= u < w and 0 <= v < h * 2 // 3:
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
