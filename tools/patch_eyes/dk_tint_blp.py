#!/usr/bin/env python3
"""Make a pale, ashen Death Knight version of a BLP2 skin/face/fur texture without re-encoding it.
Palettized BLPs (compression 1, the format of the compositor body/face textures) only get their palette recoloured;
DXT BLPs (compression 2) get their colour block endpoints recoloured, so the pixels and the mip chain stay as they were.
usage: dk_tint_blp.py in.blp out.blp [desaturation=0.85] [brightness=0.85] [lift=28]"""
import struct, sys

src, dst = sys.argv[1:3]
desat = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
bright = float(sys.argv[4]) if len(sys.argv) > 4 else 0.85
lift = float(sys.argv[5]) if len(sys.argv) > 5 else 28
TINT = (0.93, 0.98, 1.07)                                         # cold, slightly blue undead pallor

def tint(r, g, b):
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    grey = lum * bright + lift
    return tuple(max(0, min(255, round((grey * t) * desat + c * (1 - desat)))) for c, t in zip((r, g, b), TINT))

d = bytearray(open(src, 'rb').read())
magic, typ, enc, adepth, atype, mips, w, h = struct.unpack_from('<4sIBBBBII', d, 0)
assert magic == b'BLP2' and typ == 1, src + ' is not a BLP2 texture'
offs = struct.unpack_from('<16I', d, 20); sizes = struct.unpack_from('<16I', d, 84)

if enc == 1:                                                      # BGRA palette of 256 entries after the header
    for i in range(256):
        b, g, r, a = d[148 + 4*i:152 + 4*i]; r, g, b = tint(r, g, b); d[148 + 4*i:152 + 4*i] = bytes((b, g, r, a))
elif enc == 2:
    bs = 8 if atype == 0 else 16; co = bs - 8                     # colour half of the block (after DXT3/5 alpha)
    to565 = lambda r, g, b: (round(r * 31 / 255) << 11) | (round(g * 63 / 255) << 5) | round(b * 31 / 255)
    def from565(c): return ((c >> 11) & 31) * 255 // 31, ((c >> 5) & 63) * 255 // 63, (c & 31) * 255 // 31
    for o, n in zip(offs, sizes):
        if not n: continue
        for p in range(o + co, o + n, bs):
            c0, c1, bits = struct.unpack_from('<HHI', d, p)
            n0, n1 = to565(*tint(*from565(c0))), to565(*tint(*from565(c1)))
            if bs == 8 and c0 <= c1:                              # DXT1 3-colour/transparent mode needs c0 <= c1
                if n0 > n1:
                    n0, n1 = n1, n0; bits = sum((((bits >> 2*i) & 3) ^ (1 if ((bits >> 2*i) & 3) < 2 else 0)) << 2*i for i in range(16))
            else:                                                 # 4-colour mode needs c0 > c1
                if n0 < n1:
                    n0, n1 = n1, n0; bits ^= 0x55555555           # swaps 0<->1 and 2<->3
                elif n0 == n1:
                    if n0 > 0: n1 -= 1
                    else: n0 += 1
            struct.pack_into('<HHI', d, p, n0, n1, bits)
else:
    sys.exit('unsupported BLP compression %d in %s' % (enc, src))
open(dst, 'wb').write(d)
