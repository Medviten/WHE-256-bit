#!/usr/bin/env python3
"""Transport routes (gunships, ferries) as DBC and world SQL, from a few waypoints per map.

  python -I airship_routes.py ROUTE MODPAK_DIR
  python -I airship_routes.py --check

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
import bisect, math, os, sys

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
                 # stock's way out south, but climbing over Bladefist Bay's tower (F-142), which stood in it at 71
                 (1238.7, -4700.3, 90), (1255.5, -4831.2, 140), (1267.8, -4961.9, 170), (1268.5, -5140.1, 200),
                 (1500, -5600, 270), (2100, -6300, 270), (2800, -7000, 250), (3900, -9000, 250)]),
            (0, [(4000, 11800, 250), (3700, 10800, 250), (3200, 7500, 250), (2500, 3000, 220),
                 (2123.6, 1023.4, 153.5), (2009.4, 784.2, 153.9), (1978.6, 626.8, 153.8), (1974.9, 484.1, 148.3),
                 (1988.0, 342.5, 128.6), ("stop", 2062.4, 293.0, 115.0, None, 15320, 15321),
                 (2201.3, 283.7, 121.0), (2437.4, 270.8, 142.7), (2632.6, 366.0, 142.7),
                 (2900, 900, 200), (3300, 4000, 240), (3700, 10000, 250), (3850, 11400, 250)]),
            (1, [(3800, -9100, 250), (3000, -7200, 250), (1900, -5900, 180),
                 # stock's way in from the south, high over Bladefist Bay's tower
                 (1336.8, -5170.1, 190), (1277.2, -4934.8, 160), (1297.9, -4773.1, 100)]),
        ]),
    # The Bravery: Auberdine out north as stock, past Teldrassil and north-east to cross at x ~11450 into Northrend's
    # southern sea, where Northrend's map begins to lie over Kalimdor's, east along it outside the other boats' lanes
    # (NR x ~-1950), out of Northrend's east edge at EK x ~6070 and south down the Eastern Kingdoms' west coast, the
    # outermost lane, to Stormwind Harbor, arriving from the south as stock. Back out west, into Northrend at EK x
    # ~6010, west along NR x ~-2350, back to Kalimdor at NR x ~810 and round Teldrassil into Auberdine from the south.
    "bravery": dict(
        tag="F-144", path=14400, stock=176310, display=3015, speed=30, seamless="northrend", boat=True,
        name="The Bravery", where="Auberdine, Darkshore and Stormwind Harbor (boat, Alliance)",
        legs=[
            (1, [(6376.5, 757.7, 0), ("stop", 6406.0, 822.9, 0, None, 19031, 0), (6417.2, 894.2, 0),
                 (6700, 1300, 0), (7400, 1550, 0), (8200, 1000, 0), (8700, -200, 0), (9500, -1500, 0),
                 (10700, -3800, 0), (11500, -6500, 0), (11500, -8000, 0)]),
            (571, [(700, 9400, 0), (-600, 7000, 0), (-1700, 4000, 0), (-1950, 0, 0), (-1950, -4500, 0),
                   (-1950, -6500, 0), (-1150, -7700, 0)]),
            (0, [(5900, 11400, 0), (3500, 10600, 0), (1000, 10000, 0), (-2500, 9200, 0), (-6000, 7000, 0),
                 (-8500, 3800, 0), (-9300, 2300, 0), (-9064.9, 1516.2, 0), (-9020.9, 1430.2, 0),
                 (-8961.5, 1355.4, 0), (-8864.2, 1311.8, 0), (-8746.2, 1310.6, 0),
                 ("stop", -8650.7, 1346.1, 0, None, 19030, 0), (-8588.9, 1379.8, 0), (-8547.5, 1420.1, 0),
                 (-8520.6, 1496.6, 0), (-8544.2, 1636.5, 0), (-8800, 3200, 0), (-5500, 6600, 0), (-2000, 8700, 0),
                 (1500, 10500, 0), (4500, 11700, 0), (5900, 12300, 0)]),
            (571, [(-1250, -7600, 0), (-2350, -6000, 0), (-2350, -3000, 0), (-2300, 0, 0), (-2100, 4000, 0),
                   (-1000, 7200, 0), (650, 9700, 0)]),
            (1, [(11300, -8100, 0), (11100, -6500, 0), (10300, -4000, 0), (9000, -2200, 0), (8500, -300, 0),
                 (8000, 1200, 0), (7200, 1900, 0), (6300, 1500, 0), (5700, 1000, 0),
                 (5981.2, 845.2, 0), (6077.5, 747.0, 0), (6189.7, 701.4, 0), (6298.7, 698.1, 0)]),
        ]),
    # The other stock transports between continents, laid out so their lanes cross as little as the map allows. Lanes
    # of boats that both reach Northrend nest: from the open sea in, The Bravery, The Kraken, Northspear, the same at
    # the Eastern Kingdoms' edge (x ~5950 / 6450 / 6850) and in Northrend's southern sea (NR x ~-2000 / -1400 / the
    # Howling Fjord). The Lady Mehley has to cross The Bravery's and The Kraken's lanes, and The Maiden's Fancy hers on
    # Kalimdor's side; --check counts how often they meet there. Zeppelins keep heights apart: The Iron Eagle 180,
    # The Thundercaller 250, F-142's Kezan zeppelins 280-400, Cloudkisser and The Mighty Wind 330 (far apart).
    # The Lady Mehley: Theramore out east as stock, crossing at x ~-4000, east along x -4000 to Menethil from the west
    # as stock; back by x -4400, crossing at x ~-4300, into Theramore from the south.
    "lady_mehley": dict(
        tag="F-144", path=14402, stock=176231, display=3015, speed=30, seamless="east", boat=True,
        name="The Lady Mehley", where="Menethil Harbor, Wetlands and Theramore Isle, Dustwallow Marsh (boat, Alliance)",
        legs=[
            (1, [(-4100.9, -4692.4, 0), ("stop", -4016.4, -4740.6, 0, None, 10302, 0), (-3952.5, -4813.7, 0),
                 (-3910.8, -4899.6, 0), (-3886.0, -5039.0, 0), (-3867.7, -5226.8, 0), (-3900, -7000, 0),
                 (-4000, -9000, 0)]),
            (0, [(-4000, 12000, 0), (-4000, 8000, 0), (-3950, 3000, 0), (-4000, 700, 0), (-4060, 120, 0),
                 (-4199.2, -132.8, 0), (-4199.9, -372.3, 0),
                 (-4150.9, -531.3, 0), (-4088.9, -599.1, 0), (-3996.3, -611.3, 0),
                 ("stop", -3905.2, -585.8, 0, None, 10301, 0), (-3832.4, -521.3, 0), (-3801.9, -383.6, 0),
                 (-3893.9, -245.6, 0), (-3780, 600, 0), (-3850, 1600, 0), (-4300, 3500, 0), (-4350, 8000, 0),
                 (-4300, 12000, 0)]),
            (1, [(-4300, -9000, 0), (-4400, -7000, 0), (-4399.1, -5099.7, 0), (-4263.5, -4823.3, 0),
                 (-4201.2, -4718.7, 0)]),
        ]),
    # The Maiden's Fancy: Ratchet out as stock, south along Kalimdor's east coast past Tanaris, crossing south of the
    # Kezan band (x ~-13350), east to Booty Bay from the west as stock; back by a lane further north, crossing at x
    # ~-12930, into Ratchet from the south.
    "maidens_fancy": dict(
        tag="F-144", path=14403, stock=20808, display=3015, speed=30, seamless="east", boat=True,
        name="The Maiden's Fancy", where="Booty Bay, Stranglethorn Vale and Ratchet, The Barrens (boat, neutral)",
        legs=[
            (1, [(-1058.5, -3818.9, 0), ("stop", -1005.6, -3841.6, 0, None, 16398, 0), (-956.4, -3877.1, 0),
                 (-935.5, -3917.8, 0), (-950.2, -3981.3, 0), (-1037.7, -4093.1, 0), (-1149.6, -4232.9, 0),
                 (-2000, -5500, 0), (-5000, -6200, 0), (-9000, -7300, 0), (-11000, -7600, 0), (-13300, -9400, 0)]),
            (0, [(-13450, 12000, 0), (-13800, 8000, 0), (-14300, 4000, 0), (-14500, 2000, 0), (-14338.3, 1081.1, 0),
                 (-14366.7, 867.3, 0), (-14351.3, 733.7, 0), (-14342.5, 635.4, 0),
                 ("stop", -14277.7, 582.9, 0, None, 16397, 0), (-14171.9, 578.4, 0), (-14088.3, 626.5, 0),
                 (-14052.8, 732.2, 0), (-14122.9, 852.5, 0), (-13900, 2000, 0), (-13500, 6000, 0),
                 (-13000, 11000, 0), (-12950, 12300, 0)]),
            (1, [(-12900, -9300, 0), (-11200, -8900, 0), (-8500, -6800, 0), (-5000, -5700, 0), (-4000, -5500, 0),
                 (-3500, -4700, 0), (-2750, -4600, 0), (-1600, -4550, 0),
                 (-1370.2, -4266.7, 0), (-1264.9, -4139.9, 0), (-1212.5, -4019.7, 0), (-1154.2, -3887.8, 0),
                 (-1105.5, -3824.1, 0)]),
        ]),
    # The Iron Eagle: Orgrimmar's tower out south as stock, south-east over the sea at 180, crossing at x ~-2260, to
    # Grom'gol from the west as stock; back by a lane further north, crossing at x ~-2750, into Orgrimmar's tower from
    # the south as stock but further west, clear of Bladefist Bay's tower (F-142), with stock's approach event.
    "iron_eagle": dict(
        tag="F-144", path=14404, stock=175080, display=3031, speed=30, seamless="east",
        name="The Iron Eagle", where="Grom'gol Base Camp, Stranglethorn Vale and Orgrimmar, Durotar (zeppelin, Horde)",
        legs=[
            (1, [(1299.5, -4508.2, 83.8), ("stop", 1360.9, -4631.3, 71.9, None, 0, 15323), (1468.6, -4755.9, 98.8),
                 (1499.6, -5033.6, 99.0), (1600, -5350, 100), (1650, -5750, 120), (1100, -6500, 140), (-1000, -8500, 180),
                 (-2200, -9500, 180)]),
            (0, [(-2400, 12000, 180), (-6000, 8000, 180), (-10500, 3000, 180), (-12300, 1500, 130),
                 (-12433.1, 866.1, 59.3), (-12442.8, 685.7, 59.3), (-12428.0, 397.4, 53.8),
                 ("stop", -12464.0, 231.6, 49.5, None, 15324, 15325), (-12564.8, 141.6, 59.2), (-12677.8, 177.1, 80.4),
                 (-12730.4, 296.4, 85.3), (-12703.1, 463.6, 85.4), (-12300, 1800, 150), (-10000, 4500, 180),
                 (-6000, 9000, 180), (-2800, 12200, 180)]),
            (1, [(-2700, -9400, 180), (-1200, -8000, 180), (600, -6200, 170), (1000, -5200, 140), (950, -4935, 125),
                 (1000, -4751, 108), (1126.9, -4526.6, 99.0), ("event", 1223.5, -4465.4, 95.4, 15322, 0)]),
        ]),
    # Northspear: Menethil out north as stock, north up the Eastern Kingdoms' coast inside The Kraken's lanes, into
    # Northrend at EK x ~6850, west into the Howling Fjord's mouth and up to Valgarde along stock's own nodes; back
    # out of the fjord, into the Eastern Kingdoms at EK x ~7010 and south down the coast into Menethil as stock.
    "northspear": dict(
        tag="F-144", path=14405, stock=181688, display=7446, speed=15, seamless="northrend", boat=True,
        name="Northspear", where="Menethil Harbor, Wetlands and Valgarde, Howling Fjord (boat, Alliance)",
        legs=[
            (0, [(-3661.6, -640.4, 0), ("stop", -3712.7, -569.5, 0, None, 19124, 0), (-3759.4, -475.3, 0),
                 (-3735.4, -395.9, 0), (-3617.0, -281.7, 0), (-3425.1, -311.5, 0), (-3246.8, -383.4, 0),
                 (-3200, 500, 0), (-3050, 1800, 0), (-2700, 3200, 0), (-2000, 3500, 0), (0, 3400, 0), (2500, 3500, 0), (4500, 5600, 0), (6200, 9500, 0),
                 (6800, 11800, 0)]),
            (571, [(-200, -7200, 0), (-700, -6500, 0), (-961.5, -5707.9, 0), (-403.7, -5502.0, 0),
                   (-155.5, -5409.4, 0), (-7.8, -5328.6, 0), (61.4, -5204.8, 0), (125.4, -5139.7, 0),
                   (191.8, -5084.8, 0), (262.7, -5086.5, 0), (351.3, -5153.0, 0), (446.3, -5151.4, 0),
                   (520.5, -5171.0, 0), (585.5, -5206.3, 0), (639.3, -5246.7, 0), (692.1, -5291.6, 0),
                   (716.3, -5338.6, 0), (748.6, -5422.9, 0), (799.4, -5462.1, 0), (889.7, -5470.5, 0),
                   (955.5, -5400.4, 0), (983.0, -5321.9, 0), (993.6, -5252.2, 0), (978.4, -5179.0, 0),
                   (907.8, -5136.4, 0), (807.6, -5144.3, 0), (694.5, -5148.1, 0),
                   ("stop", 584.0, -5118.9, 0, None, 19123, 0), (507.2, -5107.5, 0), (433.1, -5142.8, 0),
                   (357.6, -5150.6, 0), (294.4, -5111.4, 0), (236.7, -5080.4, 0), (179.6, -5097.8, 0),
                   (132.0, -5136.0, 0), (72.0, -5198.6, 0), (-3.9, -5315.2, 0), (-151.0, -5416.6, 0),
                   (-400.8, -5508.6, 0), (-1009.9, -5783.0, 0), (-600, -6800, 0), (-100, -7600, 0)]),
            (0, [(7000, 12000, 0), (6900, 11000, 0), (5300, 7000, 0), (2700, 4000, 0), (0, 4000, 0),
                 (-2300, 3900, 0), (-3000, 1500, 0), (-3235.8, -433.8, 0), (-3420.9, -588.0, 0), (-3521.6, -629.1, 0),
                 (-3600.3, -641.8, 0)]),
        ]),
    # The Kraken: Stormwind Harbor out north-west as stock, up the Eastern Kingdoms' coast between The Bravery's lanes
    # and Northspear's, into Northrend at EK x ~6470, west south of the Howling Fjord's mouth and north to Valiance
    # Keep from the south as stock (with stock's event on the way in); back by a lane nearer the coast, into the
    # Eastern Kingdoms at EK x ~6630 and into Stormwind Harbor from the north-west as stock.
    "kraken": dict(
        tag="F-144", path=14406, stock=190536, display=7446, speed=21, seamless="northrend", boat=True,
        name="The Kraken", where="Valiance Keep, Borean Tundra and Stormwind Harbor (boat, Alliance)",
        legs=[
            (0, [(-8397.3, 1434.3, 0), ("stop", -8288.8, 1424.7, 0, None, 19032, 0), (-8160.3, 1431.5, 0),
                 (-8063.5, 1490.7, 0), (-7966.1, 1599.7, 0), (-7746.6, 1867.0, 0), (-7669.4, 2008.0, 0),
                 (-6500, 3600, 0), (-5500, 5000, 0), (-4000, 5600, 0), (-1300, 5600, 0), (1500, 7600, 0), (4000, 9300, 0),
                 (6000, 11300, 0), (6500, 11900, 0)]),
            (571, [(-700, -7200, 0), (-1500, -5700, 0), (-1500, -3000, 0), (-600, 1000, 0), (1300, 3500, 0),
                   (2375.0, 4276.9, 0), (2355.5, 4447.6, 0), (2344.3, 4641.2, 0), ("event", 2315.8, 4792.1, 0, 0, 18613),
                   (2345.3, 4949.2, 0), (2316.9, 5066.6, 0), ("stop", 2218.4, 5119.6, 0, None, 19033, 0),
                   (2133.4, 5154.5, 0), (2043.6, 5170.3, 0), (1918.7, 5123.9, 0), (1784.4, 5060.6, 0),
                   (1573.3, 4856.2, 0), (800, 4000, 0), (-300, 1500, 0), (-1000, -2500, 0), (-1250, -5700, 0),
                   (-480, -7600, 0)]),
            (0, [(6620, 12200, 0), (6300, 11200, 0), (4200, 8800, 0), (1500, 6500, 0), (700, 5500, 0), (-1000, 4800, 0),
                 (-4000, 4400, 0), (-5200, 3300, 0), (-6500, 2900, 0), (-7400, 2600, 0), (-8300, 2400, 0), (-8438.3, 1941.8, 0),
                 (-8467.7, 1657.8, 0), (-8465.4, 1513.0, 0)]),
        ]),
    # Cloudkisser: Undercity's tower out as stock, north-west at 330 over the sea, into Northrend at EK x ~7290, to
    # Vengeance Landing from the east as stock; back into the Eastern Kingdoms at EK x ~7010 and into Undercity's tower
    # from the north-west as stock.
    "cloudkisser": dict(
        tag="F-144", path=14407, stock=181689, display=7546, speed=30, seamless="northrend",
        name="Cloudkisser", where="Undercity, Tirisfal Glades and Vengeance Landing, Howling Fjord (zeppelin, Horde)",
        legs=[
            (0, [(2149.1, 429.6, 102.6), ("stop", 2056.5, 381.6, 100.4, None, 19127, 0), (2005.0, 370.3, 94.2),
                 (1978.1, 410.0, 100.5), (2041.0, 449.2, 100.9), (2091.8, 481.2, 109.9), (2173.6, 534.1, 128.9),
                 (2235.2, 575.6, 141.8), (2700, 700, 250), (3400, 1500, 330), (4500, 6000, 330), (6200, 11000, 330),
                 (7200, 12100, 330)]),
            (571, [(300, -7600, 330), (1500, -7100, 300), (2000, -6650, 120), (1933.1, -6500.4, 86.1),
                   (2065.0, -6331.5, 86.1),
                   (2059.0, -6194.8, 86.1), ("stop", 1989.4, -6082.8, 85.6, None, 19126, 0), (1807.1, -6001.6, 86.2),
                   (1671.7, -6134.8, 82.9), (1200, -6900, 300), (-100, -7700, 330)]),
            (0, [(7000, 11900, 330), (5500, 8000, 330), (3500, 3000, 330), (2700, 1300, 250), (2344.7, 620.8, 140.0),
                 (2306.9, 554.1, 134.1), (2251.1, 504.5, 126.2)]),
        ]),
    # The Mighty Wind: Orgrimmar's north tower out as stock but east and up at once, north at 330 along Kalimdor's
    # east coast, into Northrend at x ~11610, east to Warsong Hold from the west as stock; back by a lane further
    # west, into Kalimdor at NR x ~610 and into the tower from the north as stock.
    "mighty_wind": dict(
        tag="F-144", path=14408, stock=186238, display=7546, speed=30, seamless="northrend",
        name="The Mighty Wind", where="Orgrimmar, Durotar and Warsong Hold, Borean Tundra (zeppelin, Horde)",
        legs=[
            (1, [(1149.0, -3996.8, 112.2), ("stop", 1185.0, -4144.2, 70.6, None, 19137, 0), (1239.8, -4267.0, 67.4),
                 (1400, -4350, 150), (1800, -4300, 250), (2600, -4700, 330), (4500, -6400, 330), (7000, -7600, 330),
                 (9500, -8100, 330), (11400, -8400, 330), (11600, -8650, 330)]),
            (571, [(1100, 10900, 330), (1700, 9000, 300), (2150, 7300, 220), (2306.0, 6748.1, 158.6),
                   (2474.4, 6598.2, 158.7), (2666.8, 6376.8, 158.6), (2763.9, 6260.4, 148.6),
                   ("stop", 2837.9, 6187.4, 140.2, None, 19139, 0), (2906.0, 6105.2, 152.2), (3003.9, 6002.2, 149.9),
                   (3054.6, 5935.8, 151.8), (3051.7, 5805.3, 151.8), (2936.5, 5669.6, 151.8), (2699.7, 5668.5, 151.8),
                   (2434.1, 5700.3, 151.8), (2199.6, 5934.4, 151.8), (1900, 7000, 250), (1100, 9200, 330),
                   (650, 10900, 330)]),
            (1, [(11100, -8500, 330), (9300, -7700, 330), (6500, -6800, 330), (3800, -5600, 330), (3000, -4400, 330),
                 (2600, -3800, 300), (2000, -3700, 260), (1476.5, -3845.2, 154.4), (1372.0, -3851.5, 154.4), (1202.4, -3891.9, 154.4)]),
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
    "east": [(1, (0.0, 0.0), KAL_EAST_Y, [(3733, 4188), (-7466, -1600), (-16994, -12800)]),
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
    """A leg's control points, its stops ({index: (arrival event, departure event)}) and its events on the move."""
    ctrl, stops, evs = [], {}, {}
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
        elif w[0] == "event":
            # a point the transport passes without stopping, firing stock's (arrival event, departure event) there
            _, x, y, z, arr, dep = w
            ctrl.append((float(x), float(y), float(z)))
            evs[len(ctrl) - 1] = (arr, dep)
        else:
            ctrl.append(tuple(map(float, w)))
    return ctrl, stops, evs


