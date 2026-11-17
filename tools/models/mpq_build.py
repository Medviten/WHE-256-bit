#!/usr/bin/env python3
"""Pack a folder into an MPQ archive (format 1) with LZMA sectors, for the 3.3.5 client.

  python -I mpq_build.py FOLDER OUT.MPQ [--sector-kb 64] [--method best|lzma] [--exclude NAME ...] [--jobs N]
  python -I mpq_build.py --verify FOLDER OUT.MPQ [--exclude NAME ...]

Every file under FOLDER is stored under its path relative to FOLDER (backslashes, case as on disk), plus a
(listfile). Each sector keeps the smallest of LZMA (0x12), zlib level 9 (0x02, with --method best) and the data
itself; a file that doesn't shrink is stored uncompressed. Larger sectors compress better, but the client reads a
whole sector for any read inside it. --exclude skips top-level entries of FOLDER by name, case-insensitively (e.g.
--exclude DBFilesClient).

The archive has a format 1 header and a hi-block table, so it may pass 4 GB. LZMA sectors use the layout the 3.3.5
client's Mopaq reader already decodes (see mpq_lzma_repack.py). --verify reads every file back through the
archive's hash table and compares it with the folder."""
import argparse, hashlib, multiprocessing, os, struct, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "checks"))
from check_f013_assets import decrypt, hash_string  # noqa: E402
from mpq_lzma_repack import FILE_COMPRESS, FILE_EXISTS, FILE_SINGLE_UNIT, compress, encrypt, unpack  # noqa: E402

HEADER_SIZE = 44


def collect(folder, exclude):
    skip = {name.lower() for name in exclude}
    names = []
    for top in sorted(os.listdir(folder), key=str.lower):
        if top.lower() in skip:
            continue
        path = os.path.join(folder, top)
        if os.path.isfile(path):
            names.append(top)
            continue
        for root, dirs, files in os.walk(path):
            dirs.sort(key=str.lower)
            for f in sorted(files, key=str.lower):
                names.append(os.path.relpath(os.path.join(root, f), folder).replace("/", "\\"))
    lowered = {}
    for name in names:
        if name.lower() in lowered:
            raise SystemExit(f"{name} and {lowered[name.lower()]} differ only in case")
        lowered[name.lower()] = name
    return names


def pack(job):
    """Returns (stored bytes, flags) for one file."""
    source, sector_size, method = job
    if isinstance(source, bytes):
        data = source
    else:
        with open(source, "rb") as f:
            data = f.read()
    if not data:
        return b"", FILE_EXISTS
    count = (len(data) + sector_size - 1) // sector_size
    sectors = [compress(data[i * sector_size:(i + 1) * sector_size], method) for i in range(count)]
    offsets = [4 * (count + 1)]
    for s in sectors:
        offsets.append(offsets[-1] + len(s))
    if offsets[-1] >= len(data):
        return data, FILE_EXISTS
    return struct.pack(f"<{count + 1}I", *offsets) + b"".join(sectors), FILE_EXISTS | FILE_COMPRESS


def jobs(folder, names, listfile, sector_size, method):
    for name in names:
        yield os.path.join(folder, name), sector_size, method
    yield listfile, sector_size, method


