#!/usr/bin/env python3
"""Drop second texture layers of converted MoP M2s that the 3.3.5a client can't shade like MoP.

  python -I mop_m2_env.py FOLDER_OR_M2...

Many MoP doodads and creatures (training dummies, weapon racks, hats, lanterns) draw a second texture layer on UV
combo -1, a sphere-mapped reflection such as item\\objectcomponents\\weapon\\armorreflect3_horde.blp, which MoP adds
weighted by a mask. 3.3.5a has no such combiner: with wotlkconv's header flags 0 the client multiplies the mostly dark
reflection in (CM2Shared::SubstituteSimpleShaders) and the model turns black; given a combiner table, Add washes hats
and paper lanterns out to white and Mod2xNA still turns dummies black. So these batches keep only their first
texture: the model's own colours without the shine.

Trunks (the Wandering Isle's red trees) draw their texture a second time on UV set 1, which MoP brightens back
(Mod2x-like) but the client multiplies in plainly, so a trunk comes out much darker than its roots, separate models
with the same texture drawn once. Such repeated-texture layers are dropped too; second layers with another texture on
UV set 1 (grime and detail overlays) are kept.

Glow layers (a second texture of type 12, a creature's second skin, or named *glow*, on the base's UVs: the Onyx
Serpent's PandarenSerpentGod_Black_Glow) are added in MoP; multiplied, a mostly black glow map turns the model black.
Models with one get header flag 8 and a combiner table (the name, global loops or sequences wotlkconv puts in the
0x130 header slot move to the end of the file): glow batches Mod + Add, every other batch the ops the client gave it
before (first layer Mod, which it makes Opaque for opaque materials, second layer Opaque). Alpha-blended batches with
a second texture on UV set 1 (waterfalls: pandawater_06 + pandawater_color_07, both with alpha that fades the fall
into the river) get Mod + Mod, so the second layer's alpha counts too; the default keeps only the first's and the
falls end in hard edges.

Bone tracks with a single key late in a zero-length global sequence (tu_redtree_leaffall_01's emitter bone: one
rotation at 6000 ms, turning the emitter to face down) never reach it in the client, which uses the default before
the first key. Such lone keys move to time 0.

Particle emitters' zsource track comes out as 255 from wotlkconv (69 F-134 models; MoP Classic keeps the real value,
0, in its EXP2 chunk). A nonzero zsource makes the client send every particle along -Z from that point
(CPlaneParticleEmitter::CreateParticle), which the leaf emitters' downward-turned bone flips to straight up: the red
trees' leaves flew into the sky. 255 becomes 0. Safe to rerun."""
import glob, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m2_retail_combiners import (ADD, BATCH, HEADER_COMBINERS, MOD, OPAQUE, TEXTURE_COMBOS, UV_COMBOS,  # noqa: E402
                                 append_data, arr, table)

# header arrays (count, offset) of a 3.3.5 M2, and the element size of those that hold no pointers and can move
ARRAYS = (0x08, 0x14, 0x1C, 0x24, 0x2C, 0x34, 0x3C, 0x48, 0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88, 0x90, 0x98,
          0xD8, 0xE0, 0xE8, 0xF0, 0xF8, 0x100, 0x108, 0x110, 0x118, 0x120, 0x128)
MOVABLE = {0x08: 1, 0x14: 4, 0x1C: 64}      # name, global loops, sequences


def enable_combiners(d):
    """Free the 0x130 header slot and set flag 8; False when something unmovable sits there."""
    for field in ARRAYS:
        n, o = arr(d, field)
        if n and o < HEADER_COMBINERS + 8 and o + n * MOVABLE.get(field, 1) > HEADER_COMBINERS:
            if field not in MOVABLE:
                return False
            struct.pack_into('<II', d, field, n, append_data(d, bytes(d[o:o + n * MOVABLE[field]])))
    struct.pack_into('<I', d, 0x10, struct.unpack_from('<I', d, 0x10)[0] | 8)
    return True