class Row:
    """One TaxiPathNode: map, point, stop events (None when it doesn't stop), events on the move, and whether
    AzerothCore drops it as a spline guide (the path's ends and the nodes either side of a map change)."""
    __slots__ = ("m", "p", "stop", "ev", "guide")

    def __init__(self, m, p, stop=None, ev=None, guide=False):
        self.m, self.p, self.stop, self.ev, self.guide = m, p, stop, ev, guide


def route_rows(name):
    r = ROUTES[name]
    half, deck = HULLS.get(r["display"], (0.0, 0.0))
    chain = CHAINS[r["seamless"]] if r.get("seamless") else None

    def band(p):        # a point in Kalimdor's frame -> its index in the chain
        return next(i for i, (_, _, below, _) in enumerate(chain) if below is None or p[1] >= below)

    def on(p):          # a point in Kalimdor's frame -> (map, point on that map)
        m, (dx, dy), _, _ = chain[band(p)]
        return m, (p[0] - dx, p[1] - dy, p[2])

    legs = []           # (map, control points, stops, events), in Kalimdor's frame when seamless
    for m, wps in r["legs"]:
        ctrl, stops, evs = control(wps, half, deck)
        if chain:
            k = next(i for i, c in enumerate(chain) if c[0] == m)
            dx, dy = chain[k][1]
            ctrl = [(x + dx, y + dy, z) for x, y, z in ctrl]
            bad = [on(p)[1] for p in ctrl if band(p) != k]
            assert not bad, "map %d waypoints outside its part of the route: %s" % (m, bad)
        legs.append((m, ctrl, stops, evs))
    if r.get("seamless"):
        ctrl, stops, evs = [], {}, {}
        for _, c, s, e in legs:
            stops.update({len(ctrl) + i: v for i, v in s.items()})
            evs.update({len(ctrl) + i: v for i, v in e.items()})
            ctrl += c
        legs = [(None, ctrl, stops, evs)]
    if legs[0][0] == legs[-1][0] and 1 in legs[0][2]:
        # starting on a stop: close the loop as stock's single-map boats do (path 303): end on a copy of the first
        # three points (the stop and one either side). AzerothCore drops a path's first and last node (spline guides)
        # and teleports from the last kept node to the first, here from the stop to itself; each copy waits half
        m, ctrl, stops, evs = legs[-1]
        stops = {**stops, len(ctrl) + 1: legs[0][2][1]}
        legs[-1] = (m, ctrl + legs[0][1][:3], stops, evs)
        r["closed"] = True
    rows = []
    for m, ctrl, stops, evs in legs:
        pts = catmull(ctrl, SPACING)
        stop_at = {ctrl[i]: e for i, e in stops.items()}
        ev_at = {ctrl[i]: e for i, e in evs.items()}
        if m is not None:
            rows += [Row(m, p, stop_at.get(p), ev_at.get(p)) for p in pts]
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
                if math.dist(a, c) < SPACING / 4 and a not in stop_at and a not in ev_at:
                    rows.pop()
                    a = pts[i - 2]
                after = p
                if math.dist(c, p) < SPACING / 4 and p not in stop_at and p not in ev_at and i + 1 < len(pts):
                    after, skip = pts[i + 1], i
                for k, q, guide in ((ka, c, False), (ka, after, True), (kb, a, True), (kb, c, False)):
                    m, (dx, dy), _, _ = chain[k]
                    rows.append(Row(m, (q[0] - dx, q[1] - dy, q[2]), guide=guide))
            if i != skip:
                rows.append(Row(*on(p), stop_at.get(p), ev_at.get(p)))
    rows[0].guide = rows[-1].guide = True
    return r, rows