def build(args):
    names = collect(args.folder, args.exclude)
    listfile = ("\r\n".join(names) + "\r\n").encode("utf-8")
    entries = names + ["(listfile)"]
    hash_count = 1 << max(4, (len(entries) * 4 // 3).bit_length())
    shift = (args.sector_kb * 1024 // 512).bit_length() - 1
    if 512 << shift != args.sector_kb * 1024:
        raise SystemExit("--sector-kb must be a power of two")
    sector_size = 512 << shift

    hashes = [0xFFFFFFFF] * (hash_count * 4)
    for block, name in enumerate(entries):
        index = hash_string(name, 0) & (hash_count - 1)
        while hashes[index * 4 + 3] != 0xFFFFFFFF:
            index = (index + 1) & (hash_count - 1)
        hashes[index * 4:index * 4 + 4] = [hash_string(name, 1), hash_string(name, 2), 0, block]

    blocks, high = [], []
    in_bytes = out_bytes = 0
    t0 = time.time()
    with open(args.output, "wb") as out, multiprocessing.Pool(args.jobs) as pool:
        out.write(b"\0" * HEADER_SIZE)
        work = jobs(args.folder, names, listfile, sector_size, args.method)
        for i, (data, flags) in enumerate(pool.imap(pack, work, chunksize=16)):
            size = os.path.getsize(os.path.join(args.folder, names[i])) if i < len(names) else len(listfile)
            where = out.tell()
            out.write(data)
            if size and flags & FILE_COMPRESS == 0 and len(data) != size:
                raise SystemExit(f"{entries[i]}: stored size mismatch")
            blocks += [where & 0xFFFFFFFF, len(data), size, flags]
            high.append(where >> 32)
            in_bytes += size
            out_bytes += len(data)
            if i % 2000 == 1999 or i == len(entries) - 1:
                rate = in_bytes / max(time.time() - t0, 1e-6) / 1e6
                print(f"{i + 1}/{len(entries)} files, {in_bytes / 1e9:.2f} -> {out_bytes / 1e9:.2f} GB "
                      f"({100 * out_bytes / max(in_bytes, 1):.1f}%), {rate:.1f} MB/s", flush=True)

        hash_at = out.tell()
        out.write(encrypt(hashes, hash_string("(hash table)", 3)))
        block_at = out.tell()
        out.write(encrypt(blocks, hash_string("(block table)", 3)))
        hi_at = 0
        if any(high):
            hi_at = out.tell()
            out.write(struct.pack(f"<{len(high)}H", *high))
        end = out.tell()
        header = bytearray(HEADER_SIZE)
        struct.pack_into("<4sIIHHIIII", header, 0, b"MPQ\x1a", HEADER_SIZE, end & 0xFFFFFFFF, 1, shift,
                         hash_at & 0xFFFFFFFF, block_at & 0xFFFFFFFF, hash_count, len(entries))
        struct.pack_into("<QHH", header, 32, hi_at, hash_at >> 32, block_at >> 32)
        out.seek(0)
        out.write(header)
    print(f"done in {time.time() - t0:.0f} s: {len(names)} files, {in_bytes / 1e9:.3f} -> {end / 1e9:.3f} GB")


def read_file(f, hashes, blocks, high, hash_count, sector_size, name):
    index = hash_string(name, 0) & (hash_count - 1)
    a, b = hash_string(name, 1), hash_string(name, 2)
    for _ in range(hash_count):
        e = hashes[index * 4:index * 4 + 4]
        if e[3] == 0xFFFFFFFF:
            return None
        if e[0] == a and e[1] == b:
            break
        index = (index + 1) & (hash_count - 1)
    else:
        return None
    pos, csize, fsize, flags = blocks[e[3] * 4:e[3] * 4 + 4]
    f.seek(pos + (high[e[3]] << 32))
    raw = f.read(csize)
    if not flags & FILE_COMPRESS:
        return raw
    if flags & FILE_SINGLE_UNIT:
        return unpack(raw, fsize)
    count = (fsize + sector_size - 1) // sector_size
    offsets = struct.unpack_from(f"<{count + 1}I", raw)
    return b"".join(unpack(raw[offsets[i]:offsets[i + 1]], min(sector_size, fsize - i * sector_size))
                    for i in range(count))


def verify(args):
    names = collect(args.folder, args.exclude)
    with open(args.output, "rb") as f:
        header = f.read(HEADER_SIZE)
        _, _, _, _, shift, hash_pos, block_pos, hash_count, block_count = struct.unpack_from("<4sIIHHIIII", header)
        hi_at, hash_hi, block_hi = struct.unpack_from("<QHH", header, 32)
        f.seek(hash_pos + (hash_hi << 32))
        hashes = decrypt(f.read(hash_count * 16), hash_string("(hash table)", 3))
        f.seek(block_pos + (block_hi << 32))
        blocks = decrypt(f.read(block_count * 16), hash_string("(block table)", 3))
        high = [0] * block_count
        if hi_at:
            f.seek(hi_at)
            high = struct.unpack(f"<{block_count}H", f.read(block_count * 2))
        sector_size = 512 << shift
        listed = read_file(f, hashes, blocks, high, hash_count, sector_size, "(listfile)")
        bad = 0
        if listed is None or listed.decode("utf-8").split("\r\n")[:-1] != names:
            print("(listfile) doesn't match the folder")
            bad += 1
        for i, name in enumerate(names):
            with open(os.path.join(args.folder, name), "rb") as src:
                want = hashlib.sha256(src.read()).digest()
            got = read_file(f, hashes, blocks, high, hash_count, sector_size, name)
            if got is None or hashlib.sha256(got).digest() != want:
                print(f"MISMATCH {name}")
                bad += 1
            if i % 5000 == 4999:
                print(f"{i + 1}/{len(names)} checked", flush=True)
    print(f"{len(names)} files checked, {bad} bad")
    return bad == 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--verify", action="store_true", help="check OUT against FOLDER instead of building")
    parser.add_argument("folder")
    parser.add_argument("output")
    parser.add_argument("--sector-kb", type=int, default=64)
    parser.add_argument("--method", choices=["best", "lzma"], default="best")
    parser.add_argument("--exclude", nargs="*", default=[])
    parser.add_argument("--jobs", type=int, default=os.cpu_count())
    args = parser.parse_args()
    if args.verify:
        sys.exit(0 if verify(args) else 1)
    build(args)


if __name__ == "__main__":
    main()
