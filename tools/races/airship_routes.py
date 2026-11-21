#!/usr/bin/env python3
"""Transport routes (gunships, ferries) as DBC and world SQL, from a few waypoints per map.

  python -I airship_routes.py ROUTE MODPAK_DIR

ROUTES below holds each route: the TaxiPath id (fixed, since the game object names it), the game object (entry,
display, name, transport guid, speed) and its legs, one per map in order. The path loops: from its last point the
transport is teleported to its first, as stock's boats are. A leg is a list of waypoints, (x, y, z) for the ship's
origin, or ("berth", x, y, z, heading, side) for a stop: (x, y, z) is where the gangway meets the dock or ledge (the
point to read with .gps in game), heading the direction (degrees, 0 = +x, north) the ship moves along while berthed,
side +1 or -1 for which flank faces it (the ship's left or right). The ship's origin is then set half a hull's width
out from that point and DECK below it. ("stop", x, y, z, heading) is a stop at a zeppelin tower: (x, y, z) the
transport's own origin there (a stock tower's berth, or a static zeppelin the transport replaces), heading the way it
moves through it; level guide points LEAD yards either side keep the hull straight along the berth. Waypoints are smoothed into points SPACING apart (Catmull-Rom), and the hull's
bottom is checked against the terrain (water as 0) along the way; clashes are printed, not fixed.

Writes MODPAK_DIR/dbc/[TAG]_<name>_path.sql (TaxiPath, TaxiPathNode with ids from MAX(id), as F-006 does) and
MODPAK_DIR/sql/db-world/base/[TAG]_<name>_transport.sql (gameobject_template, its addon, transports)."""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "models"))
import transport_paths as tp  # noqa: E402
import adt_bake_shadows as ab  # noqa: E402
from mpq_unpack import Archive  # noqa: E402

SPACING, STOP_DELAY, LEAD = 60.0, 60, 90.0
HULLS = {   # display -> (half width, deck height above the origin), from the WMO's bounds and its stock crew
    8253: (83.0, 30.0),     # Orgrim's Hammer (Hellscream's Fist)
    8254: (50.0, 12.0),     # The Skybreaker (The Skyfire)
}
ROUTES = {
    "hellscreams_fist": dict(
        tag="F-133", path=13900, entry=1390002, guid=13902, display=8253, speed=30, accel=1,
        name="Hellscream's Fist", where="Bladefist Bay, Durotar and Honeydew Village, the Jade Forest (Gunship, Horde)",
        legs=[
            (1, [(2000, -5800, 250), (1450, -5450, 120), (1300, -5150, 40),
                 # FIRST CUT: Bladefist Bay's dock, east side (dock bounds x 1393-1478, y -5027..-4903, walkway z ~12).
                 # Replace with a .gps reading where the gangway should meet it.
                 ("berth", 1478, -4965, 12, 0, -1),
                 (1700, -5000, 40), (1950, -5450, 200), (2300, -5900, 300)]),
            (870, [(4600, -250, 350), (3700, -247, 300),
                   # FIRST CUT, to be replaced by the zeppelin tower F-133 placed at (3200, -600): see below
                   # FIRST CUT: Honeydew's cliff ledge (flat z ~267 at x 3100, y -420..-340, dropping into the inlet)
                   ("berth", 3100, -335, 267, 180, -1),
                   (2850, -247, 300), (2700, 100, 650), (3200, 400, 650), (4200, 0, 500), (4800, -250, 350)]),
        ]),
    # Bladefist Bay's zeppelin tower (Open Azeroth tile, build_oa.py: origin (1310, -4905, 11.4), yaw 270; its berths
    # repeat the stock Durotar tower's, headings as the stock zeppelins move through them) and Kezan's goblin tower,
    # whose north static zeppelin (uid 267669) build_oa.py hides so this one takes its place. Its MODF yaw -95.7 is
    # world 84.3 (CMap::CreateMapObjDef adds 180), the way the model's +X points; AzerothCore turns a transport to its
    # heading + 180 (TransportMgr::GeneratePath), so to look the same it moves through at -95.7, eastwards.
    # Out of Bladefist's west berth over Durotar, south over the sea, into Kezan from the sea to its west, out east
    # over the town, north over the sea and into Bladefist Bay from the east.
    "kezan_zeppelin": dict(
        tag="F-142", path=14200, entry=1420002, guid=14202, display=3031, speed=30, accel=1,
        name="Zeppelin to Kezan", where="Bladefist Bay, Durotar and Kezan (zeppelin)",
        legs=[
            (1, [("stop", 1283.5, -4906.3, 60.5, 75.5),
                 (1200, -4720, 140), (700, -4650, 250), (-600, -4900, 300), (-4500, -7300, 300),
                 (-8100, -9800, 280), (-8800, -10250, 220),
                 ("stop", -8912.9, -10651.3, 170.6, -95.7),
                 (-8820, -11050, 230), (-8450, -11150, 270), (-6300, -9700, 300), (-2500, -7600, 300),
                 (900, -5900, 280), (1500, -5450, 200), (1330, -5180, 110)]),
        ]),
}
MAP_DIRS = {0: ("Azeroth", "patch-OA-maps.MPQ"), 1: ("Kalimdor", "patch-OA-maps.MPQ"),
            870: ("HawaiiMainland", "patch-MoP-Pandaria.MPQ")}