def timetable(r, rows):
    """(lap time, {row index: seconds into the lap}) of the nodes AzerothCore keeps, roughly as it times them: the
    route's speed, a speed / accel ramp at each stop, the stop's delay, no time for a teleport. Time 0 is the first
    kept node, where every transport is when the server starts."""
    speed, accel = float(r["speed"]), float(r.get("accel", 1))
    copies = {}
    for i, row in enumerate(rows):
        if row.stop is not None:
            copies.setdefault(row.p, []).append(i)
    kept = [i for i, row in enumerate(rows) if not row.guide]
    t, times, prev = 0.0, {}, None
    for i in kept:
        row = rows[i]
        if prev is not None and rows[prev].m == row.m:
            t += math.dist(rows[prev].p, row.p) / speed
        times[i] = t
        if row.stop is not None:
            t += STOP_DELAY / len(copies[row.p]) + speed / accel / 2   # half a ramp each side of the stop
        prev = i
    return t, times


def write(name, out_dir):
    r, rows = route_rows(name)
    ground, clashes = Ground(), []
    for row in rows:
        m, p = row.m, row.p
        g = ground.at(m, p[0], p[1], raw=r.get("boat", False))
        if (g > p[2] - DRAFT) if r.get("boat") else (p[2] < g + 2):
            clashes.append((m, round(p[0]), round(p[1]), round(p[2]), round(g)))
    tag, pid = r["tag"], r["path"]
    copies = {}
    for i, row in enumerate(rows):
        if row.stop is not None:
            copies.setdefault(row.p, []).append(i)
    node = []
    for i, row in enumerate(rows):
        m, p, e = row.m, row.p, row.stop
        delay = arr = dep = 0
        if e is not None:
            c = copies[p]
            delay = STOP_DELAY // len(c)
            arr = e[0] if i == c[-1] else 0         # a closing stop: arrive on its last copy, leave from its first
            dep = e[1] if i == c[0] else 0
        elif row.ev:
            arr, dep = row.ev
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
    length = sum(math.dist(a.p, b.p) for a, b in zip(rows, rows[1:]) if a.m == b.m)
    print("%s: %d points over maps %s, %d stops, %.1f km a lap (~%.0f min with stops); hull below the "
          "terrain at %d points%s" % (
              name, len(rows), sorted({row.m for row in rows}), len(copies), length / 1000,
              timetable(r, rows)[0] / 60, len(clashes),
              "".join("\n  map %d (%d, %d) bottom %d, ground %d" % c for c in clashes[:20])))


