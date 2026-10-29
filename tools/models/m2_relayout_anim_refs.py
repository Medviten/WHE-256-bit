"""Rebuild the .anim references of a 3.3.5 (version 264) M2 whose external sequences point at the wrong places, when
there is no source model to copy them from (see m2_restore_anim_refs.py for when there is).

The client relocates the inner arrays of every track of a sequence without flag 0x20 against its .anim file (see
m2_anim_split.py); a reference past the end of the file makes it read out of bounds and crash. Blizzard's .anim files
hold those arrays in the order of the model's tracks, each 16-byte aligned, so the offsets follow from the counts. For
each external sequence the arrays are laid out that way; a sequence is fixed only when every times array placed in the
file is sorted and within the sequence's duration and the placed arrays end where the file does. Arrays left over past
the end (tracks added to the model after its .anim files were made, e.g. anim events) are emptied, as they have no data.

Sequences that an earlier fix took out of the sequence lookup (furbolg_fix_anims.py) are put back once fixed. The lookup
is a hash (id % count, quadratic probing), so it is rebuilt rather than patched.

usage: python -I m2_relayout_anim_refs.py <model.m2>   (in place; its .anim files sit next to it under its name)"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_anim_split import ALIAS, HAS_DATA, SEQUENCE_SIZE, anim_name, arr, pointers, sequences   # noqa: E402


def anim_file(path, name):
    """The .anim file, matched without regard to case as the client's MPQ lookup does."""
    folder = os.path.dirname(path)
    wanted = os.path.basename(name).lower()
    for f in os.listdir(folder):
        if f.lower() == wanted:
            return os.path.join(folder, f)
    return None


def layout(data, ptrs, s, size, duration):
    """[(position of the inner array entry, count, new offset or None to empty)] for sequence s, or None when its
    .anim does not follow the layout."""
    out, offset, end = [], 0, 0
    for pos, element, q in ptrs:
        if q != s or not arr(data, pos)[0]:
            continue
        count = arr(data, pos)[0]
        offset = (offset + 15) & ~15
        if offset + count * element > size:
            out.append((pos, count, None))
        elif any(new is None for _, _, new in out):
            return None   # an array that fits after one that does not: not this layout
        else:
            out.append((pos, count, offset))
            end = offset + count * element
        offset += count * element
    if not out or (end + 15) & ~15 != (size + 15) & ~15:
        return None
    return out


def relayout(path):
    data = bytearray(open(path, 'rb').read())
    if data[:4] != b'MD20' or struct.unpack_from('<I', data, 4)[0] != 264:
        raise ValueError('not a version 264 M2')
    seqs = sequences(data)
    seq_offset = arr(data, 0x1C)[1]
    external = {s for s, seq in enumerate(seqs) if not seq[2] & (HAS_DATA | ALIAS)}
    ptrs, _ = pointers(data, external)
    base = path[:-3]

    fixed = set()
    for s in sorted(external):
        name = anim_file(path, anim_name(seqs, base, s))
        if not name:
            print('sequence %d (anim %d): no .anim file, left alone' % (s, seqs[s][0]))
            continue
        anim = open(name, 'rb').read()
        duration = struct.unpack_from('<I', data, seq_offset + SEQUENCE_SIZE * s + 4)[0]
        entries = layout(data, ptrs, s, len(anim), duration)
        valid = entries is not None
        for pos, count, new in entries or []:
            element = next(e for p, e, q in ptrs if p == pos)
            if new is not None and element == 4:
                times = struct.unpack_from('<%dI' % count, anim, new)
                valid = valid and list(times) == sorted(times) and times[-1] <= duration
        if not valid:
            print('sequence %d (anim %d): %s does not follow the layout, left alone'
                  % (s, seqs[s][0], os.path.basename(name)))
            continue
        moved = emptied = 0
        for pos, count, new in entries:
            if new is None:
                struct.pack_into('<II', data, pos, 0, 0)
                emptied += 1
            elif arr(data, pos)[1] != new:
                struct.pack_into('<II', data, pos, count, new)
                moved += 1
        fixed.add(s)
        print('sequence %d (anim %d): %d references rebuilt, %d emptied' % (s, seqs[s][0], moved, emptied))

    # put fixed sequences back into the lookup: the first sequence of each anim id
    count, offset = arr(data, 0x24)
    heads = [x for x in struct.unpack_from('<%dH' % count, data, offset) if x != 0xFFFF]
    ids = {seqs[x][0] for x in heads}
    readded = [s for s in sorted(fixed) if seqs[s][1] == 0 and seqs[s][0] not in ids]
    if readded:
        table = [0xFFFF] * count
        for i in heads + readded:
            slot, step = seqs[i][0] % count, 1
            while table[slot] != 0xFFFF:
                slot = (slot + step * step) % count
                step += 1
            table[slot] = i
        struct.pack_into('<%dH' % count, data, offset, *table)
        print('sequence lookup rebuilt: anims %s put back' % ', '.join(str(seqs[s][0]) for s in readded))

    open(path, 'wb').write(data)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    relayout(sys.argv[1])
