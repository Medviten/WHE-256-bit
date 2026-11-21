#!/usr/bin/env python3
"""Smooth a boat's TaxiPathNode path and check it stays on water, for Open Azeroth's moved and added boat routes.

  python -I transport_paths.py PATH_ID OUT_SQL [--drop I,I...] [--move I=X,Y] [--dbc DIR] [--data DATA]
                                [--comment TEXT] [--rounds N]

Reads the path from a built client's TaxiPathNode.dbc (--dbc, default the test client's War realm patch), drops the
--drop node indices (doubled-back points), and smooths the rest with Chaikin's corner cutting (ROUNDS rounds). Points
within KEEP of a stop (flags 2: the docks, with their delays and events) stay exactly where they are, so the boat still
docks where the NPCs wait. Points closer than MIN_GAP to the previous one are merged. Then it samples the terrain along
the new path (Open Azeroth's ADTs, stock's where OA has none) and lists every stretch away from the docks where the sea
is shallower than DRAFT: boats run at z 0, so ground above -DRAFT means the hull is on land.

Writes OUT_SQL: the path's points replaced (DELETE by path; new ids after the highest one there when the SQL runs, as
F-006 does, so they never land on another modpak's). Boats at z 0 as stock's are."""
import argparse, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "models"))
import cata406_dbc_port as c406  # noqa: E402
from mpq_unpack import Archive  # noqa: E402
import adt_bake_shadows as ab  # noqa: E402

DBC = r"C:\Users\Medviten\Desktop\WowSquished-256-bit\Data\patch-WHE.war.MPQ\DBFilesClient"
DATA = r"C:\Users\Medviten\Desktop\WowSquished-256-bit\Data"
MAPS = {0: "Azeroth", 1: "Kalimdor"}
ROUNDS, KEEP, MIN_GAP, DRAFT, STEP, DOCK = 2, 3, 60.0, 4.0, 20.0, 250.0


class Ground:
    def __init__(self, data):
        self.archives = [Archive(os.path.join(data, n)) for n in ("patch-OA-maps.MPQ", "patch-3.mpq")]
        self.tiles = {}

    def at(self, m, x, y):
        tx, ty = int(32 - y / ab.TILE), int(32 - x / ab.TILE)
        if (m, tx, ty) not in self.tiles:
            name = "World\\Maps\\%s\\%s_%d_%d.adt" % (MAPS[m], MAPS[m], tx, ty)
            d = next((d for d in (a.read(name) for a in self.archives) if d), None)
            self.tiles[(m, tx, ty)] = ab.Terrain(d, tx, ty) if d else None
        t = self.tiles[(m, tx, ty)]
        return t.at(x, y) if t else -1000.0      # no tile: open sea


def chaikin(points, fixed):
    """One round on a list of (x, y, keep) points; kept points and their neighbours' midpoints stay put."""
    out = [points[0]]
    for a, b in zip(points, points[1:]):
        if a[2] and b[2]:
            out.append(b)
            continue
        q = (0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1], False)
        r = (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1], False)
        out += ([] if a[2] else [q]) + [r] + ([b] if b[2] else [])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=int)
    ap.add_argument("out")
    ap.add_argument("--drop", default="")
    ap.add_argument("--dbc", default=DBC)
    ap.add_argument("--data", default=DATA)
    ap.add_argument("--comment", default="")
    ap.add_argument("--move", action="append", default=[], metavar="I=X,Y",
                    help="move node index I to X,Y before smoothing (off a shoal)")
    ap.add_argument("--rounds", type=int, default=ROUNDS, help="smoothing rounds (0: check the path as it is)")
    a = ap.parse_args()

    rows = sorted((r for r in c406.Dbc(os.path.join(a.dbc, "TaxiPathNode.dbc")).records if r[1] == a.path),
                  key=lambda r: r[2])
    drop = {int(i) for i in a.drop.split(",") if i}
    moves = {int(k): tuple(map(float, v.split(","))) for k, v in (m.split("=") for m in a.move)}
    rows = [r for r in rows if r[2] not in drop]
    m = rows[0][3]
    assert all(r[3] == m for r in rows), "paths over more than one map aren't handled"
    stops = [i for i, r in enumerate(rows) if r[7] & 2]
    keep = {i for s in stops for i in range(s - KEEP, s + KEEP + 1)}
    pts = [moves.get(r[2], (c406.f32(r[4]), c406.f32(r[5]))) + (i in keep,) for i, r in enumerate(rows)]
    stop_at = {(c406.f32(rows[s][4]), c406.f32(rows[s][5])): rows[s] for s in stops}
    for _ in range(a.rounds):
        pts = chaikin(pts, keep)
    merged = [pts[0]]
    for p in pts[1:]:
        if p[2] or math.dist(p[:2], merged[-1][:2]) >= MIN_GAP:
            merged.append(p)
    pts = merged

    ground = Ground(a.data)
    docks = [(c406.f32(rows[s][4]), c406.f32(rows[s][5])) for s in stops]
    shallow = []
    for (x0, y0, _), (x1, y1, _) in zip(pts, pts[1:] + pts[:1]):
        n = max(1, int(math.dist((x0, y0), (x1, y1)) / STEP))
        for k in range(n):
            x, y = x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n
            g = ground.at(m, x, y)
            if g > -DRAFT and all(math.dist((x, y), d) > DOCK for d in docks):
                shallow.append((round(x), round(y), round(g, 1)))
    turns = []
    for p, q, r in zip(pts, pts[1:], pts[2:]):
        h1, h2 = math.atan2(q[1] - p[1], q[0] - p[0]), math.atan2(r[1] - q[1], r[0] - q[0])
        turns.append((abs(math.degrees((h2 - h1 + math.pi) % (2 * math.pi) - math.pi)), round(q[0]), round(q[1])))

    lines = ["-- %s" % a.comment if a.comment else "", "-- Generated by tools/races/transport_paths.py %d (%s): "
             "change the script's arguments, not this file." % (a.path, " ".join(
                 ["drop " + (a.drop or "none")] + ["move " + m for m in a.move])), "",
             "DELETE FROM `taxipathnode` WHERE `path_id` = %d;" % a.path,
             "SET @TaxiPathNodeID = (SELECT COALESCE(MAX(id), 0) FROM `taxipathnode`);",
             "INSERT INTO `taxipathnode` (`id`, `path_id`, `node_index`, `map`, `x`, `y`, `z`, `flags`, `delay`, "
             "`arrival_event_id`, `departure_event_id`) VALUES"]
    vals = []
    for i, (x, y, _) in enumerate(pts):
        s = stop_at.get((x, y))
        flags, delay, arr, dep = (s[7], s[8], s[9], s[10]) if s else (0, 0, 0, 0)
        vals.append("  (@TaxiPathNodeID := @TaxiPathNodeID + 1, %d, %d, %d, %.4f, %.4f, 0, %d, %d, %d, %d)" % (
            a.path, i, m, x, y, flags, delay, arr, dep))
    open(a.out, "w", encoding="utf-8", newline="\n").write("\n".join(lines).lstrip("\n") + "\n" + ",\n".join(vals) + ";\n")
    print("%d points (was %d), %d stops kept, sharpest turn %.0f deg at %s; shallow water away from docks: %d samples"
          % (len(pts), len(rows) + len(drop), len(stops), max(turns)[0], max(turns)[1:], len(shallow)))
    for s in shallow[:40]:
        print("  shallow", s)


if __name__ == "__main__":
    main()
