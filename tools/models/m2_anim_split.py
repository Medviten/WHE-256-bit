"""Move the animation data of a 3.3.5 (version 264) M2 into per-sequence .anim files, as Blizzard's own character
models keep it. The client loads a sequence's file (<model><id:04d>-<variation:02d>.anim, the sequence's alias source
for an alias) the first time the sequence plays and relocates the inner arrays of every track that has no global
sequence against it (CM2Shared::FinishLoadingLowPrioritySequence / M2Init), so all of a sequence's track data moves,
not only the bones'. Sequence flag 0x20 (data in the model) is cleared for each moved sequence.

A sequence moves together with its aliases (the ring of alias next links, which the client relocates as a whole against
its source's file). Kept in the model: the ring of sequence 0 and of any sequence below the outer count of a
global-sequence track (loading sequence s relocates such a track's inner array s against the .anim as well), rings
without track data and sequences already external. The model
is repacked: every block keeps its offset modulo 16, unreferenced bytes (some converters leave old copies behind) are
dropped. The result is checked block by block against the original.

usage: python -I m2_anim_split.py <model.m2> [output folder]   (default: in place)"""
import bisect
import os
import struct
import sys

HAS_DATA, ALIAS = 0x20, 0x40
SEQUENCE_SIZE = 64

# header offset of each array of structs with tracks: struct size, [(track offset, key size; 0 = M2TrackBase)]
TRACKS = {
    0x2C: (88, [(0x10, 12), (0x24, 8), (0x38, 12)]),                                   # bones
    0x48: (40, [(0x00, 12), (0x14, 2)]),                                               # colors
    0x58: (20, [(0x00, 2)]),                                                           # texture weights
    0x60: (60, [(0x00, 12), (0x14, 16), (0x28, 12)]),                                  # texture transforms
    0xF0: (40, [(0x14, 1)]),                                                           # attachments
    0x100: (36, [(0x18, 0)]),                                                          # events
    0x108: (156, [(0x10, 12), (0x24, 4), (0x38, 12), (0x4C, 4), (0x60, 4), (0x74, 4), (0x88, 1)]),  # lights
    0x110: (100, [(0x10, 36), (0x30, 36), (0x50, 12)]),                                # cameras
    0x120: (176, [(0x24, 12), (0x38, 2), (0x4C, 4), (0x60, 4), (0x84, 2), (0x98, 1)]),  # ribbons
    0x128: (476, [(0x34, 4), (0x48, 4), (0x5C, 4), (0x70, 4), (0x84, 4), (0x98, 4), (0xB0, 4), (0xC8, 4),
                  (0xDC, 4), (0xF0, 4), (0x1C8, 1)]),                                  # particles
}
# every header array: element size
HEADER = {0x08: 1, 0x14: 4, 0x1C: SEQUENCE_SIZE, 0x24: 2, 0x2C: 88, 0x34: 2, 0x3C: 48, 0x48: 40, 0x50: 16, 0x58: 20,
          0x60: 60, 0x68: 2, 0x70: 4, 0x78: 2, 0x80: 2, 0x88: 2, 0x90: 2, 0x98: 2, 0xD8: 2, 0xE0: 12, 0xE8: 12,
          0xF0: 40, 0xF8: 2, 0x100: 36, 0x108: 156, 0x110: 100, 0x118: 2, 0x120: 176, 0x128: 476}
# arrays inside structs (no tracks): header offset of the struct array, [(array offset, element size)]
NESTED = {
    0x50: [(0x08, 1)],                                                                 # texture file names
    0x120: [(0x14, 2), (0x1C, 2)],                                                     # ribbon textures, materials
    0x128: [(0x18, 1), (0x20, 1), (0x104, 2), (0x10C, 12), (0x114, 2), (0x11C, 2), (0x124, 2), (0x12C, 8),
            (0x13C, 2), (0x144, 2), (0x14C, 2), (0x154, 2), (0x1C0, 12)],              # particle models, part tracks, spline
}


def arr(data, pos):
    return struct.unpack_from('<II', data, pos)