class Ground:
    def __init__(self):
        self.archives, self.tiles = {}, {}
        self.stock = Archive(os.path.join(tp.DATA, "patch-3.mpq"))

    def at(self, m, x, y):
        name, arc = MAP_DIRS[m]
        tx, ty = int(32 - y / ab.TILE), int(32 - x / ab.TILE)
        if (m, tx, ty) not in self.tiles:
            if arc not in self.archives:
                self.archives[arc] = Archive(os.path.join(tp.DATA, arc))
            path = "World\\Maps\\%s\\%s_%d_%d.adt" % (name, name, tx, ty)
            d = self.archives[arc].read(path) or self.stock.read(path)
            self.tiles[(m, tx, ty)] = ab.Terrain(d, tx, ty) if d else None
        t = self.tiles[(m, tx, ty)]
        return max(t.at(x, y), 0.0) if t else 0.0


def catmull(points, spacing):
    """Points every ~spacing along a Catmull-Rom curve through points (kept exactly)."""
    out = []
    for i in range(len(points) - 1):
        p0, p1, p2, p3 = (points[max(i - 1, 0)], points[i], points[i + 1], points[min(i + 2, len(points) - 1)])
        n = max(1, int(math.dist(p1, p2) / spacing))
        for k in range(n):
            s = k / n
            out.append(tuple(0.5 * (2 * b + (-a + c) * s + (2 * a - 5 * b + 4 * c - d) * s * s
                                    + (-a + 3 * b - 3 * c + d) * s ** 3) for a, b, c, d in zip(p0, p1, p2, p3)))
    return out + [points[-1]]


