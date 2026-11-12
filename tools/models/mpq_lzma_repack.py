#!/usr/bin/env python3
"""Recompress an MPQ archive (format 1 or 2) with LZMA sectors, keeping its file names, hashes and flags.

  python -I mpq_lzma_repack.py IN.mpq OUT.mpq [--method best|lzma] [--sector-kb 4] [--jobs N] [--limit N]
  python -I mpq_lzma_repack.py --verify IN.mpq OUT.mpq

Each file is decompressed and its sectors are compressed again. --method best (default) keeps, per sector, the
smallest of LZMA (0x12), zlib level 9 (0x02) and the data itself; --method lzma uses LZMA wherever it is smaller than
the data. --sector-kb changes the sector size (the client reads one whole sector for any read inside it, so larger
sectors compress better but make small reads slower). --limit repacks only the first N files (for sampling; the
output then holds only those).

LZMA sectors use StormLib's layout (a 0 byte, 5 property bytes, the 64-bit unpacked size, then raw LZMA data), which
the 3.3.5 client's Mopaq reader (System_SComp::LzmaDecompress) already decodes. Encrypted files, imploded files and
files in compressions this script cannot read are copied unchanged. Sector checksums are dropped, since they are
adler32 sums of the old compressed bytes."""
import argparse, bz2, lzma, multiprocessing, os, struct, sys, time, zlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks"))
from check_f013_assets import CRYPT, decrypt, hash_string  # noqa: E402

FILE_IMPLODE = 0x00000100
FILE_COMPRESS = 0x00000200
FILE_ENCRYPTED = 0x00010000
FILE_FIX_KEY = 0x00020000
FILE_SINGLE_UNIT = 0x01000000
FILE_DELETE_MARKER = 0x02000000
FILE_SECTOR_CRC = 0x04000000
FILE_EXISTS = 0x80000000


def encrypt(words, key):
    seed, out = 0xEEEEEEEE, []
    for plain in words:
        seed = (seed + CRYPT[0x400 + (key & 0xFF)]) & 0xFFFFFFFF
        out.append((plain ^ (key + seed)) & 0xFFFFFFFF)
        key = (((~key << 21) + 0x11111111) | (key >> 11)) & 0xFFFFFFFF
        seed = (plain + seed + (seed << 5) + 3) & 0xFFFFFFFF
    return struct.pack(f"<{len(out)}I", *out)


def lzma_block(data):
    dict_size = max(4096, 1 << (len(data) - 1).bit_length())
    filters = [{"id": lzma.FILTER_LZMA1, "dict_size": dict_size, "lc": 3, "lp": 0, "pb": 2,
                "mode": lzma.MODE_NORMAL, "nice_len": 273, "mf": lzma.MF_BT4, "depth": 0}]
    packed = lzma.compress(data, format=lzma.FORMAT_RAW, filters=filters)
    props = bytes([(2 * 5 + 0) * 9 + 3]) + struct.pack("<I", dict_size)
    return b"\x12\x00" + props + struct.pack("<Q", len(data)) + packed


def compress(data, method):
    best = data
    candidates = [lzma_block(data)]
    if method == "best":
        candidates.append(b"\x02" + zlib.compress(data, 9))
    for c in candidates:
        if len(c) < len(best):
            best = c
    return best


def unpack(data, size):
    if len(data) == size:
        return data
    kind = data[0]
    if kind == 0x02:
        return zlib.decompress(data[1:])
    if kind == 0x10:
        return bz2.decompress(data[1:])
    if kind == 0x12:
        if data[1] != 0:
            return None
        lc_lp_pb, dict_size = data[2], struct.unpack_from("<I", data, 3)[0]
        lc, rest = lc_lp_pb % 9, lc_lp_pb // 9
        lp, pb = rest % 5, rest // 5
        filters = [{"id": lzma.FILTER_LZMA1, "dict_size": dict_size, "lc": lc, "lp": lp, "pb": pb}]
        return lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=filters).decompress(data[15:], size)
    return None


_input = None


def _open(path):
    global _input
    _input = open(path, "rb")


