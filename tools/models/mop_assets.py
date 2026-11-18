#!/usr/bin/env python3
"""Fetch and convert the client files a MoP modpak's DBC rows name (F-134's Wandering Isle), from MoP Classic on wago.

  python -I mop_assets.py MODPAK STAGE [--common-out DIR] [--client DATA] [--common PATH] [--version V]
                          [--listfile CSV] [--fetch] [--convert] [--install]

What is wanted (each a list of candidate client paths, as in tools/checks/f013_item_assets.py):
- MODPAK/wi_assets.txt (if any): the port's creature and object models, NPC bakes and spell icons
- the item displays in MODPAK/dbc/*itemdisplayinfo*.sql (icons, models of any ObjectComponents folder, every race
  variant of a head model the listfile has, armour textures of any gender suffix)
- the texture variations of MODPAK/dbc/*creaturedisplayinfo*.sql, in their model's folder
A file counts as present when WHE-common's patch-A.MPQ, the client's patch folders or its MPQs have it.

--fetch downloads what is missing (wago.tools' MoP Classic build, --version) into STAGE under its community listfile
path (--listfile, D:/wow-scratch/listfile/community-listfile.csv), with the skins, .anim files and textures its models
name, and writes STAGE/listfile.csv. --convert runs Kalibro's wotlkconv on STAGE into STAGE-out, then
m2_unshare_tracks.py on every model and m2_restore_anim_refs.py on those with .anim files. --install copies STAGE-out
into --common-out (WHE-common/patch-MoP.MPQ for F-133 / F-134, linked into the client as patch-MoP.<realm>.MPQ).
Without flags it only reports what is missing and what the listfile can't name.
"""
import argparse, glob, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "checks"))
from retail_fetch import API, get, named, chunks, EXT  # noqa: E402
from f013_item_assets import tree, needs  # noqa: E402
from check_f013_assets import Archive  # noqa: E402

B = "\\"
CONVERTER = "D:/wow-scratch/wotlkconv/RaceGuide/sources/Converter"
STOCK_DBC = os.path.join(HERE, "..", "..", "..", "References", "original-client-dbc")


def sql_rows(paths, table):
    for path in paths:
        for block in re.findall(r"INSERT INTO `%s` SET(.*?);\n" % table, open(path, encoding="utf8").read(), re.S):
            yield {k: v.replace("\\\\", "\\") for k, v in re.findall(r"`(\w+)` = '?((?:[^'\n]|'')*?)'?,?$", block, re.M)}


def tile_models(tiles):
    """[(what, [candidate])] for the WMOs (MWMO), M2 doodads (MMDX) and terrain textures (MTEX) converted 3.3.5a
    tiles name."""
    out = set()
    for adt in glob.glob(os.path.join(tiles, "*.adt")):
        c = chunks(open(adt, "rb").read())
        for tag in (b"OMWM", b"XDMM", b"XETM"):
            for name in c.get(tag, b"").split(b"\0"):
                if name:
                    out.add(name.decode("latin1").replace("/", B))
                    if tag == b"XETM":  # with specular terrain on (the default) the client loads only <name>_s.blp
                        out.add(re.sub(r"\.blp$", "_s.blp", name.decode("latin1").replace("/", B), flags=re.I))
    return [("file " + p, [p]) if p.lower().endswith((".wmo", ".blp"))
            else ("model " + p, [re.sub(r"\.(m2|mdx)$", "", p, flags=re.I)]) for p in sorted(out)]


def strings(blob):
    return [s.decode("latin1") for s in blob.split(b"\0") if s]