def build(name, out_dir):
    r = ROUTES[name]
    half, deck = HULLS.get(r["display"], (0.0, 0.0))
    ground, rows, clashes = Ground(), [], []
    for m, wps in r["legs"]:
        ctrl, stops = [], set()
        for w in wps:
            if w[0] == "berth":
                _, x, y, z, heading, side = w
                a = math.radians(heading + 90 * side)      # out from the dock, away from the flank facing it
                ctrl.append((x + half * math.cos(a), y + half * math.sin(a), z - deck))
                stops.add(len(ctrl) - 1)
            elif w[0] == "stop":
                # the transport's own origin at a tower berth, moving along heading: level guide points LEAD yards
                # either side make the curve pass straight through, so the hull lies along the berth
                _, x, y, z, heading = w
                h = math.radians(heading)
                ctrl.append((x - LEAD * math.cos(h), y - LEAD * math.sin(h), z))
                ctrl.append((float(x), float(y), float(z)))
                stops.add(len(ctrl) - 1)
                ctrl.append((x + LEAD * math.cos(h), y + LEAD * math.sin(h), z))
            else:
                ctrl.append(tuple(map(float, w)))
        if len(r["legs"]) == 1 and wps[0][0] == "stop":
            # one map, starting at a stop: close the loop as stock's single-map boats do (path 303): end on a copy of
            # the first guide, stop and guide. AzerothCore drops a path's first and last node (spline guides) and
            # teleports from the last kept node to the first, here from the stop to itself; each copy waits half
            ctrl += ctrl[:3]
            r["closed"] = True
        pts = catmull(ctrl, SPACING)
        stop_at = {ctrl[i] for i in stops}
        for p in pts:
            g = ground.at(m, p[0], p[1])
            if p[2] < g + 2:
                clashes.append((m, round(p[0]), round(p[1]), round(p[2]), round(g)))
            rows.append((m, p, p in stop_at))
    tag, pid = r["tag"], r["path"]
    dbc = ["-- %s: %s. Generated by tools/races/airship_routes.py %s: change the script, not this file."
           % (r["name"], r["where"], name), "",
           "DELETE FROM `taxipath` WHERE `id` = %d;" % pid,
           "INSERT INTO `taxipath` (`id`, `from_taxi_node`, `to_taxi_node`, `cost`) VALUES (%d, 0, 0, 0);" % pid, "",
           "DELETE FROM `taxipathnode` WHERE `path_id` = %d;" % pid,
           "SET @TaxiPathNodeID = (SELECT COALESCE(MAX(id), 0) FROM `taxipathnode`);",
           "INSERT INTO `taxipathnode` (`id`, `path_id`, `node_index`, `map`, `x`, `y`, `z`, `flags`, `delay`, "
           "`arrival_event_id`, `departure_event_id`) VALUES"]
    dbc.append(",\n".join("  (@TaxiPathNodeID := @TaxiPathNodeID + 1, %d, %d, %d, %.2f, %.2f, %.2f, %d, %d, 0, 0)"
                          % (pid, i, m, p[0], p[1], p[2], 2 if stop else 0,
                             STOP_DELAY // sum(1 for _, q, _ in rows if q == p) if stop else 0)
                          for i, (m, p, stop) in enumerate(rows)) + ";")
    world = ["-- %s: %s. Generated by tools/races/airship_routes.py %s: change the script, not this file."
             % (r["name"], r["where"], name), "",
             "DELETE FROM `gameobject_template` WHERE `entry` = %d;" % r["entry"],
             "INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, `castBarCaption`, "
             "`unk1`, `size`, `Data0`, `Data1`, `Data2`, `Data3`, `Data4`, `Data5`, `Data6`, `Data7`, `Data8`, `Data9`, "
             "`Data10`, `Data11`, `Data12`, `Data13`, `Data14`, `Data15`, `Data16`, `Data17`, `Data18`, `Data19`, "
             "`Data20`, `Data21`, `Data22`, `Data23`, `AIName`, `ScriptName`, `VerifiedBuild`) VALUES",
             "  (%d, 15, %d, '%s', '', '', '', 1, %d, %d, %d, 0, 0, 0, 0%s, '', '', 0);"
             % (r["entry"], r["display"], r["name"].replace("'", "''"), pid, r["speed"], r["accel"], ", 0" * 17), "",
             "DELETE FROM `gameobject_template_addon` WHERE `entry` = %d;" % r["entry"],
             "INSERT INTO `gameobject_template_addon` (`entry`, `faction`, `flags`) VALUES (%d, 0, 40);" % r["entry"], "",
             "DELETE FROM `transports` WHERE `guid` = %d;" % r["guid"],
             "INSERT INTO `transports` (`guid`, `entry`, `name`, `ScriptName`) VALUES (%d, %d, '%s', '');"
             % (r["guid"], r["entry"], r["where"].replace("'", "''"))]
    for sub, fname, text in (("dbc", "[%s]_%s_path.sql" % (tag, name), dbc),
                             (os.path.join("sql", "db-world", "base"), "[%s]_%s_transport.sql" % (tag, name), world)):
        os.makedirs(os.path.join(out_dir, sub), exist_ok=True)
        open(os.path.join(out_dir, sub, fname), "w", encoding="utf-8", newline="\n").write("\n".join(text) + "\n")
    print("%s: %d points over maps %s, %d stops; hull below the terrain at %d points%s" % (
        name, len(rows), [m for m, _ in r["legs"]], sum(s for _, _, s in rows), len(clashes),
        "".join("\n  map %d (%d, %d) bottom %d, ground %d" % c for c in clashes[:20])))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ROUTES:
        sys.exit(__doc__ + "\nroutes: " + ", ".join(ROUTES))
    build(sys.argv[1], sys.argv[2])