def repack(job):
    """Returns (data, flags) for one block; data None means copy the block unchanged."""
    pos, csize, fsize, flags, sector_size, new_sector_size, method = job
    if (not flags & FILE_EXISTS or flags & (FILE_ENCRYPTED | FILE_IMPLODE | FILE_DELETE_MARKER)
            or not flags & FILE_COMPRESS or fsize == 0):
        return None, flags
    _input.seek(pos)
    raw = _input.read(csize)
    try:
        if flags & FILE_SINGLE_UNIT:
            content = unpack(raw, fsize)
        else:
            count = (fsize + sector_size - 1) // sector_size
            offsets = struct.unpack_from(f"<{count + 1}I", raw)
            parts = []
            for i in range(count):
                part = unpack(raw[offsets[i]:offsets[i + 1]], min(sector_size, fsize - i * sector_size))
                if part is None:
                    return None, flags
                parts.append(part)
            content = b"".join(parts)
    except (zlib.error, OSError, lzma.LZMAError, struct.error):
        return None, flags
    if content is None or len(content) != fsize:
        return None, flags

    flags &= ~FILE_SECTOR_CRC
    if flags & FILE_SINGLE_UNIT:
        return compress(content, method), flags
    count = (fsize + new_sector_size - 1) // new_sector_size
    sectors = [compress(content[i * new_sector_size:(i + 1) * new_sector_size], method) for i in range(count)]
    offsets = [4 * (count + 1)]
    for s in sectors:
        offsets.append(offsets[-1] + len(s))
    return struct.pack(f"<{count + 1}I", *offsets) + b"".join(sectors), flags


def read_tables(path):
    with open(path, "rb") as f:
        start = 0
        while True:
            f.seek(start)
            if f.read(4) == b"MPQ\x1a":
                break
            start += 512
        f.seek(start)
        header = f.read(44)
        _, _, _, version, shift, hash_pos, block_pos, hash_count, block_count = struct.unpack_from("<4sIIHHIIII", header)
        hash_hi = block_hi = hi_block_table = 0
        if version == 1:
            hi_block_table, hash_hi, block_hi = struct.unpack_from("<QHH", header, 32)
        f.seek(start + hash_pos + (hash_hi << 32))
        hash_bytes = f.read(hash_count * 16)
        f.seek(start + block_pos + (block_hi << 32))
        blocks = decrypt(f.read(block_count * 16), hash_string("(block table)", 3))
        high = [0] * block_count
        if hi_block_table:
            f.seek(start + hi_block_table)
            high = list(struct.unpack(f"<{block_count}H", f.read(block_count * 2)))
    return start, 512 << shift, hash_bytes, blocks, high


def content(f, pos, csize, fsize, flags, sector_size):
    """The unpacked file, or None for files this script leaves alone (they are compared byte for byte)."""
    if (not flags & FILE_EXISTS or flags & (FILE_ENCRYPTED | FILE_IMPLODE | FILE_DELETE_MARKER)
            or not flags & FILE_COMPRESS or fsize == 0):
        return None
    f.seek(pos)
    raw = f.read(csize)
    if flags & FILE_SINGLE_UNIT:
        return unpack(raw, fsize)
    count = (fsize + sector_size - 1) // sector_size
    offsets = struct.unpack_from(f"<{count + 1}I", raw)
    parts = [unpack(raw[offsets[i]:offsets[i + 1]], min(sector_size, fsize - i * sector_size)) for i in range(count)]
    return None if None in parts else b"".join(parts)


