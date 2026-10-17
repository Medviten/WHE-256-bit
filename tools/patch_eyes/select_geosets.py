#!/usr/bin/env python3
"""Rebuild a WotLK (v264) skin from a chosen set of geosets, renumbering them for the 3.3.5 client, and repoint
texture paths of the M2.
Retail ports (Kalibros etc.) carry far more than 65535 triangle indices and use geoset groups the 3.3.5 client never
enables (horns 24xx, tails 38xx, faces 1xxxx ...). The client ignores the skin section 'level' field, so any submesh
starting past index 65535 is drawn from the wrong triangles (the "cloud of particles"), and unknown groups stay hidden.
This keeps only the listed geosets, gives them IDs the client understands and packs them below 65536 indices.

usage: select_geosets.py in.m2 out.m2 out.skin [--retex OLD=NEW]... [--before ID] --skin a.skin RULE... [--skin b.skin RULE...]
  RULE  ID           keep that geoset as it is            e.g. 0  1301
        LO-HI        keep a range                          e.g. 401-404
        ID=NEW       keep and renumber                     e.g. 19601=0
        LO-HI=NEW    keep a range, numbered NEW, NEW+1 ... e.g. 2401-2409=1   (horn styles -> hair geosets 1..9)
  --skin   every --skin after the first must belong to the same M2 vertex/bone data (e.g. the untouched original skin
           of a model whose first skin was already edited); its submeshes are added after those of the first skin
  --before put the submeshes of the later skins in front of the first submesh of the first skin with this geoset ID
           (keeps late transparent overlays such as the DK eye glow 1703 drawn last)
  --retex  replace the prefix OLD of every texture filename with NEW (case-insensitive, '\\' or '/' both accepted)
e.g. select_geosets.py hmt.m2 out.m2 out00.skin --retex "custom\\highmountain\\native\\male\\=Character\\highmountaintauren\\male\\"
       --skin cur00.skin 0 401-404 1301 --skin orig00.skin 2401-2409=1 3802=0"""
import struct, sys

def parse_rules(words):
    rules = []
    for w in words:
        src, _, dst = w.partition('=')
        lo, _, hi = src.partition('-'); lo = int(lo); hi = int(hi) if hi else lo
        rules.append((lo, hi, int(dst) if dst else None))
    return rules

def new_id(rules, gid):
    for lo, hi, dst in rules:
        if lo <= gid <= hi: return gid if dst is None else dst + (gid - lo)
    return None

def read_skin(path):
    s = open(path, 'rb').read()
    magic, ni, oi, nt, ot, np_, op, ns, os_, nb, ob, bmax = struct.unpack_from('<4s11I', s, 0)
    assert magic == b'SKIN', path + ' is not a skin'
    return dict(look=struct.unpack_from('<%dH' % ni, s, oi), tri=struct.unpack_from('<%dH' % nt, s, ot),
                props=[s[op + 4*i:op + 4*i + 4] for i in range(np_)],
                subs=[bytearray(s[os_ + 48*i:os_ + 48*i + 48]) for i in range(ns)],
                bats=[bytearray(s[ob + 24*i:ob + 24*i + 24]) for i in range(nb)], bmax=bmax)

a = sys.argv[1:]
m2_in, m2_out, skin_out = a[:3]; a = a[3:]
retex, before, skins = [], None, []
while a:
    if a[0] == '--retex': old, new = a[1].split('=', 1); retex.append((old.replace('/', '\\').lower(), new.replace('/', '\\'))); a = a[2:]
    elif a[0] == '--before': before = int(a[1]); a = a[2:]
    elif a[0] == '--skin':
        j = 2
        while j < len(a) and not a[j].startswith('--'): j += 1
        skins.append((a[1], parse_rules(a[2:j]))); a = a[j:]
    else: sys.exit('unexpected argument ' + a[0])
assert skins, 'no --skin given'

m = bytearray(open(m2_in, 'rb').read())
assert m[:4] == b'MD20' and struct.unpack_from('<I', m, 4)[0] == 264, 'expects a v264 (WotLK) M2'
nv = struct.unpack_from('<I', m, 0x3c)[0]

# ---------- texture paths
tn, to = struct.unpack_from('<II', m, 0x50)
for i in range(tn):
    rec = to + 16*i; ttype, fl, ln, off = struct.unpack_from('<IIII', m, rec)
    if ttype != 0 or ln <= 1: continue
    name = m[off:off + ln].rstrip(b'\0').decode('latin-1')
    for old, new in retex:
        if name.lower().startswith(old):
            nm = (new + name[len(old):]).encode('latin-1') + b'\0'; o = len(m); m += nm   # v264 offsets are absolute
            struct.pack_into('<IIII', m, rec, ttype, fl, len(nm), o)
            print('texture %2d: %s -> %s' % (i, name, nm[:-1].decode('latin-1'))); break

