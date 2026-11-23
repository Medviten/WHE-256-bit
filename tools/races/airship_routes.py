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
moves through it; level guide points LEAD yards either side keep the hull straight along the berth. With heading None
there are no guide points: the waypoints around it shape the berth (a stock path's own nodes, for instance). A stop may
add (arrival event, departure event), as stock's stops do. Waypoints are smoothed into points SPACING apart
(Catmull-Rom), and the hull's bottom is checked against the terrain (water as 0) along the way; clashes are printed, not
fixed. A boat (boat=True) runs at its waypoints' z (0, as stock's) and clashes where the sea is shallower than DRAFT.

A single-map route, or one whose first and last legs share a map, closes itself stock style when its second control
point is a stop (a "stop" with guides first, or a plain point and then a stop). A seamless route (seamless=CHAIN, one
of CHAINS) changes map where continent_bridge.lua does: its legs are smoothed as one curve in Kalimdor's frame and the
transport is teleported from the crossing point on one map to the same point on the next, so it doesn't jump. "east"
crosses straight from Kalimdor's east edge to the Eastern Kingdoms' west edge; "northrend" crosses Northrend's southern
sea, which the lua lays over both, so the trip covers the whole distance. stock=ENTRY points an existing transport at the path instead of adding one.

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
    # Bladefist Bay's zeppelin tower (Open Azeroth tile, build_oa.py: origin (1270, -4915, 9.9), yaw 270; its berths
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
            (1, [("stop", 1243.5, -4916.3, 59.0, 75.5),
                 (1200, -4720, 140), (700, -4650, 250), (-600, -4900, 300), (-4500, -7300, 300),
                 (-8100, -9800, 280), (-8800, -10250, 220),
                 # Kezan's berth, guide points written out: level in from the sea (90 yd out), but out over the town
                 # climbing at once (30 yd out 35 higher, 60 yd out 60 higher; 30 higher at 60 clipped in game, 50 barely),
                 # since a goblin house 37 yd east of the berth reaches 147.5, the hull's bottom is 26.6 below its
                 # origin and its nose reaches 49 yd ahead; then over the garage (131), the houses and the big wall (242)
                 (-8903.9, -10561.7, 170.6),
                 ("stop", -8912.9, -10651.3, 170.6, None),
                 (-8915.9, -10681.1, 205.0), (-8918.9, -10711.0, 230.0), (-8905, -10800, 260),
                 (-8820, -11050, 275), (-8450, -11150, 280), (-6300, -9700, 300), (-2500, -7600, 300),
                 (900, -5900, 280), (1500, -5450, 200), (1330, -5180, 110)]),
        ]),
    # The second Kezan zeppelin, in place of Kezan's south static zeppelin (uid 267668, MODF yaw -91.3, also hidden by
    # build_oa.py) and at Bladefist's east berth. Both berths face one way, so it runs a figure eight rather than the
    # first's loop backwards: out of Kezan east as the first does (43 yd to its south), north over the sea east of the
    # first's route, over Durotar and into Bladefist's east berth from inland, out over the bay, south over the sea
    # further east, west over Kezan's north and into its berth from the sea alongside the first. It starts at Kezan, so
    # it runs about half a lap behind the first; the laps differ, so that drifts. Where the two routes cross it flies
    # 60-100 yd higher (the hull is 56 tall); near the towers the berths' axes splay apart, and each keeps to its own.
    "kezan_zeppelin_south": dict(
        tag="F-142", path=14201, entry=1420003, guid=14203, display=3031, speed=30, accel=1,
        name="Zeppelin to Kezan", where="Bladefist Bay, Durotar and Kezan (zeppelin)",
        legs=[
            (1, [(-8953.75, -10559.17, 170.9),
                 ("stop", -8955.84, -10649.15, 170.9, None),
                 # nothing tall east of this berth, but climb out as the first does
                 (-8956.54, -10679.14, 205.9), (-8957.23, -10709.13, 230.9), (-8955, -10800, 260),
                 (-8850, -11150, 300), (-8300, -11550, 340), (-6050, -10050, 360), (-2250, -7950, 360),
                 (600, -5900, 360), (800, -4900, 330), (950, -4500, 260), (1149, -4475, 200),
                 (1196.8, -4617.6, 150),     # on the east berth's axis, 300 yd out
                 ("stop", 1291.9, -4902.0, 59.0, -71.5),
                 (1371.2, -5139.0, 110), (1450, -5200, 150), (1700, -5300, 230), (1900, -5800, 300),
                 (-2000, -8400, 400), (-6000, -10600, 400), (-7200, -9600, 380), (-7700, -9300, 360),
                 # the first's approach, 43 yd to its right
                 (-8123, -9764, 290), (-8823, -10214, 220)]),
        ]),
    # F-144: stock transports that sail or fly the whole way over Open Azeroth's filled-in sea, changing map on
    # Kalimdor's east edge instead of out of sight. Near the docks they keep stock's own nodes (paths 302 and 967),
    # with stock's stop events, which the zeppelin masters' lines and world states hang on.
    # The Thundercaller: Orgrimmar's tower out south as stock, north-east over the sea to cross at x ~4030, south-west
    # over the sea to Tirisfal and into Undercity's tower as stock; back out north, crossing at x ~3880. Both crossings
    # stay in x 3733..4188: north of the Lost Isles band, and south of Northrend's south-east corner (EK x 4188, the
    # bridge's NR_EK corner), whose map the Eastern Kingdoms' edge lies under from there to 5661.
    "thundercaller": dict(
        tag="F-144", path=14401, stock=164871, display=3031, speed=30, seamless="east",
        name="The Thundercaller", where="Orgrimmar, Durotar and Undercity, Tirisfal Glades (zeppelin, Horde)",
        legs=[
            (1, [(1309.9, -4707.4, 71.1), ("stop", 1318.1, -4658.0, 71.9, None, 15318, 15319),
                 (1295.4, -4555.8, 71.1), (1263.5, -4536.3, 71.1), (1223.9, -4564.3, 71.1), (1218.9, -4625.0, 71.1),
                 (1238.7, -4700.3, 71.1), (1255.5, -4831.2, 71.1), (1267.8, -4961.9, 71.1), (1268.5, -5140.1, 71.1),
                 (1500, -5600, 150), (2800, -7000, 250), (3900, -9000, 250)]),
            (0, [(4000, 11800, 250), (3700, 10800, 250), (3200, 7500, 250), (2500, 3000, 220),
                 (2123.6, 1023.4, 153.5), (2009.4, 784.2, 153.9), (1978.6, 626.8, 153.8), (1974.9, 484.1, 148.3),
                 (1988.0, 342.5, 128.6), ("stop", 2062.4, 293.0, 115.0, None, 15320, 15321),
                 (2201.3, 283.7, 121.0), (2437.4, 270.8, 142.7), (2632.6, 366.0, 142.7),
                 (2900, 900, 200), (3300, 4000, 240), (3700, 10000, 250), (3850, 11400, 250)]),
            (1, [(3800, -9100, 250), (3000, -7200, 250), (1900, -5900, 180),
                 (1336.8, -5170.1, 71.1), (1277.2, -4934.8, 71.1), (1297.9, -4773.1, 71.1)]),
        ]),
    # The Bravery: Auberdine out north as stock, past Teldrassil and north-east to cross at x ~11400 into Northrend's
    # southern sea, where Northrend's map begins to lie over Kalimdor's, east along it well south of the Howling Fjord (NR x ~-1100), out of Northrend's
    # east edge at EK x ~6200 and south down the Eastern Kingdoms' west coast to Stormwind Harbor, arriving from the
    # south as stock. Back out north-west, into Northrend at EK x ~6000, west along a lane further south (NR x ~-1500),
    # back to Kalimdor at x ~11200 and round Teldrassil into Auberdine from the south.
    "bravery": dict(
        tag="F-144", path=14400, stock=176310, display=3015, speed=30, seamless="northrend", boat=True,
        name="The Bravery", where="Auberdine, Darkshore and Stormwind Harbor (boat, Alliance)",
        legs=[
            (1, [(6376.5, 757.7, 0), ("stop", 6406.0, 822.9, 0, None, 19031, 0), (6417.2, 894.2, 0),
                 (6700, 1300, 0), (7400, 1550, 0), (8200, 1000, 0), (8700, -200, 0), (9500, -1500, 0),
                 (10700, -3800, 0), (11500, -6500, 0), (11500, -8000, 0)]),
            (571, [(700, 9400, 0), (-300, 7000, 0), (-1000, 4000, 0), (-1150, 0, 0), (-1100, -4500, 0),
                   (-1000, -7500, 0)]),
            (0, [(6000, 11400, 0), (3500, 10600, 0), (1000, 10000, 0), (-2500, 9200, 0), (-6000, 7000, 0),
                 (-8500, 3800, 0), (-9300, 2300, 0), (-9064.9, 1516.2, 0), (-9020.9, 1430.2, 0),
                 (-8961.5, 1355.4, 0), (-8864.2, 1311.8, 0), (-8746.2, 1310.6, 0),
                 ("stop", -8650.7, 1346.1, 0, None, 19030, 0), (-8588.9, 1379.8, 0), (-8547.5, 1420.1, 0),
                 (-8520.6, 1496.6, 0), (-8544.2, 1636.5, 0), (-7800, 3000, 0), (-5500, 6600, 0), (-2000, 8700, 0),
                 (1500, 10500, 0), (4500, 11700, 0), (6200, 12300, 0)]),
            (571, [(-1300, -7300, 0), (-1500, -4500, 0), (-1550, 0, 0), (-1400, 4000, 0), (-600, 7200, 0),
                   (650, 9700, 0)]),
            (1, [(11300, -8100, 0), (11100, -6500, 0), (10300, -4000, 0), (9000, -2200, 0), (8500, -300, 0),
                 (8000, 1200, 0), (7200, 1900, 0), (6300, 1500, 0), (5700, 1000, 0),
                 (5981.2, 845.2, 0), (6077.5, 747.0, 0), (6189.7, 701.4, 0), (6298.7, 698.1, 0)]),
        ]),
}
MAP_DIRS = {0: ("Azeroth", ("patch-OA-maps.MPQ", "patch-OA-ocean.MPQ")),
            1: ("Kalimdor", ("patch-OA-maps.MPQ", "patch-OA-ocean.MPQ")),
            571: ("Northrend", ("lichking.MPQ",)),
            870: ("HawaiiMainland", ("patch-MoP-Pandaria.MPQ",))}
