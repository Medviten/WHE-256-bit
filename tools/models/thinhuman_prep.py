#!/usr/bin/env python3
"""Convert F-041's Thin Human (Forgotten) textures to what the model and the character compositor expect.

The model is already in stock layout, with the head a separate batch on texture type 8. The skins are retail's 1024x512
atlas though: the left half is the stock atlas squeezed to half width, the right half the whole head. The compositor pastes
the stock section rectangles out of the whole texture, so the head sheet (eyes, teeth, face) lands on the torso and legs.

Textures (rewritten as 8-bit palette + 8-bit alpha with full mip chains):
- skin: the left half, with the unpainted background bled from the nearest paint so mips don't fringe white
- underwear: same layout as stock, palettized only

The whole-head files stay as they are: F-041's skin rows bind them to type 8 through texture_2 (empty before, which left
the head white). The model isn't touched.

usage: thinhuman_prep.py [--common PATH] [--jobs N]
Already converted files are skipped, so it can be rerun; restore with git in WHE-common to start over."""
import argparse, glob, multiprocessing, os, sys

from maghar_modern_prep import crop_scale, read_dxt, write_blp

BACKGROUND = 250        # the atlas leaves everything outside its islands white; no skin has paint this bright


def bleed(rgba, w, h):
    """Fills white background from its painted neighbours, one ring at a time."""
    empty = [min(rgba[i * 4:i * 4 + 3]) >= BACKGROUND for i in range(w * h)]
    ring = [i for i in range(w * h) if empty[i]]
    while ring:
        fill = []
        for i in ring:
            x, y = i % w, i // w
            near = [n for n, ok in ((i - 1, x > 0), (i + 1, x < w - 1), (i - w, y > 0), (i + w, y < h - 1)) if ok and not empty[n]]
            if near:
                fill.append((i, [sum(rgba[n * 4 + c] for n in near) // len(near) for c in range(3)]))
        if not fill:
            break
        for i, col in fill:
            rgba[i * 4:i * 4 + 3] = bytes(col)
            empty[i] = False
        ring = [i for i in ring if empty[i]]
    return rgba


def convert_skin(path):
    img = read_dxt(path)
    if img is None:
        return 0
    w, h, src = img
    assert (w, h) == (1024, 512), path
    write_blp(path, 512, 512, bleed(crop_scale(src, w, 0, 0, 512, 512, 512, 512), 512, 512))
    return 1


def convert_plain(path):
    img = read_dxt(path)
    if img is None:
        return 0
    write_blp(path, *img)
    return 1


def convert(job):
    kind, path = job
    return {'skin': convert_skin, 'plain': convert_plain}[kind](path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common')
    ap.add_argument('--jobs', type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    folder = os.path.join(a.common, 'patch-A.MPQ', 'custom', 'thinhuman', 'character', 'thinhuman', 'male')
    jobs = [('skin', f) for f in glob.glob(os.path.join(folder, 'thinhumanmaleskin*.blp'))]
    jobs += [('plain', f) for pat in ('nakedtorsoskin', 'nakedpelvisskin') for f in glob.glob(os.path.join(folder, 'thinhumanmale%s*.blp' % pat))]
    with multiprocessing.Pool(a.jobs) as pool:
        done = sum(pool.imap_unordered(convert, jobs))
    print('textures: %d jobs, %d converted' % (len(jobs), done))


if __name__ == '__main__':
    sys.exit(main())
