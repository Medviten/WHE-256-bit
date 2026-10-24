#!/usr/bin/env python3
"""Fix FurbolgRace.m2's animations, which crashed the client (e.g. on EmoteTalk when talking to an NPC).
- Sequences whose track data is inside the M2 but lack flag 0x20 (so the client looked for .anim files that don't
  exist) get the flag: ReadyRifle, AttackRifle, LoadRifle, HoldRifle.
- Sequences whose .anim file doesn't match the M2 (track offsets run past the end of the file, so the client read out
  of bounds) are dropped from the sequence lookup; the client then falls back through AnimationData.dbc like for any
  animation the model lacks (EmoteTalk, EmoteEat, sit, sleep, use standing).
The sequence lookup is a hash (id % count, quadratic probing), so it is rebuilt rather than patched.
usage: furbolg_fix_anims.py furbolgrace.m2   (in place; the .anim files must sit next to it)"""
import struct, sys, os, glob
p = sys.argv[1]
m = bytearray(open(p, 'rb').read())
assert m[:4] == b'MD20' and struct.unpack_from('<I', m, 4)[0] == 264
stem = os.path.splitext(os.path.basename(p))[0].lower()
anims = {os.path.basename(f).lower(): f for f in glob.glob(os.path.join(os.path.dirname(p), '*.anim'))}
ns, os_ = struct.unpack_from('<II', m, 0x1c)
nb, ob = struct.unpack_from('<II', m, 0x2c)
nh, oh = struct.unpack_from('<II', m, 0x24)

def arrays(i):   # (count, offset, element size) of every bone track array of sequence i
    for b in range(nb):
        for t, vs in ((0, 12), (1, 8), (2, 12)):   # translation, compressed rotation, scale
            it, gs, nts, ots, nvs, ovs = struct.unpack_from('<HhIIII', m, ob + 88 * b + 16 + 20 * t)
            if gs < 0 and i < nts:
                yield struct.unpack_from('<II', m, ots + 8 * i) + (4,)
                yield struct.unpack_from('<II', m, ovs + 8 * i) + (vs,)

dropped = set()
for i in range(ns):
    aid, sub, dur, spd, fl = struct.unpack_from('<HHIfI', m, os_ + 64 * i)
    if fl & 0x60:
        continue
    f = anims.get('%s%04d-%02d.anim' % (stem, aid, sub))
    size = os.path.getsize(f) if f else len(m)
    fits = all(o + c * w <= size for c, o, w in arrays(i) if c)
    if not f and fits:
        struct.pack_into('<I', m, os_ + 64 * i + 12, fl | 0x20)
        print('sequence %d (anim %d): data is in the M2, flagged 0x20' % (i, aid))
    elif not fits:
        dropped.add(i)
        print('sequence %d (anim %d): %s does not match the M2, dropped from the lookup' % (i, aid, os.path.basename(f) if f else 'no .anim'))

heads = [x for x in struct.unpack_from('<%dH' % nh, m, oh) if x != 0xFFFF and x not in dropped]
table = [0xFFFF] * nh
for i in heads:
    aid = struct.unpack_from('<H', m, os_ + 64 * i)[0]
    slot, step = aid % nh, 1
    while table[slot] != 0xFFFF:
        slot = (slot + step * step) % nh; step += 1
    table[slot] = i
struct.pack_into('<%dH' % nh, m, oh, *table)
open(p, 'wb').write(m)
print('rebuilt the sequence lookup: %d animations, %d dropped' % (len(heads), len(dropped)))
