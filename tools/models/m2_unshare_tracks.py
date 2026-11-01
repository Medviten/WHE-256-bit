"""Give every animation track of a 3.3.5 (version 264) M2 its own per-sequence arrays.

Each track holds two outer arrays (times and keys) of one M2Array per sequence. The client relocates those inner
M2Arrays in place while loading (M2Init), so tracks whose outer arrays point at the same place get them relocated
twice. For tracks on a global sequence the second pass bounds-checks an already relocated header, fails, and the client
rejects the whole model as corrupt: it never draws (no error, the character is just invisible). Other tracks read
garbage. Blizzard's files never share these arrays; some converters merge identical ones (e.g. Vrykul PC models: the
scale tracks of 35 bones, all the same constant key on a global sequence).

Every outer array after the first user of its place is copied to the end of the file (16-byte aligned) and the track
pointed at the copy. The copies keep the inner M2Arrays as they are, so the times and keys themselves stay shared; the
client only reads those.

usage: python -I m2_unshare_tracks.py <model.m2>...   (in place)"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_anim_split import TRACKS, arr   # noqa: E402


def unshare(data):
    """Returns the fixed model and the number of outer arrays copied."""
    data = bytearray(data)
    seen = set()
    copies = 0
    for hpos, (struct_size, tracks) in TRACKS.items():
        count, offset = arr(data, hpos)
        for i in range(count):
            for track, key_size in tracks:
                t = offset + struct_size * i + track
                for outer in [t + 4] + ([t + 12] if key_size else []):
                    n, o = arr(data, outer)
                    if not n:
                        continue
                    if o not in seen:
                        seen.add(o)
                        continue
                    data += b'\0' * (-len(data) % 16)
                    copy = len(data)
                    data += data[o:o + 8 * n]
                    struct.pack_into('<I', data, outer + 4, copy)
                    seen.add(copy)
                    copies += 1
    return bytes(data), copies


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        with open(path, 'rb') as f:
            data = f.read()
        if data[:4] != b'MD20' or struct.unpack_from('<I', data, 4)[0] != 264:
            print('%s: not a version 264 M2, skipped' % path)
            continue
        fixed, copies = unshare(data)
        if copies:
            with open(path, 'wb') as f:
                f.write(fixed)
        print('%s: %d shared track array(s) copied' % (path, copies))


if __name__ == '__main__':
    main()