def verify(original, repacked):
    a_start, a_sector, a_hashes, a_blocks, a_high = read_tables(original)
    b_start, b_sector, b_hashes, b_blocks, b_high = read_tables(repacked)
    if a_hashes != b_hashes or len(a_blocks) != len(b_blocks):
        raise SystemExit("hash or block tables differ in size or content")
    bad = 0
    with open(original, "rb") as fa, open(repacked, "rb") as fb:
        for i in range(len(a_blocks) // 4):
            pa, ca, sa, la = a_blocks[i * 4:i * 4 + 4]
            pb, cb, sb, lb = b_blocks[i * 4:i * 4 + 4]
            pa, pb = a_start + pa + (a_high[i] << 32), b_start + pb + (b_high[i] << 32)
            try:
                da = content(fa, pa, ca, sa, la, a_sector)
                db = content(fb, pb, cb, sb, lb, b_sector)
            except Exception as e:  # noqa: BLE001
                da, db = 0, e
            if da is None and db is None:
                fa.seek(pa)
                fb.seek(pb)
                same = fa.read(ca) == fb.read(cb) and la == lb
            else:
                same = da == db and sa == sb and (la & ~FILE_SECTOR_CRC) == lb
            if not same:
                bad += 1
                if bad <= 10:
                    print(f"block {i} differs ({db if isinstance(db, Exception) else ''})")
            if i % 20000 == 19999:
                print(f"{i + 1} files checked", flush=True)
    print(f"verified {len(a_blocks) // 4} files, {bad} differ")
    return bad == 0


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--verify":
        sys.exit(0 if verify(sys.argv[2], sys.argv[3]) else 1)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--method", choices=["best", "lzma"], default="best")
    parser.add_argument("--sector-kb", type=int, default=0, help="new sector size in KB (default: keep)")
    parser.add_argument("--jobs", type=int, default=os.cpu_count())
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        start = 0
        while True:
            f.seek(start)
            if f.read(4) == b"MPQ\x1a":
                break
            start += 512
        f.seek(start)
        header = bytearray(f.read(44))
        _, _, _, version, shift, hash_pos, block_pos, hash_count, block_count = struct.unpack_from("<4sIIHHIIII", header)
        if version > 1:
            raise SystemExit(f"format {version + 1} archives aren't supported")
        hash_hi = block_hi = hi_block_table = 0
        if version == 1:
            hi_block_table, hash_hi, block_hi = struct.unpack_from("<QHH", header, 32)
        f.seek(start + hash_pos + (hash_hi << 32))
        hash_bytes = f.read(hash_count * 16)
        f.seek(start + block_pos + (block_hi << 32))
        blocks = decrypt(f.read(block_count * 16), hash_string("(block table)", 3))
        high = [0] * block_count
        if hi_block_table:
            f.seek(start + hi_block_table)
            high = list(struct.unpack(f"<{block_count}H", f.read(block_count * 2)))

    sector_size = 512 << shift
    new_shift = shift
    if args.sector_kb:
        new_shift = (args.sector_kb * 1024 // 512).bit_length() - 1
        if 512 << new_shift != args.sector_kb * 1024:
            raise SystemExit("--sector-kb must be a power of two")
    new_sector_size = 512 << new_shift

    total = args.limit or block_count
    jobs = []
    for i in range(total):
        pos, csize, fsize, flags = blocks[i * 4:i * 4 + 4]
        jobs.append((start + pos + (high[i] << 32), csize, fsize, flags, sector_size, new_sector_size, args.method))

    new_blocks, new_high = list(blocks), list(high)
    copied = in_bytes = out_bytes = 0
    t0 = time.time()
    with open(args.input, "rb") as src, open(args.output, "wb") as out, \
            multiprocessing.Pool(args.jobs, _open, (args.input,)) as pool:
        out.write(b"\0" * 44)
        for i, (data, flags) in enumerate(pool.imap(repack, jobs, chunksize=64)):
            pos, csize, fsize, _ = jobs[i][:4]
            if data is None:
                src.seek(pos)
                data = src.read(csize)
                if flags & FILE_EXISTS and fsize:
                    copied += 1
            if flags & FILE_ENCRYPTED and flags & FILE_FIX_KEY and data:
                raise SystemExit(f"block {i}: encrypted with a position-dependent key; not supported")
            where = out.tell()
            out.write(data)
            in_bytes += csize
            out_bytes += len(data)
            new_blocks[i * 4:i * 4 + 4] = [where & 0xFFFFFFFF, len(data), fsize, flags]
            new_high[i] = where >> 32
            if i % 5000 == 4999 or i == total - 1:
                rate = in_bytes / max(time.time() - t0, 1e-6) / 1e6
                print(f"{i + 1}/{total} files, {in_bytes / 1e9:.2f} -> {out_bytes / 1e9:.2f} GB "
                      f"({100 * out_bytes / max(in_bytes, 1):.1f}%), {rate:.1f} MB/s", flush=True)
        for i in range(total, block_count):
            new_blocks[i * 4:i * 4 + 4] = [0, 0, 0, 0]

        hash_at = out.tell()
        out.write(hash_bytes)
        block_at = out.tell()
        out.write(encrypt(new_blocks, hash_string("(block table)", 3)))
        hi_at = out.tell()
        out.write(struct.pack(f"<{block_count}H", *new_high))
        end = out.tell()
        struct.pack_into("<4sIIHHIIII", header, 0, b"MPQ\x1a", 44, end & 0xFFFFFFFF, 1, new_shift,
                         hash_at & 0xFFFFFFFF, block_at & 0xFFFFFFFF, hash_count, block_count)
        struct.pack_into("<QHH", header, 32, hi_at, hash_at >> 32, block_at >> 32)
        out.seek(0)
        out.write(header)

    print(f"done in {time.time() - t0:.0f} s: {end / 1e9:.3f} GB written, {copied} files copied unchanged")


if __name__ == "__main__":
    main()