DRAFT = 4.0     # yards of sea a boat needs under its z
# continent_bridge.lua's edges, as seamless routes cross them. A chain lists the maps in order along Kalimdor's frame:
# (map, (dx, dy) that turns the map's coordinates into Kalimdor's, the frame's y below which the next map starts, the
# frame's x ranges a crossing into the next map must lie in, so it crosses where the lua does).
KAL_EAST_Y, EK_WEST_Y, NR_EAST_Y = -9773.0, 12615.0, -8036.0
NR_KAL = (10528.0, -19912.0)    # Kalimdor = Northrend + NR_KAL (the lua's NR_KAL_DX, NR_KAL_DY)
NR_EK = (7120.0, 20443.0)       # the Eastern Kingdoms = Northrend + NR_EK (NR_EK_DX, NR_EK_DY)
NR_TILES_Y = 11200.0            # Northrend's westmost tiles end here (column 11)
CHAINS = {
    # Kalimdor's east edge is the Eastern Kingdoms' west edge, x for x. Not across the Kezan / Lost Isles bands, where
    # the lua moves Kalimdor's edge out, nor north of 4188: the lua sends the Eastern Kingdoms' edge to Northrend only
    # from 5661, but Northrend's map (its south-east corner, the lua's NR_EK corner) already lies over it from 4188
    "east": [(1, (0.0, 0.0), KAL_EAST_Y, [(3733, 4188), (-7466, -1600)]),
             (0, (0.0, KAL_EAST_Y - EK_WEST_Y), None, None)],
    # Kalimdor's east edge north of 11037 leads to Northrend, whose east edge leads to the Eastern Kingdoms' west edge
    # north of 5661. Kalimdor hands over to Northrend before its edge, where Northrend's map begins to lie over it: 50
    # yards inside Northrend's tiles (y 11200 on its map), as the lua's SAFETY_MARGIN
    "northrend": [(1, (0.0, 0.0), NR_TILES_Y - 50 + NR_KAL[1], [(11037, 16994)]),
                  (571, NR_KAL, NR_EAST_Y + NR_KAL[1], [(5661 - NR_EK[0] + NR_KAL[0], 16985 - NR_EK[0] + NR_KAL[0])]),
                  (0, (NR_KAL[0] - NR_EK[0], NR_KAL[1] - NR_EK[1]), None, None)],
}


