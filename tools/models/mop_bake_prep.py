#!/usr/bin/env python3
"""Convert F-134's Pandaren NPC bakes from MoP Classic's HD layout to the layout F-129's Pandaren models use.

  python -I mop_bake_prep.py [--whe PATH] [--common PATH] [--jobs N]

The bakes (Textures\\BakedNpcTextures\\CreatureDisplayExtra-<id>.blp) come from MoP Classic, whose Pandaren use the
HD layout (CharComponentTextureLayouts 2, 2048 x 1024; the bakes are 1024 x 512): the left half is the stock layout,
the right half the whole HD head. F-129's models are 5.4.8's, with stock layout UVs (face upper / lower in the
bottom-left of the left half), so the bakes put head fur on the chest and armour bits on the face.

Each 1024 x 512 Pandaren bake becomes 512 x 512: the left half, with the face rectangles taken from F-129's own
skin and face textures for the row's skin colour and face (the same textures players are composited from).
Converted bakes are 512 x 512 and are skipped, so it can be rerun; restore with git in WHE-common to start over.
--modpak picks the modpak (F-134 by default, F-133 for Pandaria's NPCs)."""
import argparse, glob, multiprocessing, os, re, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maghar_modern_prep import crop_scale, read_dxt, write_blp  # noqa: E402

SLASH = chr(92)
SECTIONS = 'modpaks/F-129_mod-pandaren-neutral/dbc/[BASE,F-129]_charsections.sql'
BAKES = 'textures/bakednpctextures'      # in WHE-common/patch-MoP.MPQ (F-133 and F-134); the rows in WHE's <modpak>/dbc
FACE_UPPER, FACE_LOWER = (0, 320, 256, 64), (0, 384, 256, 128)    # stock rectangles at 512 x 512


def read_pal(path):
    """(w, h, rgba) of a palettized BLP2's top level."""
    b = open(path, 'rb').read()
    assert b[:4] == b'BLP2' and b[8] == 1, path
    depth = b[9]
    w, h = struct.unpack_from('<II', b, 12)
    off = struct.unpack_from('<I', b, 20)[0]
    pal = [struct.unpack_from('<4B', b, 148 + 4 * i) for i in range(256)]
    idx, alpha = b[off:off + w * h], b[off + w * h:]
    out = bytearray(w * h * 4)
    for i in range(w * h):
        bl, g, r, _ = pal[idx[i]]
        if depth == 8:
            a = alpha[i]
        elif depth == 4:
            a = ((alpha[i >> 1] >> (4 * (i & 1))) & 15) * 17
        elif depth == 1:
            a = 255 if alpha[i >> 3] >> (i & 7) & 1 else 0
        else:
            a = 255
        out[i * 4:i * 4 + 4] = bytes((r, g, bl, a))
    return w, h, out


def paste(dst, dw, rect, src, over):
    """Copy src (rect-sized RGBA) into dst at rect; with over, alpha-blend instead."""
    x0, y0, rw, rh = rect
    for y in range(rh):
        for x in range(rw):
            s, d = (y * rw + x) * 4, ((y0 + y) * dw + x0 + x) * 4
            if over:
                a = src[s + 3]
                for c in range(3):
                    dst[d + c] = (src[s + c] * a + dst[d + c] * (255 - a)) // 255
            else:
                dst[d:d + 4] = src[s:s + 4]
                dst[d + 3] = 255


def scaled(path, rect):
    w, h, rgba = read_pal(path)
    return crop_scale(rgba, w, 0, 0, w, h, rect[2], rect[3])


def convert(job):
    bake, skin, lower, upper = job
    img = read_dxt(bake)
    if img is None or img[:2] != (1024, 512):
        return 0
    w, _, src = img
    out = crop_scale(src, w, 0, 0, 512, 512, 512, 512)
    # the skin's own face area under the face layers, as the compositor does for players
    sw, sh, srgba = read_pal(skin)
    for rect in (FACE_UPPER, FACE_LOWER):
        x, y, rw, rh = (v * sw // 512 for v in rect)
        paste(out, 512, rect, crop_scale(srgba, sw, x, y, rw, rh, rect[2], rect[3]), False)
    paste(out, 512, FACE_LOWER, scaled(lower, FACE_LOWER), True)
    paste(out, 512, FACE_UPPER, scaled(upper, FACE_UPPER), True)
    write_blp(bake, 512, 512, out)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--whe', default=os.path.normpath(os.path.join(here, '..', '..')))
    p.add_argument('--common', default=os.path.normpath(os.path.join(here, '..', '..', '..', 'WHE-common')))
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--modpak', default='F-134_mop-wandering-isle', help='also F-133_mop-pandaria')
    a = p.parse_args()

    sections = {}   # (gender, section, variation, colour) -> (texture_1, texture_2)
    row = re.compile(r"@NeutralPandaren, @(Male|Female),\s*@(Skin|Face),\s*'([^']*)', '([^']*)', '[^']*', \d+, (\d+), (\d+)\)")
    for m in row.finditer(open(os.path.join(a.whe, SECTIONS), encoding='utf-8').read()):
        sections[(int(m.group(1) == 'Female'), m.group(2), int(m.group(5)), int(m.group(6)))] = (m.group(3), m.group(4))

    def local(game_path):
        rel = game_path.replace(SLASH * 2, '/').replace(SLASH, '/')
        folder, name = os.path.split(os.path.join(a.common, 'patch-A.MPQ', rel))
        names = {n.lower(): n for n in os.listdir(folder)}
        return os.path.join(folder, names[name.lower()])

    jobs, seen = [], set()
    extra = re.compile(r"`race` = @NeutralPandaren,\s*`gender` = (\d+),\s*`skin_color` = (\d+),\s*`face_type` = (\d+),"
                       r".*?`texture` = '([^']*)'", re.S)
    text = ''.join(open(p, encoding='utf-8').read() for p in
                   glob.glob(os.path.join(a.whe, 'modpaks', a.modpak, 'dbc', '*creaturedisplayinfoextra.sql')))
    for m in extra.finditer(text):
        gender, skin, face, tex = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4).lower()
        if not tex or tex in seen:
            continue
        seen.add(tex)
        faces = sections.get((gender, 'Face', face, skin)) or sections.get((gender, 'Face', 0, skin))
        skins = sections.get((gender, 'Skin', 0, skin))
        if not faces or not skins:
            print('no F-129 face or skin for', tex, (gender, skin, face))
            continue
        bake = os.path.join(a.common, 'patch-MoP.MPQ', BAKES, tex)
        if not os.path.exists(bake):
            continue
        jobs.append((bake, local(skins[0]), local(faces[0]), local(faces[1])))
    with multiprocessing.Pool(a.jobs) as pool:
        n = sum(pool.map(convert, jobs))
    print('converted %d of %d Pandaren bakes' % (n, len(jobs)))


if __name__ == '__main__':
    main()
