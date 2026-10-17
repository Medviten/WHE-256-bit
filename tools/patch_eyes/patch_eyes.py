#!/usr/bin/env python3
"""Turn the eye texture slot (type 5, empty filename) of the M2 into a normal file texture.
usage: python patch_eyes.py in.m2 out.m2 "Character\\highmountaintauren\\male\\eyes0_0_1.blp" [slot]"""
import struct, sys
src, dst, path = sys.argv[1:4]
slot = int(sys.argv[4]) if len(sys.argv) > 4 else 9
d = bytearray(open(src, 'rb').read())
assert d[:4] == b'MD20' and struct.unpack_from('<I', d, 4)[0] == 264, 'expects a v264 (WotLK) M2'
count, ofs = struct.unpack_from('<II', d, 0x50)          # M2 textures array
rec = ofs + slot * 16
ttype, flags, ln, off = struct.unpack_from('<IIII', d, rec)
print('slot', slot, 'of', count, ': type', ttype, 'flags', flags, 'len', ln)
assert ttype == 5 and ln <= 1, 'slot %d is not the empty type-5 eye texture' % slot
name = path.encode() + b'\0'
new_off = len(d)
d += name                                                  # v264 offsets are absolute; appending is safe
struct.pack_into('<IIII', d, rec, 0, flags, len(name), new_off)
open(dst, 'wb').write(d)
print('patched ->', dst, '| texture', slot, '=', path)