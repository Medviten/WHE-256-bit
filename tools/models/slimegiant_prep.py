"""Make the converted retail SlimeSkeleton (FileDataID 3490792) a 3.3.5 player model.

Input: the 3.3.5 .m2 and 00.skin written by wotlkconv. Output: the same files, patched in place (no layout
change) so the character code drives them, after Kalibro's SlimeGiant.h player adapter:

- texture 0 (retail type 11, the colour atlas) becomes type 1: the composited body texture, i.e. the
  CharSections skin row's first texture (creatureSkinRaces keeps it whole, alpha included)
- texture 2 (retail type 12, the tiling goo) becomes type 8: the skin row's second texture
- submesh 3 (the drip) gets geoset 102, so facial hair style 1 (geoset_1 = 2) shows it and style 0 hides it
- batch 0 (the skeleton) gets the retail effect 0 back, which is 3.3.5's shader 0x8001
  (Combiners_Opaque_Mod2xNA_Alpha + Diffuse_T1_Env); the converter had reset it. The goo batches keep the
  3.3.5 default (Mod_Opaque): their retail combiners need texture combiner combos, which would change the
  file layout.

Usage: python -I slimegiant_prep.py <in.m2> <in00.skin> <out.m2> <out00.skin>
"""

import pathlib
import struct
import sys

DRIP_GEOSET = 102
SKELETON_SHADER = 0x8001
TEXTURES = 0x50          # M2Array<M2Texture>, 16 bytes each
REPLACEABLE_LOOKUP = 0x68  # M2Array<int16>, indexed by texture type


def prepare_model(data):
    b = bytearray(data)
    if b[:4] != b"MD20" or struct.unpack_from("<I", b, 4)[0] != 264:
        sys.exit("not a 3.3.5 (version 264) M2")
    count, offset = struct.unpack_from("<II", b, TEXTURES)
    types = [struct.unpack_from("<I", b, offset + i * 16)[0] for i in range(count)]
    if types != [11, 0, 12]:
        sys.exit(f"unexpected source model: texture types {types}")
    struct.pack_into("<I", b, offset, 1)
    struct.pack_into("<I", b, offset + 2 * 16, 8)
    count, offset = struct.unpack_from("<II", b, REPLACEABLE_LOOKUP)
    if count < 13:
        sys.exit(f"unexpected source model: replaceable texture lookup has {count} entries")
    lookup = {1: 0, 8: 2, 11: -1, 12: -1}
    for texture_type, index in lookup.items():
        struct.pack_into("<h", b, offset + texture_type * 2, index)
    return bytes(b)


def prepare_skin(data):
    b = bytearray(data)
    if b[:4] != b"SKIN":
        sys.exit("not a 3.3.5 skin")
    count, offset = struct.unpack_from("<II", b, 0x1C)
    if count != 4 or any(struct.unpack_from("<H", b, offset + i * 48)[0] for i in range(4)):
        sys.exit("unexpected source skin: expected 4 submeshes, all geoset 0")
    struct.pack_into("<H", b, offset + 3 * 48, DRIP_GEOSET)
    count, offset = struct.unpack_from("<II", b, 0x24)
    if count != 4:
        sys.exit("unexpected source skin: expected 4 batches")
    struct.pack_into("<H", b, offset + 2, SKELETON_SHADER)
    return bytes(b)


if __name__ == "__main__":
    src_m2, src_skin, dst_m2, dst_skin = sys.argv[1:5]
    out_m2 = prepare_model(pathlib.Path(src_m2).read_bytes())
    out_skin = prepare_skin(pathlib.Path(src_skin).read_bytes())
    pathlib.Path(dst_m2).write_bytes(out_m2)
    pathlib.Path(dst_skin).write_bytes(out_skin)
    print("wrote", dst_m2, len(out_m2), "bytes;", dst_skin, len(out_skin), "bytes")
