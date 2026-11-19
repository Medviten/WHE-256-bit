#!/usr/bin/env python3
"""Download Mists of Pandaria's minimap tiles of a map into a client patch folder.

  python -I mop_minimaps.py ADT_DIR DIRECTORY OUT [--version 5.5.4.70631]

For every <DIRECTORY>_<x>_<y>.adt in ADT_DIR, MoP Classic's world/minimaps/<directory>/map<x>_<y>.blp (wago.tools,
community listfile names) is written to OUT/Textures/Minimap/<DIRECTORY>/map<x>_<y>.blp. The client finds tiles
there by name when md5translate.trs doesn't list them (wowdecomp's MinimapBuildSource fallback), so the shared trs
needn't change. Tiles the listfile lacks (open sea) are skipped; files already in OUT are kept.

F-137 (retail): python -I mop_minimaps.py <tiles> ExilesReach <WHE-common>/patch-ER.MPQ --source 2175
       --version 12.1.5.70961
F-134: python -I mop_minimaps.py <WHE-common>/patch-MoP.MPQ/World/Maps/NewRaceStartZone
       NewRaceStartZone <WHE-common>/patch-MoP.MPQ"""
import argparse, glob, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retail_fetch import API, get  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("adt_dir")
    p.add_argument("directory")
    p.add_argument("out")
    p.add_argument("--version", default="5.5.4.70631")
    p.add_argument("--source", help="the source build's minimap folder, when it isn't DIRECTORY (Exile's Reach: 2175)")
    a = p.parse_args()
    term = f"world/minimaps/{(a.source or a.directory).lower()}/"
    found = json.loads(get(f"{API}/files?search={urllib.parse.quote(term)}&limit=5000") or b"{}")
    by_path = {path.lower(): int(fdid) for fdid, path in found.items()}
    dest = os.path.join(a.out, "Textures", "Minimap", a.directory)
    os.makedirs(dest, exist_ok=True)
    count = missing = 0
    for f in sorted(glob.glob(os.path.join(a.adt_dir, "*.adt"))):
        m = re.search(r"_(\d+)_(\d+)\.adt$", f, re.I)
        if not m:
            continue
        name = "map%d_%02d.blp" % (int(m.group(1)), int(m.group(2)))
        target = os.path.join(dest, name)
        if os.path.exists(target):
            continue
        fdid = by_path.get(term + name)
        data = get(f"{API}/casc/{fdid}?download&version={a.version}") if fdid else None
        if not data or data[:4] != b"BLP2":
            missing += 1
            continue
        with open(target, "wb") as fh:
            fh.write(data)
        count += 1
    print(f"downloaded {count} minimap tiles; {missing} tiles have none")


if __name__ == "__main__":
    main()
