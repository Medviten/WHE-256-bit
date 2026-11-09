#!/usr/bin/env python3
"""Give converted retail character models their two-layer eye and eye-glow shading in the 3.3.5 client.

Retail draws a character's eyes and eye glows with two texture layers combined by a shader (Forever's Skyborne: eyes
0x4013 = Mod_Add, glow 1701 0x4014 = Mod_Mod2x, glows 1702-1705 0x4011 = Mod_Mod; the second layer on UV set 1). The
converted models have header flags 0, and then the client ignores a batch's shader and makes every second layer
"Opaque", i.e. multiplies it in (CM2Shared::SubstituteSimpleShaders): the eye colour is darkened by the glow-dot area of
the eye texture instead of lit by it, and the glows mostly vanish. Eyes look dead.

With header flag 8 the client reads each batch's shader as an index into the model's texture combiner table
(M2Data::m_textureCombinerCombos, header 0x130) and builds the shader from the ops there. This script
- moves the name and global loops, which the converters put right after the 0x130 header, to the end of the file and
  puts the combiner table in the freed 0x130 slot, then sets flag 8;
- gives every batch a combiner that draws it exactly as before (first layer Mod, which the client turns into Opaque
  for an opaque material, second layer Opaque), and points second layers on UV combo -1 (which flag 8 would turn into
  a sphere map) at a UV set 1 entry, the set they are drawn with now;
- gives the eyes Mod_Add (restoring a second layer that an earlier fix removed, when the lookups still pair the eye
  texture with UV set 1), the glow smoke Mod_Mod2x and the glow orbs Mod_Mod, and gives glows that lost their second
  layer in conversion (Haranir) that layer back;
- renumbers the glows to the stock meaning of group 17 (1701 none, 1702 the race's own glow, 1703 death knights).

Retail's glows: 1701 is a smoke trail (80 triangles; layer 1 samples a colour bar, layer 2 on UV set 1 the smoke) and
1702-1705 are glowing orbs with wisps (200 triangles; layer 1 the orb shapes, layer 2 a colour strip whose column picks
the colour: yellow, orange, pale violet, blue). The client shows its default 1701 on everyone and 1703 on death
knights, so retail's numbers put the death knight smoke on every character. Glows are therefore told apart by their
geometry and colour column, not their number (earlier fixes renumbered some), and become:
  smoke -> 1703, blue orbs -> 1703 (a death knight gets both), yellow orbs -> 1702, orange and pale orbs -> PARKED.
1702 shows when a facial style's CharFacialHairStyles geoset 5 is 2, as for Night Elves.

usage: m2_retail_combiners.py MODEL.m2 [...]
Patches the model and all its .skin files in place; safe to rerun."""
import glob, struct, sys

PARKED = 1999
GLOW_IDS = {1701, 1702, 1703, 1704, 1705, PARKED}
SMOKE_TRIANGLES, ORB_TRIANGLES = 80, 200
# (highest UV set 1 u of an orb's colour strip, colour, new geoset)
ORB_COLUMNS = ((0.845, 'yellow', 1702), (0.895, 'orange', PARKED), (0.955, 'pale', PARKED), (1.01, 'blue', 1703))
SMOKE_GEOSET = 1703
HEADER_COMBINERS = 0x130
FLAG_COMBINERS = 8
BATCH, SECTION, VERTEX = 24, 48, 48
MOD, OPAQUE, ADD, MOD2X = 1, 0, 3, 4
EYE_TEXTURE_TYPES = {8, 19}             # type 8: the skin row's extra texture (Skyborne); 19: retail's eye slot
TEXTURE_COMBOS, UV_COMBOS, TRANSFORM_COMBOS = 0x80, 0x88, 0x98


def arr(d, o):
    return struct.unpack_from('<II', d, o)


def table(d, offset, fmt='H'):
    n, o = arr(d, offset)
    return list(struct.unpack_from('<%d%s' % (n, fmt), d, o))


