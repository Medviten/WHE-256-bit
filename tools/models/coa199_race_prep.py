"""Copy the models and textures of the CoA 1.9.9 races (tools/races/coa199_races.py) into a client folder (WHE-common's
patch-A.MPQ), as WHE player models.

Which model a race uses comes from the release's own ChrRaces -> CreatureDisplayInfo -> CreatureModelData rows.
- catalog races are made player models as coa_race_prep.py does it (texture type 11 -> 1 and 12 -> 8, the other
  options fixed at their first choice, unkept geosets above 2000 moved to 1999), with coa199_races.Look199
- classic races are character models already: the model, its .skin and .anim files, the textures it names and the
  textures of the release's CharSections rows for the race are copied as they are

Files the stock client has (its MPQs) are not copied, so a race that reuses a stock model or texture (Undead Gnome)
does not replace it. Files the output folder already has with other contents are kept and reported (WHE-common's
Nightborne model, which Elune's Chosen shares). Models of catalog races are always copied again and patched, so
reruns are safe.

The release ships the player models but expects CoA's own client for much of what they use (the v12 races'
textures, Orc2's and Drakkari Troll's .skin and .anim files): --extra takes those from a CoA-based client's Data
folder (Kalibro's Esteria client has them).

usage: python -I coa199_race_prep.py <release client Work folder> <release client folder (catalogs)>
           <release server/dbc> <client Data folder (stock MPQs)> <output folder> [race key ...]
           [--extra <CoA-based client Data folder>]"""
import copy
import glob
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'races'))
sys.path.insert(0, os.path.join(HERE, '..', 'checks'))
sys.path.insert(0, HERE)
import coa199_races   # noqa: E402
import coa_race_prep   # noqa: E402
import m2_anim_split   # noqa: E402
import mpq_unpack   # noqa: E402
import new_race_modpaks as nrm   # noqa: E402
from check_f013_assets import Archive, hash_string   # noqa: E402

B = '\\'


def index(root):
    """Upper-case client path -> (client path as packaged, real path)."""
    out = {}
    for dirpath, _, names in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        for n in names:
            client = n if rel == '.' else rel.replace(os.sep, B) + B + n
            out[client.upper()] = (client, os.path.join(dirpath, n))
    return out


def m2_path(path):
    return path[:-4] + '.m2' if path.lower().endswith(('.mdx', '.mdl')) else path


def race_models(dbc, race):
    """(male model, female model) client paths of a coa199_races race (CoA's, or one for both: ONE_BODY)."""
    rows, _, f = nrm.load_dbc(os.path.join(dbc, 'ChrRaces.dbc'))
    displays = next(struct.unpack_from('<6I', r)[4:6] for r in rows if struct.unpack_from('<I', r)[0] == race.coa_id)
    rows, _, _ = nrm.load_dbc(os.path.join(dbc, 'CreatureDisplayInfo.dbc'))
    model_of = {struct.unpack_from('<I', r)[0]: struct.unpack_from('<I', r, 4)[0] for r in rows}
    rows, strings, _ = nrm.load_dbc(os.path.join(dbc, 'CreatureModelData.dbc'))
    path_of = {struct.unpack_from('<I', r)[0]: nrm.string(strings, struct.unpack_from('<I', r, 8)[0]) for r in rows}
    return coa199_races.models(*[m2_path(path_of[model_of[d]]) for d in displays], race)


def section_textures(dbc, coa_id):
    """Every texture of the release's CharSections rows for a CoA race (3.3.5 layout)."""
    rows, strings, _ = nrm.load_dbc(os.path.join(dbc, 'CharSections.dbc'))
    out = []
    for r in rows:
        v = struct.unpack_from('<10I', r)
        if v[1] == coa_id:
            out += [nrm.string(strings, o).strip() for o in v[4:7]]
    return [t for t in out if t]


STOCK_ARCHIVES = {'common.mpq', 'common-2.mpq', 'expansion.mpq', 'lichking.mpq', 'patch.mpq', 'patch-2.mpq', 'patch-3.mpq',
                  'base-enus.mpq', 'backup-enus.mpq', 'locale-enus.mpq', 'speech-enus.mpq', 'expansion-locale-enus.mpq',
                  'expansion-speech-enus.mpq', 'lichking-locale-enus.mpq', 'lichking-speech-enus.mpq',
                  'patch-enus.mpq', 'patch-enus-2.mpq', 'patch-enus-3.mpq'}


def mpqs(folder):
    """The MPQs of a client Data folder (and its locale folder), in the client's load order."""
    return [p for p in sorted(glob.glob(os.path.join(folder, '*.[mM][pP][qQ]')) +
                              glob.glob(os.path.join(folder, '*', '*.[mM][pP][qQ]')), key=str.lower) if os.path.isfile(p)]


