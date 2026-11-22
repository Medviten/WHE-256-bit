# mod-worgoblin-high-elf
## F-144_open-sea-transports

### Features
- Stock transports sail or fly the whole way between Kalimdor and the Eastern Kingdoms over the sea. Each one changes
  map where `lua_scripts/open-azeroth/continent_bridge.lua` moves players, at the same spot on both maps. It no longer
  sails out of sight and reappears near the other coast
- A first test with two transports:
  - **The Bravery** (gameobject 176310), Auberdine – Stormwind Harbor: taxi path 14400
    - Goes through Northrend's southern sea, which the bridge lays over both continents, so it covers the whole
      distance instead of skipping the gap between the two edges
    - Leaves Auberdine northwards, passes Teldrassil and crosses into Northrend at x ~11450, y −8762: just inside
      Northrend's map, where it begins to lie over Kalimdor's, rather than on the bridge's line further east
    - Sails east well south of the Howling Fjord (Northrend x ~−1100) and crosses into the Eastern Kingdoms at x ~6200
    - Sails south down the west coast to Stormwind Harbor, arriving from the south as stock
    - Comes back by a second lane: into Northrend at x ~6250, west along Northrend x ~−1500, into Kalimdor at x ~11325
    - 107.7 km a lap, about 62 minutes with the stops
  - **The Thundercaller** (gameobject 164871), Orgrimmar – Undercity: taxi path 14401
    - Crosses straight from Kalimdor's east edge to the Eastern Kingdoms' west edge
    - Leaves Orgrimmar's tower southwards as stock, flies north-east over the sea and crosses at x ~4030
    - Flies south-west over the sea into Undercity's tower, coming back by a second lane and crossing at x ~3880
    - Both crossings lie south of Northrend's south-east corner (EK x 4188), so it never flies under Northrend's map
    - 38.1 km a lap, about 23 minutes with the stops
- Near the docks the paths keep stock's own nodes and stop events, so the zeppelin masters' lines and the world states
  that hang on them still work. Each stop still lasts one minute. Speeds are stock (30 yards a second)
- `.tele` targets for the stops: AuberdineDock, StormwindDock (The Bravery's piers), OrgrimmarZeppelin and
  UndercityZeppelin (The Thundercaller's berths; stock's DurotarZeppelin and TirisfalGladesZeppelin reach the same)
- Made by `tools/races/airship_routes.py bravery` (`seamless="northrend"`) and `thundercaller` (`seamless="east"`).
  Change the script, not the files

### Requirements
- F-010_patch-open-azeroth, and Open Azeroth's sea tiles on both continents (its ocean patch, patch-OAOcean) on the
  client. Northrend's own tiles already cover its southern sea
- The realm's client DBCs: the paths are TaxiPathNode rows, which the client animates transports from

### Considerations
- Tested in game once, before the Northrend route: The Bravery's direct route ran a whole lap
- Crossing an edge is still a map change, with a loading screen for passengers: The Bravery has four a lap, The
  Thundercaller two. The transport doesn't jump: it leaves one map and arrives on the other at the same spot
- Clients that met these transports before keep the stock path id in `Cache\WDB\<locale>\gameobjectcache.wdb`. They
  animate the stock path against the new lap time, so the ship stops on screen while the server's sails on. Deleting
  that file fixes it
- One transport per route, as stock, so passengers wait up to a whole lap between departures, now about 62 minutes for
  The Bravery. A faster speed (gameobject_template `Data1`) or a second transport would shorten it
- The crossings stay where continent_bridge.lua's edges agree: Kalimdor to Northrend north of x 11037, Northrend to
  the Eastern Kingdoms north of EK x 5661, and Kalimdor straight to the Eastern Kingdoms at x 3733–4188 or
  −7466–−1600. That keeps away from the Kezan and Lost Isles bands, where the lua moves Kalimdor's edge out, and from
  EK x 4188–5661, which the lua links straight to Kalimdor although Northrend's map already lies over it
- Turning the modpak off needs the world database's stock `Data0` back (967 for 176310, 302 for 164871)
- Not with F-076's `[F-076]_vanilla_transports.sql`, which points The Bravery at its pre-WotLK path to Menethil Harbor:
  whichever runs later wins, and F-076 runs later in the manifest