class Ground:
    def __init__(self):
        self.archives, self.tiles = {}, {}

    def read(self, arc, path):
        if arc not in self.archives:
            self.archives[arc] = Archive(os.path.join(tp.DATA, arc))
        try:
            return self.archives[arc].read(path)
        except Exception:       # mpq_unpack trips over some files it doesn't hold
            return None

    def at(self, m, x, y, raw=False):
        """Terrain height, water as 0; raw: the sea floor instead, -1000 where no tile is (open sea)."""
        name, arcs = MAP_DIRS[m]
        tx, ty = int(32 - y / ab.TILE), int(32 - x / ab.TILE)
        if (m, tx, ty) not in self.tiles:
            path = "World\\Maps\\%s\\%s_%d_%d.adt" % (name, name, tx, ty)
            d = next((d for d in (self.read(a, path) for a in arcs + ("patch-3.mpq",)) if d), None)
            self.tiles[(m, tx, ty)] = ab.Terrain(d, tx, ty) if d else None
        t = self.tiles[(m, tx, ty)]
        if raw:
            return t.at(x, y) if t else -1000.0
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


def control(wps, half, deck):
    """A leg's control points and its stops ({index: (arrival event, departure event)})."""
    ctrl, stops = [], {}
    for w in wps:
        if w[0] == "berth":
            _, x, y, z, heading, side = w[:6]
            a = math.radians(heading + 90 * side)      # out from the dock, away from the flank facing it
            ctrl.append((x + half * math.cos(a), y + half * math.sin(a), z - deck))
            stops[len(ctrl) - 1] = tuple(w[6:8]) or (0, 0)
        elif w[0] == "stop":
            # the transport's own origin at a tower berth, moving along heading: level guide points LEAD yards
            # either side make the curve pass straight through, so the hull lies along the berth
            _, x, y, z, heading = w[:5]
            h = None if heading is None else math.radians(heading)
            if h is not None:
                ctrl.append((x - LEAD * math.cos(h), y - LEAD * math.sin(h), z))
            ctrl.append((float(x), float(y), float(z)))
            stops[len(ctrl) - 1] = tuple(w[5:7]) or (0, 0)
            if h is not None:
                ctrl.append((x + LEAD * math.cos(h), y + LEAD * math.sin(h), z))
        else:
            ctrl.append(tuple(map(float, w)))
    return ctrl, stops


