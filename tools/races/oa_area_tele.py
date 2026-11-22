#!/usr/bin/env python3
"""`.tele` targets for Open Azeroth's areas, found in its terrain.

  python -I oa_area_tele.py MODPAK_DIR [--data DATA]

Reads the areas F-010 adds (MODPAK_DIR/dbc/[BASE,F-010]_areatable.sql) and every Kalimdor and Eastern Kingdoms tile
in Open Azeroth's maps (DATA/patch-OA-maps.MPQ). Each map chunk names its area. For each area on those maps, the
target is the chunk nearest the middle of the area's chunks that is dry (no liquid), whole (no terrain holes, which
drop players into the void) and flattest, at its centre, 1 yard above the ground. An area with no dry chunk (Vashj'ir's
are under the sea) gets a whole one under water instead, UNDERWATER yards above the sea floor. Names are the area's, in
CamelCase without punctuation (Keel Harbor -> KeelHarbor; .tele also finds a part of a name, so .tele keelharb works).

Leaves out names stock's game_tele already has (its target is kept and printed), names F-010's hand-picked
zz_[F-010]_game_tele.sql sets, and names two areas share (printed). Writes
MODPAK_DIR/sql/db-world/base/zz_[F-010]_game_tele_areas.sql, ids from ID_BASE."""
import argparse, math, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "models"))
import transport_paths as tp  # noqa: E402
import adt_bake_shadows as ab  # noqa: E402
from mpq_unpack import Archive  # noqa: E402

MAPS = {"@EasternKingdoms": (0, "Azeroth"), "@Kalimdor": (1, "Kalimdor"), "0": (0, "Azeroth"), "1": (1, "Kalimdor")}
ID_BASE = 88000
STOCK_TELE = os.path.join(HERE, "..", "..", "..", "azerothcore-wotlk-256-bit", "data", "sql", "base", "db_world",
                          "game_tele.sql")
UNDERWATER = 3.0
SKIP = re.compile(r"unused|do not use|\btest\b|\[|deprecated|^zz", re.I)


def areas(sql):
    """{id: (map, name)} for the areas the SQL inserts on Kalimdor or the Eastern Kingdoms."""
    out = {}
    for m in re.finditer(r"INSERT INTO `areatable` \([^)]*\) VALUES \((\d+), ([^,]+), [^']*?'((?:[^'\\]|\\.|'')*)'",
                         sql):
        if m.group(2) in MAPS:
            out[int(m.group(1))] = (MAPS[m.group(2)][0], re.sub(r"\\(.)", r"\1", m.group(3)).replace("''", "'"))
    return out


def tele_name(name):
    words = re.findall(r"[A-Za-z0-9]+", name.replace("'", ""))
    return "".join(w[0].upper() + w[1:] for w in words)


