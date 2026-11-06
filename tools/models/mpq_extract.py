#!/usr/bin/env python3
"""Extract one file from an MPQ archive (format 1 or 2, files over 4 GB included).

  python mpq_extract.py ARCHIVE.mpq "Path\\In\\Archive" OUT_FILE

Handles single-unit and sectored files, zlib and bzip2 compression and encrypted files. Enough for the client
patches (e.g. OA's patch-4.MPQ or the squished patch-3.mpq); other compressions stop with an error."""
import bz2, os, struct, sys, zlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks"))
from check_f013_assets import decrypt, hash_string  # noqa: E402


def words(data, key):
    n = len(data) // 4 * 4
    return struct.pack(f"<{n // 4}I", *decrypt(data[:n], key)) + data[n:]


def unpack(data, size):
    if len(data) == size:
        return data
    kind = data[0]
    if kind == 0x02:
        return zlib.decompress(data[1:])
    if kind == 0x10:
        return bz2.decompress(data[1:])
    raise SystemExit(f"compression {kind:#x} isn't supported")


def extract(archive, name):
    with open(archive, "rb") as f:
        start = 0
        while True:
            f.seek(start)
            if f.read(4) == b"MPQ\x1a":
                break
            start += 512
        f.seek(start)
        h = f.read(44)
        _, _, _, version, sector_shift, hash_pos, block_pos, hash_count, block_count = struct.unpack_from("<4sIIHHIIII", h)
        hash_hi = block_hi = hi_block_table = 0
        if version >= 1:
            hi_block_table, hash_hi, block_hi = struct.unpack_from("<QHH", h, 32)
        f.seek(start + hash_pos + (hash_hi << 32))
        hashes = decrypt(f.read(hash_count * 16), hash_string("(hash table)", 3))
        f.seek(start + block_pos + (block_hi << 32))
        blocks = decrypt(f.read(block_count * 16), hash_string("(block table)", 3))
        high = None
        if hi_block_table:
            f.seek(start + hi_block_table)
            high = struct.unpack(f"<{block_count}H", f.read(block_count * 2))

        a, b = hash_string(name, 1), hash_string(name, 2)
        index = hash_string(name, 0) % hash_count
        block = None
        for i in range(hash_count):
            e = hashes[(index + i) % hash_count * 4:(index + i) % hash_count * 4 + 4]
            if e[3] == 0xFFFFFFFF:
                break
            if e[0] == a and e[1] == b and e[3] < 0xFFFFFFFE:
                block = e[3]
                break
        if block is None:
            return None
        pos, csize, fsize, flags = blocks[block * 4:block * 4 + 4]
        if high:
            pos |= high[block] << 32
        key = None
        if flags & 0x10000:
            key = hash_string(name.replace("/", "\\").split("\\")[-1], 3)
            if flags & 0x20000:
                key = ((key + (pos & 0xFFFFFFFF)) ^ fsize) & 0xFFFFFFFF
        f.seek(start + pos)
        raw = f.read(csize)

    if flags & 0x01000000:  # single unit
        data = words(raw, key) if key is not None else raw
        return (unpack(data, fsize) if flags & 0x200 else data)[:fsize]
    sector = 512 << sector_shift
    count = (fsize + sector - 1) // sector
    offsets = None
    if flags & 0xFF00:  # compressed: a sector offset table first
        table = raw[:(count + 1) * 4]
        offsets = decrypt(table, (key - 1) & 0xFFFFFFFF) if key is not None else struct.unpack(f"<{count + 1}I", table)
    data = b""
    for i in range(count):
        chunk = raw[offsets[i]:offsets[i + 1]] if offsets else raw[i * sector:(i + 1) * sector]
        if key is not None:
            chunk = words(chunk, (key + i) & 0xFFFFFFFF)
        data += unpack(chunk, min(sector, fsize - i * sector)) if flags & 0x200 else chunk
    return data[:fsize]


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    content = extract(sys.argv[1], sys.argv[2])
    if content is None:
        sys.exit(f"{sys.argv[2]} isn't in {sys.argv[1]}")
    with open(sys.argv[3], "wb") as out:
        out.write(content)
    print(f"{sys.argv[2]}: {len(content)} bytes")