class Copier:
    def __init__(self, work, data, out, extra=None):
        self.work, self.out = index(work), out
        # only the stock archive names: a client's extra patch MPQs (patch-4, patch-5...) are not something every
        # client has
        self.stock = [Archive(p) for p in mpqs(data) if os.path.basename(p).lower() in STOCK_ARCHIVES]
        # --extra: a CoA-based client's Data folder, for what the release expects CoA's own client to have (the v12
        # races' textures, Orc2's and Drakkari Troll's .skin/.anim files); the last archive with a file wins
        self.extra = []
        for p in reversed(mpqs(extra)) if extra else []:
            try:
                self.extra.append(mpq_unpack.Archive(p))
            except (struct.error, ValueError) as e:   # a protected or damaged archive: report and go on
                print('--extra: %s skipped (%s)' % (os.path.basename(p), e))
        self.missing, self.kept, self.copied, self.from_extra = [], [], 0, 0

    def is_stock(self, path):
        return any(a.has(path) for a in self.stock)

    def read(self, path):
        """(client path, contents) from the release, else from the extra client; None when neither has it."""
        hit = self.work.get(path.upper())
        if hit:
            return hit[0], open(hit[1], 'rb').read()
        for a in self.extra:
            try:
                data = a.read(path)
            except SystemExit as e:   # a compression mpq_extract does not know
                print('    %s: %s' % (path, e))
                continue
            if data is not None:
                self.from_extra += 1
                return path, data
        return None

    def has(self, path):
        return path.upper() in self.work or any((hash_string(path, 1), hash_string(path, 2)) in a.index for a in self.extra)

    def copy(self, path, force=False, dest=None):
        """Copy one file (to dest, a client path, if given); returns the output path, or None when it was not copied."""
        if not force and not dest and self.is_stock(path):
            return None
        hit = self.read(path)
        if hit is None:
            if not self.is_stock(path):
                self.missing.append(path)
            return None
        client, data = hit
        client = dest or client
        dst = os.path.join(self.out, *client.split(B))
        if os.path.exists(dst) and not force:
            if open(dst, 'rb').read() != data:
                self.kept.append(client)
            return dst
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'wb') as fh:
            fh.write(data)
        self.copied += 1
        return dst

    def model_files(self, path):
        """The model's .skin and .anim files and the textures it names (type 0)."""
        hit = self.read(path)
        if hit is None:
            return []
        data = hit[1]
        base = path[:-3]
        files = ['%s%02d.skin' % (base, n) for n in range(struct.unpack_from('<I', data, coa_race_prep.NUM_SKINS)[0])]
        table = m2_anim_split.sequences(data)
        files += sorted({base + m2_anim_split.anim_name(table, '', s) for s in range(len(table))
                         if not table[s][2] & m2_anim_split.HAS_DATA})
        return files + coa_race_prep.texture_names(data)


def unfilled_geosets(skin, model):
    """Geosets of a .skin drawn only with replaceable texture types 11 and up (nothing fills them without the DLL)."""
    count, offset = struct.unpack_from('<II', skin, 0x1C)
    ids = [struct.unpack_from('<H', skin, offset + 48 * i)[0] for i in range(count)]
    combo_types = coa_race_prep.texture_types(model)
    bcount, boffset = struct.unpack_from('<II', skin, 0x24)
    types_of = {}
    for i in range(bcount):
        section = struct.unpack_from('<H', skin, boffset + 24 * i + 4)[0]
        combo = struct.unpack_from('<H', skin, boffset + 24 * i + 16)[0]
        types_of.setdefault(ids[section], set()).add(combo_types[combo])
    return {g for g, types in types_of.items() if g and all(t >= 11 for t in types)}


def hide_unfilled_submeshes(skin, model):
    """Move geoset 0 submeshes drawn only with replaceable types 11 and up (the DLL's baked armour on the Gnoll's body
    geoset) to the hidden geoset: geoset 0 is always drawn, so hiding by geoset can't reach them."""
    b = bytearray(skin)
    count, offset = struct.unpack_from('<II', b, 0x1C)
    combo_types = coa_race_prep.texture_types(model)
    bcount, boffset = struct.unpack_from('<II', b, 0x24)
    types_of = {}
    for i in range(bcount):
        section = struct.unpack_from('<H', b, boffset + 24 * i + 4)[0]
        types_of.setdefault(section, set()).add(combo_types[struct.unpack_from('<H', b, boffset + 24 * i + 16)[0]])
    parked = []
    for i in range(count):
        if struct.unpack_from('<H', b, offset + 48 * i)[0] == 0 and types_of.get(i) and all(t >= 11 for t in types_of[i]):
            struct.pack_into('<H', b, offset + 48 * i, coa_race_prep.coa_races.HIDDEN_GEOSET)
            parked.append(i)
    return bytes(b), parked


