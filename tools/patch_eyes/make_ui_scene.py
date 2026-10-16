#!/usr/bin/env python3
"""Copy a glue scene M2 (UI_<Race>.m2 + its 4 skins) to a new race name and move its camera back so a bigger
character is framed like the original one.
The camera position and target are scaled by SCALE about the character attachment point (attachment 0), so the view
direction is unchanged and the character keeps the same on-screen proportions it would have had at scale 1.
usage: make_ui_scene.py UI_Tauren.m2 NewName SCALE [outdir]
  e.g. make_ui_scene.py UI_Tauren.m2 HighmountainTauren 1.45 out/   ->  out/UI_HighmountainTauren.m2 + 4 skins"""
import struct, sys, os, shutil
src, newname, scale = sys.argv[1], sys.argv[2], float(sys.argv[3]); out = sys.argv[4] if len(sys.argv) > 4 else '.'
base = os.path.splitext(src)[0]
m = bytearray(open(src, 'rb').read())
assert m[:4] == b'MD20' and struct.unpack_from('<I', m, 4)[0] == 264
na, oa = struct.unpack_from('<II', m, 0xf0); assert na >= 1, 'no attachments'
ax, ay, az = struct.unpack_from('<3f', m, oa + 8)           # attachment 0 = where the character stands
nc, oc = struct.unpack_from('<II', m, 0x110); assert nc == 1, 'expected a single camera'
pb = list(struct.unpack_from('<3f', m, oc + 36)); tb = list(struct.unpack_from('<3f', m, oc + 68))
base_pt = (ax, ay, az)
mv = lambda p: [base_pt[i] + (p[i] - base_pt[i]) * scale for i in range(3)]
np_, nt_ = mv(pb), mv(tb)
struct.pack_into('<3f', m, oc + 36, *np_); struct.pack_into('<3f', m, oc + 68, *nt_)
print('character attachment', [round(x, 3) for x in base_pt])
print('camera position  %s -> %s' % ([round(x, 3) for x in pb], [round(x, 3) for x in np_]))
print('camera target    %s -> %s' % ([round(x, 3) for x in tb], [round(x, 3) for x in nt_]))
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'UI_%s.m2' % newname), 'wb').write(m)
for i in range(4):
    sp = '%s%02d.skin' % (base, i)
    if os.path.exists(sp): shutil.copy(sp, os.path.join(out, 'UI_%s%02d.skin' % (newname, i)))
print('wrote UI_%s.m2 + skins to %s' % (newname, out))