def pointers(data, external):
    """Every array of the model: (position of its M2Array, element size, sequence) with sequence None for arrays that
    stay in the model and the sequence index for the inner arrays of sequences in `external` (or already external,
    which are skipped)."""
    flags = struct.unpack_from('<I', data, 0x10)[0]
    header = dict(HEADER)
    if flags & 0x8:
        header[0x130] = 2
    nseq, seqs = arr(data, 0x1C)
    seq_flags = [struct.unpack_from('<I', data, seqs + SEQUENCE_SIZE * i + 0x0C)[0] for i in range(nseq)]
    out = [(pos, size, None) for pos, size in header.items()]
    for hpos, fields in NESTED.items():
        count, offset = arr(data, hpos)
        for i in range(count):
            out += [(offset + header[hpos] * i + f, size, None) for f, size in fields]
    for hpos, (struct_size, tracks) in TRACKS.items():
        count, offset = arr(data, hpos)
        for i in range(count):
            for track, key_size in tracks:
                t = offset + struct_size * i + track
                global_sequence = struct.unpack_from('<H', data, t + 2)[0] != 0xFFFF
                parts = [(t + 4, 4)] + ([(t + 12, key_size)] if key_size else [])
                inner_count = arr(data, t + 4)[0]
                for outer, size in parts:
                    out.append((outer, 8, None))
                    n, o = arr(data, outer)
                    for s in range(min(n, inner_count)):
                        if not global_sequence and s >= nseq:
                            raise ValueError('track at 0x%X has more sequences than the model' % t)
                        if global_sequence or seq_flags[s] & HAS_DATA and s not in external:
                            out.append((o + 8 * s, size, None))
                        elif s in external:
                            out.append((o + 8 * s, size, s))
    return out, seq_flags


def sequences(data):
    """(id, variation, flags, alias next) of each sequence."""
    nseq, seqs = arr(data, 0x1C)
    return [struct.unpack_from('<HHI', data, seqs + SEQUENCE_SIZE * i)[:2]
            + (struct.unpack_from('<I', data, seqs + SEQUENCE_SIZE * i + 0x0C)[0],
               struct.unpack_from('<H', data, seqs + SEQUENCE_SIZE * i + 0x3E)[0]) for i in range(nseq)]


def anim_name(seqs, base, s):
    """The .anim file the client reads for sequence s: that of its alias source."""
    for _ in range(len(seqs)):
        if not seqs[s][2] & ALIAS:
            break
        s = seqs[s][3]
    return '%s%04d-%02d.anim' % (base, seqs[s][0], seqs[s][1])


def chosen(data):
    """Sequences to move. A sequence and its aliases form a ring (alias next), which the client loads from one file
    and relocates as a whole: a ring moves when it has data in the model, a source that is no alias and some track
    data (the client cannot load an empty .anim), and no sequence the global-sequence tracks reserve."""
    seqs = sequences(data)
    # loading sequence s also relocates inner array s of global-sequence tracks (normally only 0 exists)
    reserved = 1
    for hpos, (struct_size, tracks) in TRACKS.items():
        count, offset = arr(data, hpos)
        for i in range(count):
            for track, key_size in tracks:
                t = offset + struct_size * i + track
                if struct.unpack_from('<H', data, t + 2)[0] != 0xFFFF:
                    reserved = max(reserved, arr(data, t + 4)[0], arr(data, t + 12)[0] if key_size else 0)
    out, seen = set(), set()
    for i in range(len(seqs)):
        if i in seen:
            continue
        ring, j = [i], seqs[i][3]
        while j != i and j < len(seqs) and len(ring) <= len(seqs):
            ring.append(j)
            j = seqs[j][3]
        seen.update(ring)
        if j == i and min(ring) >= reserved and all(seqs[s][2] & HAS_DATA for s in ring) \
                and any(not seqs[s][2] & ALIAS for s in ring):
            out.update(ring)
    ptrs, _ = pointers(data, out)
    with_data = {seq for pos, size, seq in ptrs if seq is not None and arr(data, pos)[0]}
    rings = {}
    for s in out:
        rings.setdefault(anim_name(seqs, '', s), set()).add(s)
    return {s for ring in rings.values() if ring & with_data for s in ring}


