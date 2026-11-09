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
  texture with UV set 1), the death knight smoke (retail's 1701, 80 triangles) Mod_Mod2x and the glow orbs (1702-1705)
  Mod_Mod;
- renumbers the glows to the stock meaning of group 17 (1701 none, 1702 the race's glow, 1703 death knights): retail's
  1701 smoke becomes 1703 and its orbs are parked at PARKED, which the client hides. Without this the client's default
  1701 shows the death knight smoke on everyone. Models already renumbered (the Mag'har prep) have no 1701 left.

usage: m2_retail_combiners.py MODEL.m2 [...]
Patches the model and all its .skin files in place; an already patched model is left alone."""
import glob, struct, sys

PARKED = 1999
GLOW_GEOSETS = {1701: 1703, 1702: PARKED, 1703: PARKED, 1704: PARKED, 1705: PARKED}
SMOKE_TRIANGLES = 80
HEADER_COMBINERS = 0x130
FLAG_COMBINERS = 8
BATCH = 24
MOD, OPAQUE, ADD, MOD2X = 1, 0, 3, 4
EYE_TEXTURE_TYPES = {8, 19}             # type 8: the skin row's extra texture (Skyborne); 19: retail's eye slot


def arr(d, o):
    return struct.unpack_from('<II', d, o)


def is_eye_texture(types, names, slot):
    return types[slot] in EYE_TEXTURE_TYPES or 'eye_color' in names[slot].lower()


def patch(model_path):
    d = bytearray(open(model_path, 'rb').read())
    flags, = struct.unpack_from('<I', d, 0x10)
    if flags & FLAG_COMBINERS:
        return 'already has combiners'
    name_n, name_o = arr(d, 0x08)
    loops_n, loops_o = arr(d, 0x14)
    if name_o != HEADER_COMBINERS or loops_o != name_o + ((name_n + 3) & ~3):
        return 'skipped: the data after the header is not the name and global loops'
    # Move the name and global loops to the end, aligned.
    def append(data):
        while len(d) % 16:
            d.append(0)
        offset = len(d)
        d.extend(data)
        return offset
    name = bytes(d[name_o:name_o + name_n])
    loops = bytes(d[loops_o:loops_o + 4 * loops_n])
    struct.pack_into('<II', d, 0x08, name_n, append(name))
    struct.pack_into('<II', d, 0x14, loops_n, append(loops) if loops_n else 0)

    nt, ot = arr(d, 0x50)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    names = []
    for i in range(nt):
        n, o = struct.unpack_from('<II', d, ot + 16 * i + 8)
        names.append(d[o:o + n].rstrip(b'\0').decode('latin1'))
    nm, om = arr(d, 0x70)
    blend = [struct.unpack_from('<HH', d, om + 4 * i)[1] for i in range(nm)]
    ntc, otc = arr(d, 0x80)
    tex_combos = struct.unpack_from('<%dH' % ntc, d, otc)
    nuv, ouv = arr(d, 0x88)
    uv_combos = struct.unpack_from('<%dh' % nuv, d, ouv)
    uv_set1 = uv_combos.index(1) if 1 in uv_combos else None

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
        ns, osub = struct.unpack_from('<II', s, 0x1C)
        nb, ob = struct.unpack_from('<II', s, 0x24)
        counts = {'eyes': 0, 'glows': 0, 'uv': 0, 'plain': 0, 'renumbered': 0}
        ids = [struct.unpack_from('<H', s, osub + 48 * i)[0] for i in range(ns)]
        for b in range(nb):
            o = ob + BATCH * b
            section, = struct.unpack_from('<H', s, o + 4)
            material, = struct.unpack_from('<H', s, o + 10)
            count, tex, uv = struct.unpack_from('<HHH', s, o + 14)
            geoset = ids[section]
            triangles = struct.unpack_from('<H', s, osub + 48 * section + 10)[0] // 3
            two_on_set1 = (tex + 1 < ntc and uv + 1 < nuv and tex_combos[tex] == tex_combos[tex + 1]
                           and uv_combos[uv] == 0 and uv_combos[uv + 1] == 1)
            if (geoset == 0 or geoset // 100 == 33) and count in (1, 2) and two_on_set1 \
                    and is_eye_texture(types, names, tex_combos[tex]) and blend[material] in (0, 1):
                struct.pack_into('<H', s, o + 14, 2)
                ops = (MOD, ADD)
                counts['eyes'] += 1
            elif geoset // 100 == 17 and count == 2 and two_on_set1:
                ops = (MOD, MOD2X) if triangles == SMOKE_TRIANGLES else (MOD, MOD)
                counts['glows'] += 1
            else:
                ops = (MOD, OPAQUE)[:count]
                if count == 2 and uv + 1 < nuv and (uv_combos[uv + 1] & 0xFFFF) > 2:   # -1 too: the client reads it as 0xFFFF
                    if uv_set1 is None or uv_combos[uv] != 0:
                        return "skipped: batch %d has a second layer on UV combo %d and no UV set 1 entry to keep it" % (
                            b, uv_combos[uv + 1])
                    # [0, 1] pair: the first entry stays UV set 0
                    pair = next((i for i in range(nuv - 1) if uv_combos[i] == 0 and uv_combos[i + 1] == 1), None)
                    if pair is None:
                        return 'skipped: no UV combo pair (0, 1) for batch %d' % b
                    struct.pack_into('<H', s, o + 18, pair)
                    counts['uv'] += 1
                counts['plain'] += 1
            struct.pack_into('<H', s, o + 2, combiner(ops))
        if 1701 in ids:
            for i, sid in enumerate(ids):
                if sid in GLOW_GEOSETS:
                    struct.pack_into('<H', s, osub + 48 * i, GLOW_GEOSETS[sid])
                    counts['renumbered'] += 1
        open(skin_path, 'wb').write(s)
        report.append('%s: %d eye, %d glow, %d unchanged batches (%d moved off a UV combo -1 layer), %d glow geosets '
                      'renumbered' % (skin_path.replace(chr(92), '/').split('/')[-1], counts['eyes'], counts['glows'],
                                      counts['plain'], counts['uv'], counts['renumbered']))

    struct.pack_into('<II', d, HEADER_COMBINERS, len(combiners), append(struct.pack('<%dH' % len(combiners), *combiners)))
    struct.pack_into('<I', d, 0x10, flags | FLAG_COMBINERS)
    open(model_path, 'wb').write(d)
    return '; '.join(report) + ', combiners %s' % combiners


def main():
    for path in sys.argv[1:]:
        print(path.replace('\\', '/').split('/')[-1], patch(path))


if __name__ == '__main__':
    main()
