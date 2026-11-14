#!/usr/bin/env python3
"""Download every file in a game folder from wago.tools, at a given build version.

  python wago_folder.py FOLDER OUT [--version 5.5.4.70631] [--exclude REGEX]

FOLDER is a community listfile path prefix, e.g. world/maps/newracestartzone/ (the Wandering Isle's tiles, F-134).
Files are saved under OUT with their listfile names (lowercase); files already there are kept. --version defaults to
MoP Classic's, whose files are MoP's; --exclude skips paths matching the regex (e.g. _obj1\\.adt$, the later LOD
tiles 3.3.5a has no use for)."""
import argparse, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retail_fetch import API, get  # noqa: E402


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder")
    p.add_argument("out")
    p.add_argument("--version", default="5.5.4.70631")
    p.add_argument("--exclude")
    a = p.parse_args()
    found = json.loads(get(f"{API}/files?search={urllib.parse.quote(a.folder)}&limit=10000") or b"{}")
    if not isinstance(found, dict):
        sys.exit(f"nothing in {a.folder}")
    skip = re.compile(a.exclude) if a.exclude else None
    done = failed = 0
    for fdid, path in sorted(found.items(), key=lambda x: x[1]):
        if not path.startswith(a.folder) or (skip and skip.search(path)):
            continue
        target = os.path.join(a.out, *path.split("/"))
        if os.path.exists(target):
            continue
        data = get(f"{API}/casc/{fdid}?download&version={a.version}")
        if not data:
            print(f"  {path} ({fdid}): nothing at {a.version}")
            failed += 1
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)
        done += 1
    print(f"downloaded {done}, failed {failed}")


if __name__ == "__main__":
    main()
