#!/usr/bin/env python3
"""Keep converted MoP M2s out of the client's doodad batching (M2BatchDoodads), which makes them flicker.

  python -I mop_m2_nobatch.py FOLDER_OR_SKIN...

The client draws copies of a doodad batch flagged 0x10 in its .skin as one instanced draw (CM2Scene, DrawBatchDoodad).
For wotlkconv's MoP doodads that draw puts copies in the wrong place or drops them, and which copies share a draw changes
with what is in view, so trees, rocks and grass blink in and out as the camera turns (gone with M2BatchDoodads 0).
Clearing the flag draws each copy on its own, as M2BatchDoodads 0 does, for these models only.
shortcut: the instancing fault itself isn't found; find it in the client if draw calls on MoP maps get too costly."""
import glob, os, struct, sys

BATCH, BATCHABLE = 24, 0x10


def patch(path):
    s = bytearray(open(path, 'rb').read())
    if s[:4] != b'SKIN':
        return 0
    nb, ob = struct.unpack_from('<II', s, 0x24)
    changed = 0
    for b in range(nb):
        if s[ob + BATCH * b] & BATCHABLE:
            s[ob + BATCH * b] &= ~BATCHABLE & 0xFF
            changed += 1
    if changed:
        open(path, 'wb').write(s)
    return changed


def main():
    files = []
    for x in sys.argv[1:]:
        files += glob.glob(os.path.join(x, '**', '*.skin'), recursive=True) if os.path.isdir(x) else [x]
    n = sum(1 for f in files if patch(f))
    print('unbatched %d of %d skins' % (n, len(files)))


if __name__ == '__main__':
    main()