def wmo_named(data, names):
    """The file ids a WMO root names: groups, doodads, textures, skybox (by id since 8.1, else by name)."""
    import struct
    c, ids = chunks(data), []
    ints = lambda b: list(struct.unpack("<%dI" % (len(b) // 4), b[:len(b) // 4 * 4]))  # noqa: E731
    ids += ints(c.get(b"DIFG", b"")) + ints(c.get(b"IDOM", b""))
    if b"ISOM" in c and len(c[b"ISOM"]) == 4:
        ids += ints(c[b"ISOM"])
    momt = c.get(b"TMOM", b"")
    if b"XTOM" not in c:
        for i in range(0, len(momt) - 63, 64):
            ids += [struct.unpack_from("<I", momt, i + o)[0] for o in (12, 24, 36)]
    lookup = lambda p: names.get(p.replace(B, "/").lower().replace(".mdx", ".m2"))  # noqa: E731
    ids += [lookup(s) for s in strings(c.get(b"XTOM", b"")) + strings(c.get(b"NDOM", b""))]
    return [i for i in ids if i]


def stock_models():
    import struct
    d = open(os.path.join(STOCK_DBC, "CreatureModelData.dbc"), "rb").read()
    _, n, fields, size, _ = struct.unpack("<4s4I", d[:20])
    table = 20 + n * size
    out = {}
    for i in range(n):
        mid, _, name = struct.unpack_from("<3I", d, 20 + i * size)
        out[mid] = d[table + name:d.index(b"\0", table + name)].decode("latin1")
    return out


def wanted(modpak):
    """[(what, [candidate client paths])]; model candidates have no extension."""
    out = []
    listed = os.path.join(modpak, "wi_assets.txt")
    for line in open(listed, encoding="utf8") if os.path.exists(listed) else []:
        p = line.strip()
        if not p:
            continue
        if p.lower().startswith("interface" + B + "icons" + B) and not p.lower().endswith(".blp"):
            p += ".blp"
        if re.search(r"\.(m2|mdx)$", p, re.I):
            out.append(("model " + p, [re.sub(r"\.(m2|mdx)$", "", p, flags=re.I)]))
        else:
            out.append(("file " + p, [p]))
    dbc = glob.glob(os.path.join(modpak, "dbc", "*.sql"))
    for row in sql_rows([p for p in dbc if "itemdisplayinfo" in p], "itemdisplayinfo"):
        out += needs(row)
    models = {r["id"]: r["model_path"] for r in sql_rows([p for p in dbc if "creaturemodeldata" in p], "creaturemodeldata")}
    stock = stock_models()
    for row in sql_rows([p for p in dbc if p.endswith("creaturedisplayinfo.sql")], "creaturedisplayinfo"):
        m = row.get("model_id", "")
        model = models.get(m) or (stock.get(int(m)) if m.isdigit() else None)
        if not model:
            continue
        folder = model.rsplit(B, 1)[0]
        for k in ("texture_variation_1", "texture_variation_2", "texture_variation_3"):
            if row.get(k):
                out.append(("texture " + folder + B + row[k], [folder + B + row[k] + ".blp"]))
    return out


class Present:
    def __init__(self, common, client):
        self.local = {}
        for root in [common] + [os.path.join(client, p) for p in ("patch-C.MPQ", "patch-B.MPQ", "patch-A.MPQ")]:
            for k, v in tree(root).items():
                self.local.setdefault(k, v)
        self.archives = [Archive(p) for p in glob.glob(os.path.join(client, "*.[mM][pP][qQ]"))
                         + glob.glob(os.path.join(client, "enUS", "*.[mM][pP][qQ]")) if os.path.isfile(p)]

    def __call__(self, path):
        if path.upper().endswith((".BLP", ".WMO")):
            return path.upper() in self.local or any(x.has(path) for x in self.archives)
        stem = path.upper()
        return any(k.startswith(stem) and k.endswith(".M2") for k in self.local) or \
            any(x.has(path + s + ".m2") for x in self.archives for s in ("", "_HuM", "_HuF"))


def listfile(path):
    out = {}
    for line in open(path, encoding="utf8", errors="replace"):
        f, _, p = line.strip().partition(";")
        if p and f.isdigit():
            out[p.lower()] = int(f)
    return out


def resolve(candidates, names):
    """Listfile paths for a want: textures exactly; models with every race / gender suffix the listfile has."""
    out = []
    for c in candidates:
        q = c.replace(B, "/").lower()
        if q.endswith((".blp", ".wmo")):
            if q in names:
                out.append(q)
        else:
            out += [p for p in names if p.startswith(q) and p.endswith(".m2")
                    and re.fullmatch(r"(_\w{2,4})?", p[len(q):-3])]
        if out:
            break
    return out


def patient_get(url, tries=10):
    """get, waiting out dropped connections (a long fetch outlives a flaky line); reruns resume from STAGE anyway."""
    for n in range(tries):
        try:
            return get(url)
        except OSError as e:
            if n + 1 == tries:
                raise
            print("network error (%s), retrying in 60 s" % e, flush=True)
            time.sleep(60)


def fetch(paths, names, stage, version):
    by_id = {v: k for k, v in names.items()}
    lf = os.path.join(stage, "listfile.csv")
    listing = {}
    if os.path.exists(lf):
        for line in open(lf, encoding="utf8"):
            f, _, p = line.strip().partition(";")
            listing[int(f)] = p
    queue = [names[p] for p in paths]
    seen, failed = set(), []
    while queue:
        fdid = queue.pop(0)
        if fdid in seen:
            continue
        seen.add(fdid)
        path = by_id.get(fdid)
        target = os.path.join(stage, *(path or "unnamed/%d" % fdid).split("/"))
        if os.path.exists(target):
            data = open(target, "rb").read()
        else:
            data = patient_get("%s/casc/%d?download&version=%s" % (API, fdid, version))
            if not data:
                failed.append(path or fdid)
                continue
            if not path:
                target += "." + EXT.get(data[:4], "wmo" if data[:4] == b"REVM" else "anim")
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)
            time.sleep(0.2)
        listing[fdid] = os.path.relpath(target, stage).replace(os.sep, "/")
        if data[:4] in (b"MD21", b"SKL1"):
            queue += named(data)
        elif data[:4] == b"REVM" and b"DHOM" in chunks(data):
            queue += wmo_named(data, names)
    with open(lf, "w", encoding="utf8", newline="\n") as f:
        f.writelines("%d;%s\n" % kv for kv in sorted(listing.items()))
    return len(seen) - len(failed), failed


def convert(stage):
    out = stage.rstrip("/\\") + "-out"
    cmd = [sys.executable, "-I", "-c", "import sys,runpy; sys.path.insert(0, %r); sys.argv = ['wotlkconv'] + sys.argv[1:]; "
           "runpy.run_module('wotlkconv', run_name='__main__')" % CONVERTER,
           "convert", stage, "-o", out, "-l", os.path.join(stage, "listfile.csv"), "-q"]
    subprocess.run(cmd, check=True)
    fixed, anims = 0, 0
    for m2 in glob.glob(os.path.join(out, "**", "*.m2"), recursive=True):
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "m2_unshare_tracks.py"), m2], check=True,
                       stdout=subprocess.DEVNULL)
        fixed += 1
        src = os.path.join(stage, os.path.relpath(m2, out))
        if glob.glob(os.path.splitext(m2)[0] + "*.anim") and os.path.exists(src):
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "m2_restore_anim_refs.py"), m2, src],
                               capture_output=True, text=True)
            anims += 1
            if r.returncode:
                print("  anim refs not restored: %s (%s)" % (m2, (r.stderr or r.stdout).strip().splitlines()[-1:]))
    print("converted into %s: %d models fixed, %d with .anim files" % (out, fixed, anims))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modpak")
    ap.add_argument("stage")
    ap.add_argument("--common-out")
    ap.add_argument("--client", default="C:/Users/Medviten/Desktop/WowSquished-256-bit/Data")
    ap.add_argument("--common", default="D:/GitHub/WHE-common/patch-A.MPQ")
    ap.add_argument("--version", default="5.5.4.70631")
    ap.add_argument("--listfile", default="D:/wow-scratch/listfile/community-listfile.csv")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--convert", action="store_true")
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--tiles", help="also the WMOs and doodads these converted 3.3.5a tiles place")
    a = ap.parse_args()
    present = Present(a.common, a.client)
    extra = tree(a.common_out) if a.common_out and os.path.isdir(a.common_out) else {}
    names = listfile(a.listfile)
    want, unnamed = set(), []
    for what, candidates in wanted(a.modpak) + (tile_models(a.tiles) if a.tiles else []):
        if any(present(c) for c in candidates) or any(
                c.upper() in extra or (not c.upper().endswith((".BLP", ".WMO")) and any(k.startswith(c.upper()) and k.endswith(".M2")
                                                                             for k in extra)) for c in candidates):
            continue
        found = resolve(candidates, names)
        if found:
            want |= set(found)
        else:
            unnamed.append(what)
    print("%d files to fetch; %d wants nothing names: %s" % (len(want), len(unnamed), ", ".join(sorted(unnamed)[:20])))
    if a.fetch:
        n, failed = fetch(sorted(want), names, a.stage, a.version)
        print("fetched %d files (with dependencies); %d not in %s: %s" % (n, len(failed), a.version, failed[:20]))
    out = a.stage.rstrip("/\\") + "-out"
    if a.convert:
        out = convert(a.stage)
    if a.install:
        if not a.common_out:
            sys.exit("--install needs --common-out")
        n = 0
        for f in glob.glob(os.path.join(out, "**", "*"), recursive=True):
            if os.path.isfile(f) and not f.endswith((".csv", ".json", ".txt")):
                dest = os.path.join(a.common_out, os.path.relpath(f, out))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(f, dest)
                n += 1
        print("installed %d files into %s" % (n, a.common_out))


if __name__ == "__main__":
    main()
