#!/usr/bin/env python3
"""Halve BLP2 textures larger than a size by dropping their top mip levels, in place.

  python -I blp_drop_mip.py [--max 512] FILE_OR_DIR...

For terrain: the 3.3.5a client draws tileset textures above 512 x 512 (Cataclysm and later ship 1024 x 1024 ones)
as flat green. The smaller mips are already in the file, so this only moves them up; nothing is re-encoded."""
import argparse, glob, os, struct


def shrink(path, limit):
    d = bytearray(open(path, "rb").read())
    if d[:4] != b"BLP2":
        return False
    w, h = struct.unpack_from("<II", d, 12)
    offs = list(struct.unpack_from("<16I", d, 20))
    sizes = list(struct.unpack_from("<16I", d, 84))
    drop = 0
    while max(w, h) > limit and drop + 1 < 16 and offs[drop + 1]:
        w, h, drop = max(w // 2, 1), max(h // 2, 1), drop + 1
    if not drop:
        return False
    head = d[:148]  # header + offsets + sizes (the palette follows for palettized files)
    body_start = 148 + (1024 if d[8] == 1 else 0)
    keep = [(o, s) for o, s in zip(offs[drop:], sizes[drop:]) if o]
    out = bytearray(head + d[148:body_start])
    new_offs, new_sizes = [], []
    for o, s in keep:
        new_offs.append(len(out))
        new_sizes.append(s)
        out += d[o:o + s]
    struct.pack_into("<II", out, 12, w, h)
    struct.pack_into("<16I", out, 20, *(new_offs + [0] * (16 - len(new_offs))))
    struct.pack_into("<16I", out, 84, *(new_sizes + [0] * (16 - len(new_sizes))))
    open(path, "wb").write(out)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paths", nargs="+")
    p.add_argument("--max", type=int, default=512)
    a = p.parse_args()
    files = []
    for x in a.paths:
        files += glob.glob(os.path.join(x, "**", "*.blp"), recursive=True) if os.path.isdir(x) else [x]
    n = sum(shrink(f, a.max) for f in files)
    print("shrank %d of %d files to at most %d" % (n, len(files), a.max))


if __name__ == "__main__":
    main()
