#!/usr/bin/env python3
"""Copy a map's 3.3.5a ADTs (plus its .wdt/.wdl) with every MCNK's area id set to one area.

  python -I adt_set_area.py IN_DIR OUT_DIR AREA_ID

For continents shipped as terrain only (F-145..F-148): their tiles keep retail's area ids, which no AreaTable.dbc
row names, and there aren't enough free explore bits below 4096 for all of them. One zone row per continent then
covers every tile, for the zone text, flying (F-006's flags) and the server's .map AREA section
(swap_server_maps.py --new-map reads the ids back from these tiles). The source tiles keep the original ids."""
import argparse, os, shutil, struct


def set_area(data, area):
    d = bytearray(data)
    i = 0
    while i + 8 <= len(d):
        magic, size = struct.unpack_from("<4sI", d, i)
        if magic == b"NICM":  # MCIN: 256 x (offset, size, flags, async id), absolute offsets
            for c in range(256):
                off = struct.unpack_from("<I", d, i + 8 + 16 * c)[0]
                assert d[off:off + 4] == b"KNCM", f"MCIN entry {c} doesn't point at an MCNK"
                struct.pack_into("<I", d, off + 8 + 0x34, area)
            return bytes(d)
        i += 8 + size
    raise ValueError("no MCIN")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("in_dir")
    p.add_argument("out_dir")
    p.add_argument("area", type=int)
    a = p.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    n = 0
    for f in sorted(os.listdir(a.in_dir)):
        ext = os.path.splitext(f)[1]
        src, dst = os.path.join(a.in_dir, f), os.path.join(a.out_dir, f)
        if ext.lower() == ".adt":
            with open(src, "rb") as fh:
                data = set_area(fh.read(), a.area)
            with open(dst, "wb") as fh:
                fh.write(data)
            n += 1
        elif ext.lower() in (".wdt", ".wdl"):
            shutil.copyfile(src, dst)
    print(f"{n} tiles -> {a.out_dir} (area {a.area})")


if __name__ == "__main__":
    main()
