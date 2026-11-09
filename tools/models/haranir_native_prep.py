#!/usr/bin/env python3
"""Bake a native Haranir (F-098/F-099) for clients that don't map the race in retailRaces, as RetroPorter's set did for Mechagnome.

Kalibro's package has the models (custom/haranir/native) but no textures: his client composes them at run time. This script
composes Retail's layers with RetailComposeProbe (from a WOWDECOMP_RETAIL_ASSETS build) and bakes the results.

Textures (custom/haranir/native/<sex>, 8-bit palette + 8-bit alpha with full mip chains, as the compositor needs):
- the Retail body sheet is 2048x1024: the left half is the body, the right half the whole head. The models' body UVs are
  Kalibro's stock layout: the left half stretched to the whole texture, with the head squeezed into the face rectangles
- body<skin>: the body without its cloth (Loincloth/Underclothes Color "Transmog" draws none)
- pelvis<skin>, torso<skin> (female): the same body with its cloth, cropped to the underwear rectangles
- facelower<skin>_<face>, faceupper<skin>_<face>: the head. Faces after Retail's own use the Growth face paint
- hair<colour>: Retail's hair sheet, no highlights
- eyes, glow, spines, cloth, jewelry: one fixed look for the slots nothing here can fill (see fix_model)

Models:
- hair styles 4002-4018 become geosets 2-18 of group 0, which CharHairGeosets selects
- female eyebrows 34xx become group 1, which CharacterFacialHairStyles selects (males use groups 1-3 for beards)
- the client only manages geosets up to 2000, so everything above is always drawn. Variants nothing can select are parked in
  group 19, leaving Retail's defaults (as Earthen does)
- slots of types the client doesn't fill point at the fixed-look files

usage: haranir_native_prep.py [--common PATH] [--package PATH] [--probe EXE] [--ini PATH] [--work DIR] [--jobs N]
                              [--sex male|female] [--skins N] [--models-only]
Finished textures are skipped, so it can be rerun. Scratch files go to --work and are deleted as they are converted."""
import argparse, multiprocessing, os, re, shutil, struct, subprocess, sys, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'races'))
from maghar_modern_prep import crop_scale, write_blp  # noqa: E402
from m2_retail_combiners import patch as retail_combiners  # noqa: E402

SLASH = chr(92)
RACE = 86           # Alliance and Horde Haranir share a ChrModel, so one bake serves both
PARKED = 1999
FACE_PAINT = 'Growth'
SHEET_W, SHEET_H = 2048, 1024
# Retail defaults everywhere else: first choice of every option. These are the ones that aren't plain
FIXED = {'Face Paint': 'None', 'Body Paint': 'None', 'Hair Highlight Color': 'None', 'Face Fur Pattern': 'None',
         'Body Fur Pattern': 'None', 'Feet': 'Normal'}
CLOTH = {'male': 'Loincloth Color', 'female': 'Underclothes Color'}
# Skip the choices retail doesn't offer players
SKIP = ('NPC Skin', 'Hagar', 'Transmog')
# Retail's default variant of each group above 2000; the rest of the group is parked. Empty groups are all parked
KEEP = {20: {2001}, 22: {2201}, 32: {3202}, 34: {3401}, 35: set(), 36: set(), 42: {4201}, 43: set(), 44: set(), 45: set(),
        46: set(), 47: {4701}, 51: {5101}}
# texture type -> fixed-look file. Types 8 and 12 hold the same Retail sheet (spine colours)
STATIC = {5: 'eyes', 8: 'spines', 9: 'cloth', 10: 'glow', 12: 'spines', 13: 'jewelry'}
# the Retail texture type each file is composed from
STATIC_SOURCE = {'eyes': 19, 'spines': 8, 'cloth': 9, 'glow': 10, 'jewelry': 20}