def set_combiners(path):
    """Mod + Add for glow layers, Mod + Mod for alpha-blended batches with a second texture on UV set 1; returns the
    number of such batches (0 when the model has none or already has these ops)."""
    d = bytearray(open(path, 'rb').read())
    tex_combos, uv_combos = table(d, TEXTURE_COMBOS), table(d, UV_COMBOS, 'h')
    nt, ot = arr(d, 0x50)
    kinds, names = [], []
    for i in range(nt):
        kind, _, ln, so = struct.unpack_from('<IIII', d, ot + 16 * i)
        kinds.append(kind)
        names.append(bytes(d[so:so + ln]).lower() if ln else b'')
    nm, om = arr(d, 0x70)
    blend = [struct.unpack_from('<HH', d, om + 4 * i)[1] for i in range(nm)]
    skins, special = [], 0
    for skin_path in sorted(glob.glob(path[:-3] + '0?.skin')):
        s = bytearray(open(skin_path, 'rb').read())
        nb, ob = arr(s, 0x24)
        batches = []
        for b in range(nb):
            o = ob + BATCH * b
            material, = struct.unpack_from('<H', s, o + 10)
            count, tex, uv = struct.unpack_from('<HHH', s, o + 14)
            second = tex_combos[tex + 1] if count == 2 and tex + 1 < len(tex_combos) else None
            uv2 = uv_combos[uv + 1] if second is not None and uv + 1 < len(uv_combos) else None
            ops = (MOD, OPAQUE)[:max(count, 1)]
            if second is not None and second < nt and uv2 == uv_combos[uv] and (
                    kinds[second] == 12 or b'glow' in names[second]):
                ops = (MOD, ADD)
            elif uv2 == 1 and second != tex_combos[tex] and material < len(blend) and blend[material] == 2:
                ops = (MOD, MOD)     # waterfalls: the second layer's alpha shapes the fall
            special += ops != (MOD, OPAQUE)[:max(count, 1)]
            batches.append((o, ops))
        skins.append((skin_path, s, batches))
    if not special:
        return 0
    if struct.unpack_from('<I', d, 0x10)[0] & 8:
        have = table(d, HEADER_COMBINERS)
        if all(tuple(have[sh:sh + len(ops)]) == ops for _, s, bs in skins for o, ops in bs
               for sh in [struct.unpack_from('<H', s, o + 2)[0]]):
            return 0
    if not enable_combiners(d):
        return 0
    combiners = []

    def combiner(ops):
        for i in range(len(combiners) - len(ops) + 1):
            if combiners[i:i + len(ops)] == list(ops):
                return i
        combiners.extend(ops)
        return len(combiners) - len(ops)

    for skin_path, s, batches in skins:
        for o, ops in batches:
            struct.pack_into('<H', s, o + 2, combiner(ops))
        open(skin_path, 'wb').write(s)
    struct.pack_into('<II', d, HEADER_COMBINERS, len(combiners),
                     append_data(d, struct.pack('<%dH' % len(combiners), *combiners)))
    open(path, 'wb').write(d)
    return special


def patch(path):
    d = open(path, 'rb').read()
    if d[:4] != b'MD20':
        return 0
    uv_combos = table(d, UV_COMBOS, 'h')
    tex_combos = table(d, TEXTURE_COMBOS)
    dropped = 0
    for skin_path in sorted(glob.glob(path[:-3] + '0?.skin')):
        s = bytearray(open(skin_path, 'rb').read())
        nb, ob = arr(s, 0x24)
        changed = 0
        for b in range(nb):
            o = ob + BATCH * b
            count, tex, uv = struct.unpack_from('<HHH', s, o + 14)
            if count != 2 or uv + 1 >= len(uv_combos):
                continue
            repeated = uv_combos[uv + 1] == 1 and tex + 1 < len(tex_combos) and tex_combos[tex] == tex_combos[tex + 1]
            if uv_combos[uv + 1] == -1 or repeated:
                struct.pack_into('<H', s, o + 14, 1)
                changed += 1
        if changed:
            open(skin_path, 'wb').write(s)
            dropped += changed
    return dropped


def zero_lone_keys(path):
    """Move single bone keys to time 0; returns how many moved."""
    d = bytearray(open(path, 'rb').read())
    if d[:4] != b'MD20':
        return 0
    moved = 0
    bn, bo = arr(d, 0x2C)
    for b in range(bn):
        for t in range(3):                          # translation, rotation, scale tracks of an 88-byte bone
            track = bo + 88 * b + 16 + 20 * t
            # only global-sequence tracks: the others' keys of sequences kept in .anim files point into those
            # files, not this one (writing there zeroed the header of models with .anim files)
            if struct.unpack_from('<h', d, track + 2)[0] < 0:
                continue
            tn, to = struct.unpack_from('<II', d, track + 4)
            for i in range(tn):
                count, at = struct.unpack_from('<II', d, to + 8 * i)
                if count == 1 and at + 4 <= len(d) and struct.unpack_from('<I', d, at)[0]:
                    struct.pack_into('<I', d, at, 0)
                    moved += 1
    if moved:
        open(path, 'wb').write(d)
    return moved


def clear_zsource(path):
    """Particle zsource keys of 255 (not MoP's: its EXP2 chunk holds 0) back to 0; returns how many."""
    d = bytearray(open(path, 'rb').read())
    if d[:4] != b'MD20':
        return 0
    cleared = 0
    n, o = arr(d, 0x128)
    for i in range(n):
        _, _, _, _, vn, vo = struct.unpack_from('<HhIIII', d, o + 476 * i + 0xF0)
        for k in range(vn):
            count, at = struct.unpack_from('<II', d, vo + 8 * k)
            for j in range(count):
                if struct.unpack_from('<f', d, at + 4 * j)[0] == 255.0:
                    struct.pack_into('<f', d, at + 4 * j, 0.0)
                    cleared += 1
    if cleared:
        open(path, 'wb').write(d)
    return cleared


def main():
    files = []
    for x in sys.argv[1:]:
        files += glob.glob(os.path.join(x, '**', '*.m2'), recursive=True) if os.path.isdir(x) else [x]
    counts = [patch(f) for f in files]
    glows = [set_combiners(f) for f in files]
    print('dropped the second layer of %d batches in %d of %d models; %d glow and two-layer alpha batches in %d models given combiners' % (
        sum(counts), sum(1 for c in counts if c), len(files), sum(glows), sum(1 for g in glows if g)))
    print('moved %d lone bone keys to time 0' % sum(zero_lone_keys(f) for f in files))
    print('cleared %d particle zsource keys of 255' % sum(clear_zsource(f) for f in files))


if __name__ == '__main__':
    main()
