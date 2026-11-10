#!/usr/bin/env python3
"""Unpack whole MPQ archives (format 1 or 2) into a folder, the way the client layers them.

  python -I mpq_unpack.py OUT_DIR ARCHIVE.mpq [ARCHIVE.mpq ...]

Archives are unpacked in the order given (give them in the client's load order), so a later archive's copy of a file
replaces an earlier one's, as in game. Each archive's (listfile) names its files; files without a name are skipped.
Same compressions as mpq_extract.py (zlib, bzip2); a file in another compression is reported and skipped."""
import os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks"))
from check_f013_assets import decrypt, hash_string  # noqa: E402
from mpq_extract import unpack, words  # noqa: E402


class Archive:
    def __init__(self, path):
        self.f = open(path, "rb")
        start = 0
        while True:
            self.f.seek(start)
            if self.f.read(4) == b"MPQ\x1a":
                break
            start += 512
        self.start = start
        self.f.seek(start)
        h = self.f.read(44)
        _, _, _, version, sector_shift, hash_pos, block_pos, hash_count, block_count = struct.unpack_from("<4sIIHHIIII", h)
        hash_hi = block_hi = hi_block_table = 0
        if version >= 1:
            hi_block_table, hash_hi, block_hi = struct.unpack_from("<QHH", h, 32)
        self.sector = 512 << sector_shift
        self.f.seek(start + hash_pos + (hash_hi << 32))
        hashes = decrypt(self.f.read(hash_count * 16), hash_string("(hash table)", 3))
        self.f.seek(start + block_pos + (block_hi << 32))
        self.blocks = decrypt(self.f.read(block_count * 16), hash_string("(block table)", 3))
        self.high = None
        if hi_block_table:
            self.f.seek(start + hi_block_table)
            self.high = struct.unpack(f"<{block_count}H", self.f.read(block_count * 2))
        self.index = {}
        for i in range(hash_count):
            a, b, _, block = hashes[i * 4:i * 4 + 4]
            if block < 0xFFFFFFFE:
                self.index[(a, b)] = block

    def read(self, name):
        block = self.index.get((hash_string(name, 1), hash_string(name, 2)))
        if block is None:
            return None
        pos, csize, fsize, flags = self.blocks[block * 4:block * 4 + 4]
        if not flags & 0x80000000:   # not a file (deleted)
            return None
        if self.high:
            pos |= self.high[block] << 32
        key = None
        if flags & 0x10000:
            key = hash_string(name.replace("/", "\\").split("\\")[-1], 3)
            if flags & 0x20000:
                key = ((key + (pos & 0xFFFFFFFF)) ^ fsize) & 0xFFFFFFFF
        self.f.seek(self.start + pos)
        raw = self.f.read(csize)
        if flags & 0x01000000:
            data = words(raw, key) if key is not None else raw
            return (unpack(data, fsize) if flags & 0x200 else data)[:fsize]
        count = (fsize + self.sector - 1) // self.sector
        offsets = None
        if flags & 0xFF00:
            table = raw[:(count + 1) * 4]
            offsets = decrypt(table, (key - 1) & 0xFFFFFFFF) if key is not None else struct.unpack(f"<{count + 1}I", table)
        out = []
        for i in range(count):
            chunk = raw[offsets[i]:offsets[i + 1]] if offsets else raw[i * self.sector:(i + 1) * self.sector]
            if key is not None:
                chunk = words(chunk, (key + i) & 0xFFFFFFFF)
            out.append(unpack(chunk, min(self.sector, fsize - i * self.sector)) if flags & 0x200 else chunk)
        return b"".join(out)[:fsize]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out = sys.argv[1]
    for path in sys.argv[2:]:
        archive = Archive(path)
        listfile = archive.read("(listfile)")
        if listfile is None:
            print(f"{path}: no (listfile), skipped")
            continue
        names = [n.strip() for n in listfile.decode("latin1").replace("\r", "\n").split("\n") if n.strip()]
        done = failed = 0
        for name in names:
            if name.startswith("("):
                continue
            try:
                data = archive.read(name)
            except SystemExit as e:
                print(f"  {name}: {e}")
                failed += 1
                continue
            if data is None:
                continue
            target = os.path.join(out, *name.replace("/", "\\").split("\\"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)
            done += 1
        print(f"{os.path.basename(path)}: {done} files, {failed} failed", flush=True)


if __name__ == "__main__":
    main()