def read_png(path):
    """The probe's PNGs: 8-bit RGBA, filter 0 on every row."""
    d = open(path, 'rb').read()
    at, idat = 8, []
    while at < len(d):
        size = struct.unpack_from('>I', d, at)[0]
        tag = d[at + 4:at + 8]
        if tag == b'IHDR':
            w, h = struct.unpack_from('>II', d, at + 8)
        elif tag == b'IDAT':
            idat.append(d[at + 8:at + 8 + size])
        at += 12 + size
    raw = zlib.decompress(b''.join(idat))
    out = bytearray(w * h * 4)
    for y in range(h):
        out[y * w * 4:(y + 1) * w * 4] = raw[y * (w * 4 + 1) + 1:(y + 1) * (w * 4 + 1)]
    return w, h, out


def bleed(rgba, w, h):
    """Fills transparent background from its painted neighbours, one ring at a time, so the mips don't fringe."""
    empty = [rgba[i * 4 + 3] < 128 for i in range(w * h)]
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


def opaque(rgba):
    rgba[3::4] = b'\xff' * (len(rgba) // 4)
    return rgba


def crop(src, w, x, y, cw, ch):
    out = bytearray(cw * ch * 4)
    for row in range(ch):
        out[row * cw * 4:(row + 1) * cw * 4] = src[((y + row) * w + x) * 4:((y + row) * w + x + cw) * 4]
    return out


def body_sheet(src):
    """The stock-layout texture Kalibro's UVs expect: the left half of the sheet, with the head in the face rectangles."""
    out = bleed(crop_scale(src, SHEET_W, 0, 0, SHEET_W // 2, SHEET_H, 512, 512), 512, 512)
    head = bleed(crop_scale(src, SHEET_W, SHEET_W // 2, 0, SHEET_W // 2, SHEET_H, 256, 192), 256, 192)
    for row in range(192):
        out[(320 + row) * 512 * 4:((320 + row) * 512 + 256) * 4] = head[row * 256 * 4:(row + 1) * 256 * 4]
    return opaque(out)


def convert(job):
    kind, folder, prefix, tag = job
    if kind == 'static':
        for name, source in STATIC_SOURCE.items():
            path = '%s-type%d.png' % (prefix, source)
            w, h, src = read_png(path)
            write_blp(os.path.join(folder, name + '.blp'), w, h, src)
        return kind
    if kind == 'hair':
        w, h, src = read_png(prefix + '-type6.png')
        write_blp(os.path.join(folder, 'hair%s.blp' % tag), w, h, bleed(src, w, h))
        return kind
    w, h, src = read_png(prefix + '-type1.png')
    assert (w, h) == (SHEET_W, SHEET_H), (w, h)
    sheet = body_sheet(src)
    if kind == 'body':
        write_blp(os.path.join(folder, 'body%s.blp' % tag), 512, 512, sheet)
    elif kind == 'under':
        write_blp(os.path.join(folder, 'pelvis%s.blp' % tag), 256, 128, crop(sheet, 512, 256, 192, 256, 128))
        if os.path.basename(folder) == 'female':
            write_blp(os.path.join(folder, 'torso%s.blp' % tag), 256, 128, crop(sheet, 512, 256, 0, 256, 128))
    elif kind == 'face':
        write_blp(os.path.join(folder, 'faceupper%s.blp' % tag), 256, 64, crop(sheet, 512, 0, 320, 256, 64))
        write_blp(os.path.join(folder, 'facelower%s.blp' % tag), 256, 128, crop(sheet, 512, 0, 384, 256, 128))
    return kind


def finished(job):
    kind, folder, _, tag = job
    names = {'static': [n + '.blp' for n in STATIC_SOURCE], 'hair': ['hair%s.blp' % tag], 'body': ['body%s.blp' % tag],
             'under': ['pelvis%s.blp' % tag] + (['torso%s.blp' % tag] if os.path.basename(folder) == 'female' else []),
             'face': ['faceupper%s.blp' % tag, 'facelower%s.blp' % tag]}[kind]
    return all(os.path.exists(os.path.join(folder, n)) for n in names)


class Options:
    """Retail's options for one sex, by name."""

    def __init__(self, probe, ini, sex):
        self.probe, self.ini, self.sex = probe, ini, sex
        out = self.run(str(RACE), str(0 if sex == 'male' else 1))
        self.ids = {name: int(oid) for oid, name in re.findall(r'option (\d+) "([^"]*)"', out)}
        self.choices = {}
        for name, oid in self.ids.items():
            rows = re.findall(r'^(\d+) (\d+) (.*?)\r?$', self.run('choices', str(oid)), re.M)
            self.choices[name] = [(int(i), c.strip()) for i, _, c in rows]

    def run(self, *args):
        return subprocess.run([self.probe, self.ini, *args], cwd=os.path.dirname(self.ini), capture_output=True, text=True, check=True).stdout

    def pick(self, option, choice):
        return '%d:%d' % (self.ids[option], next(i for i, c in self.choices[option] if c == choice))

    def index(self, option, i):
        return '%d:%d' % (self.ids[option], i)

    def offered(self, option):
        return [i for i, c in self.choices[option] if c not in SKIP]

    def base(self):
        return [self.pick(o, c) for o, c in FIXED.items() if o in self.ids]


def bake_jobs(opts, sex, folder, work, skins_limit):
    """(job, composer arguments) for everything of one sex."""
    jobs = []
    gender = '0' if sex == 'male' else '1'
    base = opts.base()
    skins = opts.offered('Skin Color')[:skins_limit]
    faces = opts.offered('Face')
    paint = opts.pick('Face Paint', FACE_PAINT)
    bare = opts.pick(CLOTH[sex], 'Transmog')

    def add(kind, tag, picks):
        prefix = os.path.join(work, '%s-%s%s' % (sex, kind, tag))
        jobs.append(((kind, folder, prefix, tag), [str(RACE), gender, prefix] + base + picks))

    add('static', '', [])
    for c, colour in enumerate(opts.offered('Hair Color')):
        add('hair', str(c), [opts.index('Hair Color', colour)])
    for s, skin in enumerate(skins):
        pick = opts.index('Skin Color', skin)
        add('body', str(s), [pick, bare])
        add('under', str(s), [pick])
        for f, face in enumerate(faces):
            add('face', '%d_%d' % (s, f), [pick, opts.index('Face', face)])
            add('face', '%d_%d' % (s, f + len(faces)), [pick, opts.index('Face', face), paint])
    return jobs


def run_jobs(jobs, opts, work, pool):
    todo = [j for j in jobs if not finished(j[0])]
    print(len(jobs), 'textures sets,', len(todo), 'to do', flush=True)
    for at in range(0, len(todo), 32):
        chunk = todo[at:at + 32]
        cases = os.path.join(work, 'cases.txt')
        with open(cases, 'w') as f:
            f.write('\n'.join(' '.join(args) for _, args in chunk) + '\n')
        done = subprocess.run([opts.probe, opts.ini, 'batch', cases], cwd=os.path.dirname(opts.ini), capture_output=True, text=True)
        if done.returncode:
            sys.exit('compose failed:\n' + done.stdout[-1500:] + done.stderr[-1500:])
        list(pool.imap_unordered(convert, [j for j, _ in chunk]))
        for job, _ in chunk:
            for type_ in (1, 6, 8, 9, 10, 19, 20, 25):
                path = '%s-type%d.png' % (job[2], type_)
                if os.path.exists(path):
                    os.remove(path)
        print(at + len(chunk), '/', len(todo), flush=True)


def fix_skin(data, sex):
    s = bytearray(data)
    (_, _, _, _, _, _, ns, os_, _, _, _) = struct.unpack_from('<11I', s, 4)
    changed = 0
    for i in range(ns):
        at = os_ + 48 * i
        sid = struct.unpack_from('<H', s, at)[0]
        group = sid // 100
        if group == 40:
            new = sid - 4000
        elif group == 34 and sex == 'female':
            new = 100 + sid % 100
        elif group in KEEP:
            new = sid if sid in KEEP[group] else PARKED
        elif sid > 2000:
            new = PARKED
        else:
            new = sid
        if new != sid:
            struct.pack_into('<H', s, at, new)
            changed += 1
    return s, changed


def fix_model(common, package, sex):
    rel = os.path.join('custom', 'haranir', 'native', sex, 'harronir' + sex)
    src, dst = os.path.join(package, rel), os.path.join(common, 'patch-A.MPQ', rel)
    d = bytearray(open(src + '.m2', 'rb').read())
    s, changed = fix_skin(open(src + '00.skin', 'rb').read(), sex)
    nt, ot = struct.unpack_from('<II', d, 0x50)
    names = {}
    slots = 0
    for slot in range(nt):
        at = ot + 16 * slot
        type_, flags = struct.unpack_from('<II', d, at)
        if type_ not in STATIC:
            continue
        name = SLASH.join(('custom', 'haranir', 'native', sex, STATIC[type_] + '.blp')).encode('latin1') + b'\0'
        if name not in names:
            names[name] = len(d)
            d += name
        struct.pack_into('<4I', d, at, 0, flags, len(name), names[name])
        slots += 1
    open(dst + '.m2', 'wb').write(d)
    open(dst + '00.skin', 'wb').write(s)
    return 'sections changed %d, fixed slots %d' % (changed, slots)


def copy_assets(common, package, sex):
    """The neutral texture and the hard materials the models name, with complete mip chains."""
    from kalibro_races import pad_mips
    for rel, match in ((os.path.join('custom', 'haranir', 'native', sex), 'neutral.blp'),
                       (os.path.join('custom', 'haranir', 'character', 'harronir'), '')):
        src, dst = os.path.join(package, rel), os.path.join(common, 'patch-A.MPQ', rel)
        os.makedirs(dst, exist_ok=True)
        for name in os.listdir(src):
            if name.endswith('.blp') and (not match or name == match):
                shutil.copy2(os.path.join(src, name), os.path.join(dst, name))
                pad_mips(os.path.join(dst, name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--common', default='D:/GitHub/WHE-common')
    ap.add_argument('--package', default='D:/Downloads/Downloads/Races/Kalibros_Races_20261012')
    ap.add_argument('--probe', default='D:/GitHub/wowdecomp-256-bit/build/retail/bin/Release/RetailComposeProbe.exe')
    ap.add_argument('--options-probe', default='D:/GitHub/wowdecomp-256-bit/build/retail/bin/Release/RetailRaceProbe.exe')
    ap.add_argument('--ini', default='D:/wow-scratch/haranir-probe/RetailCasc.ini')
    ap.add_argument('--work', default='D:/wow-scratch/haranir-native')
    ap.add_argument('--jobs', type=int, default=max(1, multiprocessing.cpu_count() - 1))
    ap.add_argument('--sex', choices=('male', 'female'))
    ap.add_argument('--skins', type=int, default=99, help='only the first N skin colours, for testing')
    ap.add_argument('--models-only', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    with multiprocessing.Pool(a.jobs) as pool:
        for sex in ('male', 'female'):
            if a.sex and a.sex != sex:
                continue
            folder = os.path.join(a.common, 'patch-A.MPQ', 'custom', 'haranir', 'native', sex)
            os.makedirs(folder, exist_ok=True)
            copy_assets(a.common, a.package, sex)
            print(sex, fix_model(a.common, a.package, sex), flush=True)
            # retail's 1701 death knight smoke would show on everyone (the client's default eye glow geoset)
            print(sex, retail_combiners(os.path.join(folder, 'harronir%s.m2' % sex)), flush=True)
            if a.models_only:
                continue
            opts = Options(a.options_probe, a.ini, sex)
            opts.probe = a.probe
            run_jobs(bake_jobs(opts, sex, folder, a.work, a.skins), opts, a.work, pool)


if __name__ == '__main__':
    sys.exit(main())
