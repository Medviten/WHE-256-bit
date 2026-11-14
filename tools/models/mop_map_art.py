#!/usr/bin/env python3
"""Download Mists of Pandaria's world map art for a map (and the World map) into a client patch folder.

  python mop_map_art.py MOP_DBC_DIR OUT [--map 870] [--world] [--version 5.5.4.70631]

OUT is a patch folder such as WHE-common's patch-A.MPQ: files go to OUT/Interface/WorldMap/<map>/<file>.blp, named as
the 3.3.5 client asks for them. Which files: for every WorldMapArea of --map that F-133 keeps (no dungeon floors or
phase copies), its 12 tiles (<name>1..12) and, for zones, the highlight the continent map shows on hover
(<name>Highlight); for every WorldMapOverlay of those, its 256 x 256 pieces (<texture>1..N, N = tiles across x down);
with --world, the World map's 12 tiles. MOP_DBC_DIR holds the 5.4.8 DBCs the rows come from.

The files come from wago.tools at --version, by default MoP Classic's (its map art is MoP's; the newest version of
the World tiles is Legion's, with the Broken Isles). Their community listfile names are looked up per folder.
Files already in OUT are kept."""
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
        if r[1] != map_id or r[9] or r[10]:
            continue
        name = wma.s(r[3])
        folder_of[r[0]] = name
        out[name] = [f"{name}{i}" for i in range(1, 13)] + ([f"{name}Highlight"] if r[2] else [])
    for r in wmo.records:
        if r[1] in folder_of:
            tex = wmo.s(r[6])
            n = math.ceil(r[7] / 256) * math.ceil(r[8] / 256)
            out[folder_of[r[1]]] += [f"{tex}{i}" for i in range(1, n + 1)]
    if world:
        out["World"] = [f"World{i}" for i in range(1, 13)]
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mop_dbc")
    p.add_argument("out")
    p.add_argument("--map", type=int, default=870)
    p.add_argument("--world", action="store_true")
    p.add_argument("--version", default="5.5.4.70631")
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


if __name__ == "__main__":
    main()