def keyframes(r, rows):
    """[(seconds into the lap, map, point, docked)] the transport passes, and its lap time: at each kept node's arrival,
    and again at its departure where it stops."""
    lap, times = timetable(r, rows)
    speed, accel = float(r["speed"]), float(r.get("accel", 1))
    copies = {}
    for i, row in enumerate(rows):
        if row.stop is not None:
            copies.setdefault(row.p, []).append(i)
    out = []
    for i, t in sorted(times.items(), key=lambda kv: kv[1]):
        row = rows[i]
        out.append((t, row.m, row.p, row.stop is not None))
        if row.stop is not None:
            out.append((t + STOP_DELAY / len(copies[row.p]) + speed / accel / 2, row.m, row.p, True))
    return out, lap


def where(frames, lap, t):
    """(map, point, docked) at t seconds of uptime, moving straight between keyframes."""
    tm = t % lap
    k = bisect.bisect_right(frames, (tm, 1 << 30)) - 1
    t0, m0, p0, d0 = frames[k]
    t1, m1, p1, d1 = frames[(k + 1) % len(frames)]
    if k + 1 == len(frames):
        t1 += lap
    if m0 != m1 or t1 <= t0:
        return m0, p0, d0
    f = (tm - t0) / (t1 - t0)
    return m0, tuple(a + f * (b - a) for a, b in zip(p0, p1)), d0 and d1


