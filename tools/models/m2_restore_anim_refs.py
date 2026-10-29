"""Restore the .anim references of a model converted by wotlkconv from its source model (e.g. a Cataclysm v272 M2).

wotlkconv passes a model's external .anim files through unchanged but rewrites the inner arrays of every track for the
sequences that live in them (sequence flag 0x20 clear) to point into the converted model, at bytes that are not the
animation data. The client relocates those arrays against the sequence's .anim when it loads it (see m2_anim_split.py),
so playing such a sequence (emotes, MountSelfStart, ...) reads past the .anim buffer and crashes. Since the .anim files
are the source's own, the source's inner array entries (count, offset) are copied back for those sequences.

Both models must have the same sequences and the same number of each struct with tracks; every restored entry is checked
to fit in its .anim. Tracks with a global sequence stay in the model and are left alone.

usage: python -I m2_restore_anim_refs.py <converted.m2> <source.m2>   (the converted model is fixed in place; its .anim
files sit next to it under its own name)"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_anim_split import HAS_DATA, TRACKS, anim_name, arr, sequences   # noqa: E402

# source structs laid out unlike version 264's, by source version: header offset -> (struct size, track offsets in the
# order of TRACKS). Cataclysm's camera has no fov field before its tracks and a fov track after them
SOURCE_LAYOUTS = {
    272: {0x110: (116, [0x0C, 0x2C, 0x4C])},
}


def restore(path, source_path):
    data = bytearray(open(path, 'rb').read())
    source = open(source_path, 'rb').read()
    if data[:4] != b'MD20' or source[:4] != b'MD20':
        raise ValueError('not an M2')
    seqs, source_seqs = sequences(data), sequences(source)
    if [s[:2] for s in seqs] != [s[:2] for s in source_seqs]:
        raise ValueError('the models have different sequences')
    external = [s for s in range(len(seqs)) if not seqs[s][2] & HAS_DATA]
    base = path[:-3]
    sizes = {}
    for s in external:
        name = anim_name(seqs, base, s)
        sizes[s] = os.path.getsize(name) if os.path.exists(name) else None

    layouts = SOURCE_LAYOUTS.get(struct.unpack_from('<I', source, 4)[0], {})
    restored = kept = emptied = 0
    for hpos, (struct_size, tracks) in TRACKS.items():
        count, offset = arr(data, hpos)
        source_count, source_offset = arr(source, hpos)
        if count != source_count:
            raise ValueError('header array 0x%X: %d in the model, %d in the source' % (hpos, count, source_count))
        source_size, source_tracks = layouts.get(hpos, (struct_size, [track for track, _ in tracks]))
        for i in range(count):
            for (track, key_size), source_track in zip(tracks, source_tracks):
                t = offset + struct_size * i + track
                st = source_offset + source_size * i + source_track
                if struct.unpack_from('<H', data, t + 2)[0] != 0xFFFF:
                    continue
                for part, size in [(4, 4)] + ([(12, key_size)] if key_size else []):
                    n, o = arr(data, t + part)
                    sn, so = arr(source, st + part)
                    for s in external:
                        if s >= n:
                            continue
                        if s >= sn:
                            raise ValueError('track at 0x%X: sequence %d missing from the source' % (t, s))
                        c, _ = arr(data, o + 8 * s)
                        sc, soff = arr(source, so + 8 * s)
                        # an array the converter emptied (e.g. some camera tracks) is never read
                        if not c:
                            emptied += bool(sc)
                            continue
                        if c != sc:
                            raise ValueError('track at 0x%X, sequence %d: %d keys in the model, %d in the source'
                                             % (t, s, c, sc))
                        if sizes[s] is None or soff + c * size > sizes[s]:
                            raise ValueError('track at 0x%X, sequence %d: source data is not in %s'
                                             % (t, s, anim_name(seqs, base, s)))
                        if arr(data, o + 8 * s)[1] == soff:
                            kept += 1
                        else:
                            struct.pack_into('<II', data, o + 8 * s, c, soff)
                            restored += 1

    open(path, 'wb').write(data)
    print('%s: %d .anim references restored, %d already right, %d left empty (%d external sequences)'
          % (os.path.basename(path), restored, kept, emptied, len(external)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    restore(sys.argv[1], sys.argv[2])