def tile_chunks(d, tx, ty):
    """(area, x, y, ground, flatness) of each chunk whose centre is dry and whole, the same of each whole one under
    water, and (area, x, y) of every chunk.

    Dry: the ground at the centre is above the top of the chunk's water (MH2O layers, or MCLQ). Whole: none of the four
    middle squares of the chunk's 4 x 4 hole mask is a hole."""
    terrain = ab.Terrain(d, tx, ty)
    water = {}          # chunk index -> highest water surface
    for t, p, n in ab.chunks(d):
        if t == b'O2HM':           # MH2O: 256 headers (offset of the first layer, layer count, offset)
            base = p + 8
            for i in range(256):
                ofs, count, _ = struct.unpack_from('<III', d, base + i * 12)
                for k in range(count):     # layer: type, flags, min height, max height, ...
                    water[i] = max(water.get(i, -1e9), struct.unpack_from('<f', d, base + ofs + k * 24 + 8)[0])
    good, wet, every = [], [], []
    for t, p, n in ab.chunks(d):
        if t != b'KNCM':
            continue
        h = p + 8
        flags, ix, iy = struct.unpack_from('<III', d, h)
        area, = struct.unpack_from('<I', d, h + 0x34)
        holes, = struct.unpack_from('<H', d, h + 0x3C)
        ofs_lq, size_lq = struct.unpack_from('<II', d, h + 0x60)
        x = terrain.top_x - (iy + 0.5) * ab.CHUNK
        y = terrain.top_y - (ix + 0.5) * ab.CHUNK
        every.append((area, x, y))
        top = water.get(iy * 16 + ix, -1e9)
        if flags & 0x3C and size_lq > 8:           # 0x4..0x20: an MCLQ liquid, min and max height first
            top = max(top, struct.unpack_from('<f', d, p + ofs_lq + 8 + 4)[0])
        if holes & 0x0660:
            continue
        hs = [terrain.h[iy * 8 + r][ix * 8 + c] for r in range(9) for c in range(9)]
        (wet if terrain.at(x, y) < top + 0.5 else good).append((area, x, y, terrain.at(x, y), max(hs) - min(hs)))
    return good, wet, every


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("modpak")
    ap.add_argument("--data", default=tp.DATA)
    a = ap.parse_args()
    want = areas(open(os.path.join(a.modpak, "dbc", "[BASE,F-010]_areatable.sql"), encoding="utf-8").read())
    hand = set(re.findall(r", '([^']+)'\)", open(os.path.join(a.modpak, "sql", "db-world", "base",
                                                               "zz_[F-010]_game_tele.sql"), encoding="utf-8").read()))
    stock = {n.lower() for n in re.findall(r",'((?:[^']|\\')*)'\)", open(STOCK_TELE, encoding="utf-8").read())}
    arc = Archive(os.path.join(a.data, "patch-OA-maps.MPQ"))
    good, wet, every = {}, {}, {}
    for m, name in ((0, "Azeroth"), (1, "Kalimdor")):
        for ty in range(64):
            for tx in range(64):
                try:
                    d = arc.read("World\\Maps\\%s\\%s_%d_%d.adt" % (name, name, tx, ty))
                except Exception:
                    d = None
                if not d:
                    continue
                g, w, e = tile_chunks(d, tx, ty)
                for c in g:
                    good.setdefault((m, c[0]), []).append(c[1:])
                for c in w:
                    wet.setdefault((m, c[0]), []).append(c[1:])
                for c in e:
                    every.setdefault((m, c[0]), []).append(c[1:])
    rows, kept, dupes, missing, under, by_name = [], [], [], [], [], {}
    for aid, (m, name) in sorted(want.items()):
        tn = tele_name(name)
        if not tn or SKIP.search(name):
            continue
        if (m, aid) not in every:
            missing.append(name)
            continue
        by_name.setdefault(tn.lower(), []).append((aid, m, name, tn))
    for key, same in sorted(by_name.items()):
        if len(same) > 1:
            dupes.append("%s (%s)" % (same[0][3], ", ".join(str(s[0]) for s in same)))
            continue
        aid, m, name, tn = same[0]
        if tn in hand:
            continue
        if key in stock:
            kept.append(tn)
            continue
        cands, lift = good.get((m, aid)), 1.0
        if not cands:
            cands, lift = wet.get((m, aid)), UNDERWATER
            under.append(tn)
        if not cands:
            missing.append(name + " (no whole chunk)")
            under.pop()
            continue
        pts = every[(m, aid)]
        cx, cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        x, y, z, _ = min(cands, key=lambda c: math.hypot(c[0] - cx, c[1] - cy) + 20 * c[3])
        rows.append((m, x, y, z + lift, tn, name))
    out = os.path.join(a.modpak, "sql", "db-world", "base", "zz_[F-010]_game_tele_areas.sql")
    text = ["-- .tele targets for Open Azeroth's areas on Kalimdor and the Eastern Kingdoms: each one the dry, whole, flat",
            "-- map chunk nearest the middle of the area, or a whole one under water where none is dry (Vashj'ir). Generated",
            "-- by tools/races/oa_area_tele.py: change the script, not this file. Names stock already has keep stock's target; zz_[F-010]_game_tele.sql's hand-picked ones win.",
            "DELETE FROM `game_tele` WHERE `id` BETWEEN %d AND %d;" % (ID_BASE, ID_BASE + 999)]
    if rows:
        text.append("DELETE FROM `game_tele` WHERE `name` IN (%s);" % ", ".join("'%s'" % r[4] for r in rows))
        text.append("INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, "
                    "`name`) VALUES")
        text.append(",\n".join("(%d, %.1f, %.1f, %.1f, 0, %d, '%s')" % (ID_BASE + i, x, y, z, m, tn)
                               for i, (m, x, y, z, tn, _) in enumerate(rows)) + ";")
    assert len(rows) < 1000
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(text) + "\n")
    print("%d targets written to %s" % (len(rows), out))
    print("under water (%d): %s" % (len(under), ", ".join(under)))
    print("kept stock's target (%d): %s" % (len(kept), ", ".join(kept)))
    print("shared by several areas, left out (%d): %s" % (len(dupes), ", ".join(dupes)))
    print("not found in the terrain (%d): %s" % (len(missing), ", ".join(missing)))


if __name__ == "__main__":
    main()