def check(days=7.0, step=2.0):
    """Every pair of transports that come within APART yards across and HULL yards up or down of each other, in DAYS of
    uptime from a server start (all transports start their laps then), sampled every STEP seconds. Each meeting is
    listed once, where they come closest; meetings where one of them is docked are counted apart (stock's berths sit
    side by side on purpose). The timing follows AzerothCore's only roughly, so read the meetings as how often and
    where, not to the second."""
    import array
    sims = {}
    for name in ROUTES:
        if name in OUT_OF_WORLD:
            continue
        r, rows = route_rows(name)
        sims[name] = keyframes(r, rows)
    n = int(days * 86400 / step)
    pos = {}
    for name, (frames, lap) in sims.items():
        ms, xs, ys, zs, ds = array.array('i'), array.array('d'), array.array('d'), array.array('d'), array.array('b')
        for s in range(n):
            m, p, d = where(frames, lap, s * step)
            ms.append(m), xs.append(p[0]), ys.append(p[1]), zs.append(p[2]), ds.append(d)
        pos[name] = (ms, xs, ys, zs, ds)
    names = sorted(sims)
    for ai, a in enumerate(names):
        for b in names[ai + 1:]:
            ma, xa, ya, za, da = pos[a]
            mb, xb, yb, zb, db = pos[b]
            meets, docked, cur = [], 0, None
            for s in range(n):
                close = (ma[s] == mb[s] and abs(za[s] - zb[s]) < HULL
                         and (xa[s] - xb[s]) ** 2 + (ya[s] - yb[s]) ** 2 < APART * APART)
                if close:
                    dist = math.hypot(xa[s] - xb[s], ya[s] - yb[s])
                    if cur is None:
                        cur = [s, dist, s, bool(da[s] or db[s])]
                    elif dist < cur[1]:
                        cur[1], cur[2] = dist, s
                    cur[3] = cur[3] or bool(da[s] or db[s])
                elif cur is not None:
                    if cur[3]:
                        docked += 1
                    else:
                        meets.append(cur)
                    cur = None
            if not meets and not docked:
                continue
            spots = ", ".join("map %d (%d, %d) %d yd after %.1f h" % (
                ma[s], xa[s], ya[s], dist, s * step / 3600) for _, dist, s, _ in meets[:5])
            print("%s / %s: %d meetings under way%s%s; %d more with one of them docked" % (
                a, b, len(meets), ": " if meets else "", spots + (" ..." if len(meets) > 5 else ""), docked))


OUT_OF_WORLD = {"hellscreams_fist"}     # F-133's first cut: its world SQL was taken out (2e533c15)
APART, HULL = 100.0, 60.0               # a ship's or zeppelin's length; a zeppelin's height (56)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        check()
    elif len(sys.argv) != 3 or sys.argv[1] not in ROUTES:
        sys.exit(__doc__ + "\nroutes: " + ", ".join(ROUTES) + "\n  python -I airship_routes.py --check")
    else:
        write(sys.argv[1], sys.argv[2])