def align(d):
    while len(d) % 16:
        d.append(0)


def append_data(d, data):
    align(d)
    offset = len(d)
    d.extend(data)
    return offset


def pair_index(d, offset, a, b, fmt):
    """Index of a consecutive (a, b) in a lookup table, appending the pair (moving the table to the end) if missing."""
    values = table(d, offset, fmt)
    for i in range(len(values) - 1):
        if values[i] == a and values[i + 1] == b:
            return i
    struct.pack_into('<II', d, offset, len(values) + 2,
                     append_data(d, struct.pack('<%d%s' % (len(values) + 2, fmt), *(values + [a, b]))))
    return len(values)


def is_eye_texture(types, names, slot):
    return types[slot] in EYE_TEXTURE_TYPES or 'eye_color' in names[slot].lower()


def glow_kind(d, s, section_offset):
    """('smoke' | colour, new geoset) for a retail eye glow section, else None."""
    sid, _, vstart, vcount, _, icount = struct.unpack_from('<6H', s, section_offset)
    if sid not in GLOW_IDS:
        return None
    if icount // 3 not in (SMOKE_TRIANGLES, ORB_TRIANGLES):
        return None
    nl, ol = arr(s, 0x04)
    lookup = struct.unpack_from('<%dH' % nl, s, ol)
    nv, ov = arr(d, 0x3C)
    uvs = [struct.unpack_from('<4f', d, ov + VERTEX * lookup[vstart + k] + 32) for k in range(vcount)]
    top = max(uv[2] for uv in uvs)
    if icount // 3 == SMOKE_TRIANGLES:
        # layer 1 in the colour bar at the atlas' top left, layer 2 across the smoke on its right half
        if max(uv[0] for uv in uvs) < 0.2 and max(uv[1] for uv in uvs) < 0.12 and top > 0.9:
            return 'smoke', SMOKE_GEOSET
        return None
    if top < 0.79:
        return None
    for limit, colour, geoset in ORB_COLUMNS:
        if top <= limit:
            return colour, geoset
    return None


def enable_combiners(d):
    flags, = struct.unpack_from('<I', d, 0x10)
    if flags & FLAG_COMBINERS:
        return True
    name_n, name_o = arr(d, 0x08)
    loops_n, loops_o = arr(d, 0x14)
    if name_o != HEADER_COMBINERS or loops_o != name_o + ((name_n + 3) & ~3):
        return False
    name = bytes(d[name_o:name_o + name_n])
    loops = bytes(d[loops_o:loops_o + 4 * loops_n])
    struct.pack_into('<II', d, 0x08, name_n, append_data(d, name))
    struct.pack_into('<II', d, 0x14, loops_n, append_data(d, loops) if loops_n else 0)
    struct.pack_into('<II', d, HEADER_COMBINERS, 0, 0)
    struct.pack_into('<I', d, 0x10, flags | FLAG_COMBINERS)
    return True