def prepare_catalog(cp, catalogs, race, models):
    # catalogs: the folder of the release's catalogs, or {gender: look} already made (coa199_replace.py)
    looks = catalogs if isinstance(catalogs, dict) else coa199_races.catalog(coa199_races.catalog_path(catalogs, race))
    for gender, path in enumerate(models):
        if gender and path == models[0]:
            continue   # one body for both genders
        look = coa199_races.look_for(looks, coa199_races.ONE_BODY.get(race.key, gender))   # one body: its gender's look
        if not cp.has(path):
            cp.missing.append(path)
            continue
        if cp.is_stock(path):
            raise SystemExit('%s: %s is a stock model; patching it would change the stock NPCs' % (race.key, path))
        files = [f for f in cp.model_files(path) if not f.endswith(".skin")]   # the .skin files are copied and patched below
        for f in files + list(look.fixed.values()) + [p for skin in look.skins for p in skin]:
            cp.copy(f)
        m2 = cp.copy(path, force=True)
        model, changes = coa_race_prep.patch_model(open(m2, 'rb').read(), look)
        open(m2, 'wb').write(model)
        print('%s %s: %s' % (race.key, path, '; '.join(changes) or 'no texture changes'))
        # geosets the catalog always shows but that are drawn only with creature texture types still unfilled after
        # the patch (type 14: the DLL's baked armour, as Kyrian's type 15) go too: without the DLL they'd be untextured
        baked = unfilled_geosets(cp.read('%s00.skin' % path[:-3])[1], model)
        if baked & look.keep:
            look = copy.copy(look)
            look.keep = look.keep - baked
            print('    hiding the always-shown geosets drawn only with unfilled types: %s' % sorted(baked))
        for n in range(struct.unpack_from('<I', model, coa_race_prep.NUM_SKINS)[0]):
            skin_path = cp.copy('%s%02d.skin' % (path[:-3], n), force=True)
            if skin_path is None:
                continue
            skin, hidden, shown, used = coa_race_prep.patch_skin(open(skin_path, 'rb').read(), look, model)
            skin, parked = hide_unfilled_submeshes(skin, model)
            if parked and n == 0:
                print('    always-drawn (geoset 0) submeshes drawn only with unfilled types, hidden: %s' % parked)
            open(skin_path, 'wb').write(skin)
            if n == 0:
                print('    hidden geosets %s; always shown %s; texture types drawn %s' % (hidden, shown, used))
                missing = [t for t in used if t >= 11]
                if missing:
                    print('    WARNING: shown batches use replaceable types without a texture: %s' % missing)


def trim_skins(cp, path):
    """A model whose later .skin files (lower detail levels) nobody has declares only those that exist; the client
    would otherwise fail to load the missing ones."""
    m2 = os.path.join(cp.out, *path.split(B))
    if not os.path.exists(m2):
        return
    data = bytearray(open(m2, 'rb').read())
    count = struct.unpack_from('<I', data, coa_race_prep.NUM_SKINS)[0]
    have = 0
    while have < count and os.path.exists(m2[:-3] + '%02d.skin' % have):
        have += 1
    if 0 < have < count:
        struct.pack_into('<I', data, coa_race_prep.NUM_SKINS, have)
        open(m2, 'wb').write(bytes(data))
        print('    %s: %d of its %d .skin files exist; it now declares %d' % (path, have, count, have))


def prepare_classic(cp, dbc, race, models):
    for path in dict.fromkeys(models):
        new = coa199_races.target(path)   # a renamed model takes its .skin and .anim files along
        for f in [path] + cp.model_files(path):
            renamed = f.lower().startswith(path[:-3].lower()) and new != path
            cp.copy(f, dest=new[:-3] + f[len(path) - 3:] if renamed else None)
        trim_skins(cp, new)
    textures = section_textures(dbc, race.coa_id)
    for t in dict.fromkeys(textures):
        cp.copy(t)
    print('%s: %s, %d CharSections textures' % (race.key, ' / '.join(dict.fromkeys(models)), len(set(textures))))


def main():
    args = sys.argv[1:]
    if len(args) < 5:
        sys.exit(__doc__)
    extra = None
    if '--extra' in args:
        i = args.index('--extra')
        extra = args[i + 1]
        del args[i:i + 2]
    work, catalogs, dbc, data, out = args[:5]
    wanted = set(args[5:])
    cp = Copier(work, data, out, extra)
    for race in coa199_races.RACES:
        if wanted and race.key not in wanted:
            continue
        models = race_models(dbc, race)
        if race.catalog:
            prepare_catalog(cp, catalogs, race, models)
        else:
            prepare_classic(cp, dbc, race, models)
    print('copied %d files (%d from --extra)' % (cp.copied, cp.from_extra))
    for what, paths in (('in neither the release, the extra client nor the stock client', cp.missing),
                        ('already in the output with other contents (kept)', cp.kept)):
        if paths:
            print('%d files %s:' % (len(set(paths)), what))
            for p in sorted(set(paths)):
                print('   ', p)


if __name__ == '__main__':
    main()
