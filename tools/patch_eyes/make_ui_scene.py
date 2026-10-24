#!/usr/bin/env python3
"""Copy a glue scene M2 (UI_<Race>.m2 + its 4 skins) to a new race name and move its camera back so a bigger
character is framed like the original one.
The camera position and target are scaled by SCALE about the character attachment point (attachment 0), so the view
direction is unchanged and the character keeps the same on-screen proportions it would have had at scale 1.
Screen overlays (submeshes lying right in front of the camera, like UI_Tauren's full-screen lensAlpha quad) are moved
the same way, or they would shrink to a box in the middle of the screen.
usage: make_ui_scene.py UI_Tauren.m2 NewName SCALE [outdir]
  e.g. make_ui_scene.py UI_Tauren.m2 HighmountainTauren 1.45 out/   ->  out/UI_HighmountainTauren.m2 + 4 skins"""
import struct, sys, os, shutil, math
OVERLAY = 0.2   # a submesh whose vertices are all within this fraction of the camera-to-character distance is an overlay
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
nv, ov = struct.unpack_from('<II', m, 0x3c); vpos = lambda v: struct.unpack_from('<3f', m, ov + 48 * v)
s = open(base + '00.skin', 'rb').read()                      # the skins index the same model vertices
ni, oi = struct.unpack_from('<II', s, 4); idx = struct.unpack_from('<%dH' % ni, s, oi)
nsm, osm = struct.unpack_from('<II', s, 0x1c)
sets = [set(idx[vs:vs + vc]) for vs, vc in (struct.unpack_from('<2H', s, osm + 48 * j + 4) for j in range(nsm))]
reach = OVERLAY * math.dist(pb, base_pt)
for j, verts in enumerate(sets):
    if not verts or any(math.dist(vpos(v), pb) > reach for v in verts):
        continue
    assert not any(verts & other for k, other in enumerate(sets) if k != j), 'overlay %d shares vertices' % j
    for v in verts: struct.pack_into('<3f', m, ov + 48 * v, *mv(vpos(v)))
    print('moved overlay submesh %d (%d vertices) with the camera' % (j, len(verts)))
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'UI_%s.m2' % newname), 'wb').write(m)
for i in range(4):
    sp = '%s%02d.skin' % (base, i)
    if os.path.exists(sp): shutil.copy(sp, os.path.join(out, 'UI_%s%02d.skin' % (newname, i)))
print('wrote UI_%s.m2 + skins to %s' % (newname, out))