def build(name, out_dir):
    r = ROUTES[name]
    half, deck = HULLS.get(r["display"], (0.0, 0.0))
    chain = CHAINS[r["seamless"]] if r.get("seamless") else None

    def band(p):        # a point in Kalimdor's frame -> its index in the chain
        return next(i for i, (_, _, below, _) in enumerate(chain) if below is None or p[1] >= below)

    def on(p):          # a point in Kalimdor's frame -> (map, point on that map)
        m, (dx, dy), _, _ = chain[band(p)]
        return m, (p[0] - dx, p[1] - dy, p[2])

    legs = []           # (map, control points, stops), in Kalimdor's frame when seamless
    for m, wps in r["legs"]:
        ctrl, stops = control(wps, half, deck)
        if chain:
            k = next(i for i, c in enumerate(chain) if c[0] == m)
            dx, dy = chain[k][1]
            ctrl = [(x + dx, y + dy, z) for x, y, z in ctrl]
            bad = [on(p)[1] for p in ctrl if band(p) != k]
            assert not bad, "map %d waypoints outside its part of the route: %s" % (m, bad)
        legs.append((m, ctrl, stops))
    if r.get("seamless"):
        ctrl, stops = [], {}
        for _, c, s in legs:
            stops.update({len(ctrl) + i: e for i, e in s.items()})
            ctrl += c
        legs = [(None, ctrl, stops)]
    if legs[0][0] == legs[-1][0] and 1 in legs[0][2]:
        # starting on a stop: close the loop as stock's single-map boats do (path 303): end on a copy of the first
        # three points (the stop and one either side). AzerothCore drops a path's first and last node (spline guides)
        # and teleports from the last kept node to the first, here from the stop to itself; each copy waits half
        m, ctrl, stops = legs[-1]
        stops = {**stops, len(ctrl) + 1: legs[0][2][1]}
        legs[-1] = (m, ctrl + legs[0][1][:3], stops)
        r["closed"] = True
    ground, rows, clashes = Ground(), [], []        # rows: (map, point, stop events or None)

    for m, ctrl, stops in legs:
        pts = catmull(ctrl, SPACING)
        stop_at = {ctrl[i]: e for i, e in stops.items()}
        if m is not None:
            rows += [(m, p, stop_at.get(p)) for p in pts]
            continue
        # seamless: split the curve on the edge. Around a crossing c between points a and p the path runs a, c, p on
        # the old map and a, c, p on the new one. AzerothCore drops the last node before a map change and the first
        # after it (they only shape the curve, as at the path's ends) and teleports from c to c
        # A sample closer than SPACING / 4 to c is left out, so no segment next to the crossing is nearly empty.
        skip = None
        for i, p in enumerate(pts):
            a = pts[i - 1] if i else None
            if a is not None and band(a) != band(p):
                ka, kb = band(a), band(p)
                assert abs(ka - kb) == 1, "the curve skips a map between %s and %s" % (a, p)
                line, xs = chain[min(ka, kb)][2:]
                t = (line - a[1]) / (p[1] - a[1])
                c = tuple(u + t * (v - u) for u, v in zip(a, p))
                assert any(lo <= c[0] <= hi for lo, hi in xs), "crossing at x %.0f, outside %s" % (c[0], xs)
                if math.dist(a, c) < SPACING / 4 and stop_at.get(a) is None:
                    rows.pop()
                    a = pts[i - 2]
                after = p
                if math.dist(c, p) < SPACING / 4 and stop_at.get(p) is None and i + 1 < len(pts):
                    after, skip = pts[i + 1], i
                for k, q in ((ka, c), (ka, after), (kb, a), (kb, c)):
                    m, (dx, dy), _, _ = chain[k]
                    rows.append((m, (q[0] - dx, q[1] - dy, q[2]), None))
            if i != skip:
                rows.append(on(p) + (stop_at.get(p),))
    for m, p, _ in rows:
        g = ground.at(m, p[0], p[1], raw=r.get("boat", False))
        if (g > p[2] - DRAFT) if r.get("boat") else (p[2] < g + 2):
            clashes.append((m, round(p[0]), round(p[1]), round(p[2]), round(g)))
    tag, pid = r["tag"], r["path"]
    copies = {}
    for i, (_, p, e) in enumerate(rows):
        if e is not None:
            copies.setdefault(p, []).append(i)
    node = []
    for i, (m, p, e) in enumerate(rows):
        delay = arr = dep = 0
        if e is not None:
            c = copies[p]
            delay = STOP_DELAY // len(c)
            arr = e[0] if i == c[-1] else 0         # a closing stop: arrive on its last copy, leave from its first
            dep = e[1] if i == c[0] else 0
        node.append("  (@TaxiPathNodeID := @TaxiPathNodeID + 1, %d, %d, %d, %.2f, %.2f, %.2f, %d, %d, %d, %d)"
                    % (pid, i, m, p[0], p[1], p[2], 2 if e is not None else 0, delay, arr, dep))
    head = "-- %s: %s. Generated by tools/races/airship_routes.py %s: change the script, not this file." % (
        r["name"], r["where"], name)
    dbc = [head, "",
           "DELETE FROM `taxipath` WHERE `id` = %d;" % pid,
           "INSERT INTO `taxipath` (`id`, `from_taxi_node`, `to_taxi_node`, `cost`) VALUES (%d, 0, 0, 0);" % pid, "",
           "DELETE FROM `taxipathnode` WHERE `path_id` = %d;" % pid,
           "SET @TaxiPathNodeID = (SELECT COALESCE(MAX(id), 0) FROM `taxipathnode`);",
           "INSERT INTO `taxipathnode` (`id`, `path_id`, `node_index`, `map`, `x`, `y`, `z`, `flags`, `delay`, "
           "`arrival_event_id`, `departure_event_id`) VALUES", ",\n".join(node) + ";"]
    if r.get("stock"):
        world = [head, "", "UPDATE `gameobject_template` SET `Data0` = %d WHERE `entry` = %d;" % (pid, r["stock"])]
    else:
        world = [head, "",
                 "DELETE FROM `gameobject_template` WHERE `entry` = %d;" % r["entry"],
                 "INSERT INTO `gameobject_template` (`entry`, `type`, `displayId`, `name`, `IconName`, "
                 "`castBarCaption`, `unk1`, `size`, `Data0`, `Data1`, `Data2`, `Data3`, `Data4`, `Data5`, `Data6`, "
                 "`Data7`, `Data8`, `Data9`, `Data10`, `Data11`, `Data12`, `Data13`, `Data14`, `Data15`, `Data16`, "
                 "`Data17`, `Data18`, `Data19`, `Data20`, `Data21`, `Data22`, `Data23`, `AIName`, `ScriptName`, "
                 "`VerifiedBuild`) VALUES",
                 "  (%d, 15, %d, '%s', '', '', '', 1, %d, %d, %d, 0, 0, 0, 0%s, '', '', 0);"
                 % (r["entry"], r["display"], r["name"].replace("'", "''"), pid, r["speed"], r["accel"], ", 0" * 17),
                 "",
                 "DELETE FROM `gameobject_template_addon` WHERE `entry` = %d;" % r["entry"],
                 "INSERT INTO `gameobject_template_addon` (`entry`, `faction`, `flags`) VALUES (%d, 0, 40);"
                 % r["entry"], "",
                 "DELETE FROM `transports` WHERE `guid` = %d;" % r["guid"],
                 "INSERT INTO `transports` (`guid`, `entry`, `name`, `ScriptName`) VALUES (%d, %d, '%s', '');"
                 % (r["guid"], r["entry"], r["where"].replace("'", "''"))]
    for sub, fname, text in (("dbc", "[%s]_%s_path.sql" % (tag, name), dbc),
                             (os.path.join("sql", "db-world", "base"), "[%s]_%s_transport.sql" % (tag, name), world)):
        os.makedirs(os.path.join(out_dir, sub), exist_ok=True)
        open(os.path.join(out_dir, sub, fname), "w", encoding="utf-8", newline="\n").write("\n".join(text) + "\n")
    length = sum(math.dist(a[1], b[1]) for a, b in zip(rows, rows[1:]) if a[0] == b[0])
    print("%s: %d points over maps %s, %d stops, %.1f km a lap (~%.0f min at %d yd/s, plus stops); hull below the "
          "terrain at %d points%s" % (
              name, len(rows), sorted({m for m, _, _ in rows}), len(copies), length / 1000,
              length / r["speed"] / 60, r["speed"], len(clashes),
              "".join("\n  map %d (%d, %d) bottom %d, ground %d" % c for c in clashes[:20])))

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ROUTES:
        sys.exit(__doc__ + "\nroutes: " + ", ".join(ROUTES))
    build(sys.argv[1], sys.argv[2])