def split(data, name):
    """(new model, {file name: .anim data}) for a model named `name` (its file name, for the .anim names)."""
    if data[:4] != b'MD20' or struct.unpack_from('<I', data, 4)[0] != 264:
        raise ValueError('not a 3.3.5 (version 264) M2')
    external = chosen(data)
    ptrs, seq_flags = pointers(data, external)
    flags = struct.unpack_from('<I', data, 0x10)[0]
    header_size = 0x138 if flags & 0x8 else 0x130

    # blocks that stay: the header and every kept array's data
    kept = {(0, header_size)}
    for pos, size, seq in ptrs:
        n, o = arr(data, pos)
        if seq is None and n:
            kept.add((o, o + n * size))
    regions = []
    for start, end in sorted(kept):
        if regions and start <= regions[-1][1]:
            regions[-1][1] = max(regions[-1][1], end)
        else:
            regions.append([start, end])
    # moved data is copied out of the original, so data a moved and a kept array share is in both files
    moved = {}
    for pos, size, seq in ptrs:
        n, o = arr(data, pos)
        if seq is not None and n:
            moved.setdefault(seq, []).append((pos, o, n * size))

    # repack the kept regions, each at its old offset modulo 16
    new_start, out = [], bytearray()
    for start, end in regions:
        out += b'\0' * ((start - len(out)) % 16)
        new_start.append(len(out))
        out += data[start:end]
    starts = [r[0] for r in regions]

    def remap(offset):
        lo, hi = 0, len(regions) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        start, end = regions[lo]
        if not start <= offset < end:
            raise ValueError('offset 0x%X is outside the kept data' % offset)
        return new_start[lo] + offset - start

    def where(pos):
        """New position of an M2Array that stays in the model."""
        return remap(pos)

    for pos, size, seq in ptrs:
        n, o = arr(data, pos)
        if seq is None:
            struct.pack_into('<I', out, where(pos) + 4, remap(o) if n else 0)

    nseq, seqs = arr(data, 0x1C)
    table = sequences(data)
    base = os.path.splitext(name)[0]
    anims, placed = {}, {}   # placed: (file, offset, length) -> offset in the file, for data ring members share
    for seq, blocks in sorted(moved.items()):
        file = anim_name(table, base, seq)
        anim = anims.setdefault(file, bytearray())
        for pos, o, length in blocks:
            key = (file, o, length)
            if key not in placed:
                anim += b'\0' * (-len(anim) % 16)
                placed[key] = len(anim)
                anim += data[o:o + length]
            struct.pack_into('<I', out, where(pos) + 4, placed[key])
    anims = {file: bytes(anim) for file, anim in anims.items()}
    # a file of the same name may be left over from an earlier conversion (its sequence back in the model); one that
    # an external sequence reads must stay
    for s in range(nseq):
        if not table[s][2] & HAS_DATA and anim_name(table, base, s) in anims:
            raise ValueError('%s is read by external sequence %d' % (anim_name(table, base, s), s))
    new_seqs = remap(seqs)
    for seq in external:
        f = struct.unpack_from('<I', out, new_seqs + SEQUENCE_SIZE * seq + 0x0C)[0]
        struct.pack_into('<I', out, new_seqs + SEQUENCE_SIZE * seq + 0x0C, f & ~HAS_DATA)
    check(data, bytes(out), anims, base, external)
    return bytes(out), anims


def contents(data, anims, base, external):
    """{(array kind, index...): bytes} of every array, reading moved sequences from their .anim data."""
    table = sequences(data)
    names = {s: anim_name(table, base, s) for s in range(len(table))}
    ptrs, _ = pointers(data, external)
    offsets = sorted(pos + 4 for pos, size, seq in ptrs)   # the offset fields, which the split rewrites
    out = []
    for pos, size, seq in ptrs:
        n, o = arr(data, pos)
        source = data if seq is None else anims[names[seq]]
        block = bytearray(source[o:o + n * size] if n else b'')
        if seq is None and n:
            for field in offsets[bisect.bisect_left(offsets, o):bisect.bisect_left(offsets, o + n * size)]:
                block[field - o:field - o + 4] = b'\0\0\0\0'
        if pos == 0x1C:   # the sequences, without the flag the split clears
            for s in range(n):
                block[SEQUENCE_SIZE * s + 0x0C] &= ~HAS_DATA & 0xFF
        out.append(bytes(block))
    return out


def check(old, new, anims, base, external):
    a = contents(old, {}, base, set())
    b = contents(new, anims, base, external)
    if len(a) != len(b):
        raise ValueError('split model has %d arrays, the original %d' % (len(b), len(a)))
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            raise ValueError('split model does not read back as the original (array %d: %d bytes, was %d)'
                             % (i, len(y), len(x)))


def split_file(path, out_dir=None):
    data = open(path, 'rb').read()
    model, anims = split(data, os.path.basename(path))
    out_dir = out_dir or os.path.dirname(path)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, os.path.basename(path)), 'wb').write(model)
    for name, anim in anims.items():
        open(os.path.join(out_dir, name), 'wb').write(anim)
    return len(data), len(model), anims


if __name__ == '__main__':
    before, after, anims = split_file(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print('%s: %d -> %d bytes, %d .anim files (%d bytes, largest %d)' % (
        sys.argv[1], before, after, len(anims), sum(map(len, anims.values())), max(map(len, anims.values()), default=0)))