# ---------- pick submeshes: (skin, submesh index, new geoset id)
loaded = [(read_skin(p), rules) for p, rules in skins]
first = [(0, i, new_id(loaded[0][1], struct.unpack_from('<H', sb, 0)[0])) for i, sb in enumerate(loaded[0][0]['subs'])]
later = [(k, i, new_id(rules, struct.unpack_from('<H', sb, 0)[0]))
         for k, (sk, rules) in enumerate(loaded) if k for i, sb in enumerate(sk['subs'])]
first = [x for x in first if x[2] is not None]; later = [x for x in later if x[2] is not None]
cut = len(first)
if before is not None:
    hits = [n for n, (k, i, _) in enumerate(first) if struct.unpack_from('<H', loaded[0][0]['subs'][i], 0)[0] == before]
    if hits: cut = hits[0]
order = first[:cut] + later + first[cut:]

# ---------- rebuild skin
# every submesh gets its own vertex and index window: overlapping windows (storing triangles shared by two geosets
# once) made the 3.3.5 client crash intermittently
look, tri, props, subs, bats = [], [], [], [], []
newidx = {}
for n, (k, i, gid) in enumerate(order):
    sk = loaded[k][0]; sb = bytearray(sk['subs'][i])
    sid, lvl, vs, vc, is_, ic = struct.unpack_from('<6H', sb, 0); st = (lvl << 16) | is_
    assert all(sk['look'][vs + v] < nv for v in range(vc)), 'skin %s references vertices the M2 does not have' % skins[k][0]
    assert all(vs <= t < vs + vc for t in sk['tri'][st:st + ic]), 'submesh %d of %s uses vertices outside its range' % (i, skins[k][0])
    nvs, nis = len(look), len(tri)
    look += sk['look'][vs:vs + vc]; props += sk['props'][vs:vs + vc]
    tri += [t - vs + nvs for t in sk['tri'][st:st + ic]]
    struct.pack_into('<6H', sb, 0, gid, nis >> 16, nvs, vc, nis & 0xFFFF, ic); subs.append(sb); newidx[(k, i)] = n
# batches: first skin's in their own order, later skins' batches spliced in where their submeshes went
def bats_of(k, wanted):
    out = []
    for b in loaded[k][0]['bats']:
        sec = struct.unpack_from('<H', b, 4)[0]
        if (k, sec) in wanted:
            nb = bytearray(b); struct.pack_into('<HH', nb, 4, newidx[(k, sec)], newidx[(k, sec)]); out.append(nb)
    return out
cut_set = {(0, i) for (_, i, _) in first[:cut]}; tail_set = {(0, i) for (_, i, _) in first[cut:]}
bats = bats_of(0, cut_set) + [b for k in range(1, len(loaded)) for b in bats_of(k, {(kk, i) for (kk, i, _) in later if kk == k})] + bats_of(0, tail_set)

assert len(look) < 65536, 'too many skin vertices: %d' % len(look)
assert len(tri) <= 65535, 'too many triangle indices for the 3.3.5 client: %d (limit 65535)' % len(tri)
pad = lambda b: b + b'\0' * ((-len(b)) % 4)
out = bytearray(48)
oi = len(out); out += pad(struct.pack('<%dH' % len(look), *look))
ot = len(out); out += pad(struct.pack('<%dH' % len(tri), *tri))
op = len(out); out += b''.join(props)
os_ = len(out); out += b''.join(bytes(x) for x in subs)
ob = len(out); out += b''.join(bytes(x) for x in bats)
struct.pack_into('<4s11I', out, 0, b'SKIN', len(look), oi, len(tri), ot, len(props), op, len(subs), os_, len(bats), ob,
                 max(sk['bmax'] for sk, _ in loaded))
open(m2_out, 'wb').write(m); open(skin_out, 'wb').write(out)
ids = {}
for sb in subs: g = struct.unpack_from('<H', sb, 0)[0]; ids[g] = ids.get(g, 0) + 1
print('skin: %d submeshes, %d batches, %d vertices, %d / 65535 triangle indices' % (len(subs), len(bats), len(look), len(tri)))
print('geosets:', ' '.join('%d%s' % (g, 'x%d' % c if c > 1 else '') for g, c in sorted(ids.items())))