def patch(model_path):
    d = bytearray(open(model_path, 'rb').read())
    if not enable_combiners(d):
        return 'skipped: the data after the header is not the name and global loops'

    nt, ot = arr(d, 0x50)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    names = []
    for i in range(nt):
        n, o = struct.unpack_from('<II', d, ot + 16 * i + 8)
        names.append(d[o:o + n].rstrip(b'\0').decode('latin1'))
    nm, om = arr(d, 0x70)
    blend = [struct.unpack_from('<HH', d, om + 4 * i)[1] for i in range(nm)]

    combiners = []
    def combiner(ops):
        for i in range(len(combiners) - len(ops) + 1):
            if combiners[i:i + len(ops)] == list(ops):
                return i
        combiners.extend(ops)
        return len(combiners) - len(ops)

    report = []
    for skin_path in sorted(glob.glob(model_path[:-3] + '0?.skin')):
        s = bytearray(open(skin_path, 'rb').read())
        ns, osub = arr(s, 0x1C)
        nb, ob = arr(s, 0x24)
        kinds = {i: glow_kind(d, s, osub + SECTION * i) for i in range(ns)}
        counts = {'eyes': 0, 'glows': 0, 'layered': 0, 'uv': 0, 'plain': 0}
        for b in range(nb):
            o = ob + BATCH * b
            section, = struct.unpack_from('<H', s, o + 4)
            material, = struct.unpack_from('<H', s, o + 10)
            count, tex, uv, _, transform = struct.unpack_from('<HHHHH', s, o + 14)
            tex_combos = table(d, TEXTURE_COMBOS)
            uv_combos = table(d, UV_COMBOS, 'h')
            geoset, = struct.unpack_from('<H', s, osub + SECTION * section)
            two_on_set1 = (tex + 1 < len(tex_combos) and uv + 1 < len(uv_combos)
                           and tex_combos[tex] == tex_combos[tex + 1] and uv_combos[uv] == 0 and uv_combos[uv + 1] == 1)
            kind = kinds[section]
            if (geoset == 0 or geoset // 100 == 33) and count in (1, 2) and two_on_set1 \
                    and is_eye_texture(types, names, tex_combos[tex]) and blend[material] in (0, 1):
                struct.pack_into('<H', s, o + 14, 2)
                ops = (MOD, ADD)
                counts['eyes'] += 1
            elif kind and count in (1, 2):
                if count == 1:
                    # the second layer conversion dropped: the same texture again, on UV set 1, with the same transform
                    t = tex_combos[tex]
                    tf = table(d, TRANSFORM_COMBOS, 'h')[transform]
                    struct.pack_into('<H', s, o + 14, 2)
                    struct.pack_into('<H', s, o + 16, pair_index(d, TEXTURE_COMBOS, t, t, 'H'))
                    struct.pack_into('<H', s, o + 18, pair_index(d, UV_COMBOS, 0, 1, 'h'))
                    struct.pack_into('<H', s, o + 22, pair_index(d, TRANSFORM_COMBOS, tf, tf, 'h'))
                    counts['layered'] += 1
                ops = (MOD, MOD2X) if kind[0] == 'smoke' else (MOD, MOD)
                counts['glows'] += 1
            else:
                ops = (MOD, OPAQUE)[:count]
                if count == 2 and uv + 1 < len(uv_combos) and (uv_combos[uv + 1] & 0xFFFF) > 2:   # -1 too (0xFFFF)
                    if uv_combos[uv] != 0:
                        return 'skipped: batch %d has a second layer on UV combo %d and a first not on UV set 0' % (
                            b, uv_combos[uv + 1])
                    struct.pack_into('<H', s, o + 18, pair_index(d, UV_COMBOS, 0, 1, 'h'))
                    counts['uv'] += 1
                counts['plain'] += 1
            struct.pack_into('<H', s, o + 2, combiner(ops))
        renumbered = {}
        for i, kind in kinds.items():
            if kind:
                struct.pack_into('<H', s, osub + SECTION * i, kind[1])
                renumbered[kind[0]] = renumbered.get(kind[0], 0) + 1
        open(skin_path, 'wb').write(s)
        report.append('%s: %d eye, %d glow (%d given their second layer), %d unchanged batches (%d moved off a UV combo '
                      '-1 layer); glows %s' % (skin_path.replace(chr(92), '/').split('/')[-1], counts['eyes'],
                                              counts['glows'], counts['layered'], counts['plain'], counts['uv'],
                                              renumbered or 'none'))

    if table(d, HEADER_COMBINERS) != combiners:
        struct.pack_into('<II', d, HEADER_COMBINERS, len(combiners),
                         append_data(d, struct.pack('<%dH' % len(combiners), *combiners)))
    open(model_path, 'wb').write(d)
    return '; '.join(report) + ', combiners %s' % combiners


def main():
    for path in sys.argv[1:]:
        print(path.replace(chr(92), '/').split('/')[-1], patch(path))


if __name__ == '__main__':
    main()
