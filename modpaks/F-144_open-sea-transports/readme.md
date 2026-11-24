# mod-worgoblin-high-elf
## F-144_open-sea-transports

### Features
- Stock transports between continents sail or fly the whole way over the sea. Each one changes map where
  `lua_scripts/open-azeroth/continent_bridge.lua` moves players, at the same spot on both maps. It no longer sails out
  of sight and reappears near the other coast
- All nine stock transports that changed map do, each on a new taxi path. Lap times include the stops:

  | Transport | Gameobject | Path | Route | Maps | Crossings | Lap |
  | --- | --- | --- | --- | --- | --- | --- |
  | The Bravery (boat) | 176310 | 14400 | Auberdine – Stormwind Harbor | Kalimdor, Northrend, EK | Kalimdor x ~11450 / ~810 NR; EK x ~6010 / ~6070 | 109.1 km, ~63 min |
  | The Thundercaller (zeppelin) | 164871 | 14401 | Orgrimmar – Undercity | Kalimdor, EK | x ~4035 / ~3880 | 38.1 km, ~24 min |
  | The Lady Mehley (boat) | 176231 | 14402 | Menethil Harbor – Theramore | Kalimdor, EK | x ~-4000 / ~-4290 | 37.6 km, ~23 min |
  | The Maiden's Fancy (boat) | 20808 | 14403 | Booty Bay – Ratchet | Kalimdor, EK | x ~-13490 / ~-13000 | 53.7 km, ~32 min |
  | The Iron Eagle (zeppelin) | 175080 | 14404 | Orgrimmar – Grom'gol | Kalimdor, EK | x ~-2140 / ~-2590 | 47.6 km, ~29 min |
  | Northspear (boat) | 181688 | 14405 | Menethil Harbor – Valgarde | EK, Northrend | EK x ~6900 / ~7045 | 50.2 km, ~58 min |
  | The Kraken (boat) | 190536 | 14406 | Stormwind Harbor – Valiance Keep | EK, Northrend | EK x ~6545 / ~6680 | 69.5 km, ~57 min |
  | Cloudkisser (zeppelin) | 181689 | 14407 | Undercity – Vengeance Landing | EK, Northrend | EK x ~7295 / ~7070 | 33.6 km, ~21 min |
  | The Mighty Wind (zeppelin) | 186238 | 14408 | Orgrimmar – Warsong Hold | Kalimdor, Northrend | Kalimdor x ~11585 / ~660 NR | 37.0 km, ~23 min |

- The Northrend routes go through Northrend's southern sea, which the bridge lays over Kalimdor and the Eastern
  Kingdoms, so they cover the whole distance. Kalimdor hands over to Northrend at y −8762, just inside Northrend's map,
  where it begins to lie over Kalimdor's
- Near the docks the paths keep stock's own nodes and events (at stops, and the Iron Eagle's and The Kraken's on the
  way in), so the zeppelin masters' lines and the world states that hang on them still work. Each stop still lasts one
  minute. Speeds are stock (Northspear 15 yards a second, The Kraken 21, the rest 30)
- `.tele` targets for The Bravery's and The Thundercaller's stops: AuberdineDock, StormwindDock, OrgrimmarZeppelin and
  UndercityZeppelin (stock's DurotarZeppelin and TirisfalGladesZeppelin reach the same towers)
- Made by `tools/races/airship_routes.py <route>` (routes named after the transports: `bravery`, `thundercaller`,
  `lady_mehley`, `maidens_fancy`, `iron_eagle`, `northspear`, `kraken`, `cloudkisser`, `mighty_wind`). Change the
  script, not the files

### Lanes and meetings
- Transports don't collide in the core: where two are at the same spot they pass through each other, and a passenger
  could step onto the other's deck. All of them start their laps when the server starts, so where they meet depends on
  uptime only
- Boat lanes that both reach Northrend nest instead of crossing: from the open sea in, The Bravery, The Kraken,
  Northspear, in the same order at the Eastern Kingdoms' edge and in Northrend's southern sea (NR x ~−2000, ~−1400
  and the Howling Fjord). Zeppelins keep heights apart where their lanes cross: The Iron Eagle 100-180, The
  Thundercaller 250-270, F-142's Kezan zeppelins 280-400, Cloudkisser and The Mighty Wind 330
- `python -I tools/races/airship_routes.py --check` simulates every transport for a week of uptime and lists the
  pairs that come within 100 yards across and 60 up or down. In this version, per week:
  - The Lady Mehley has to cross The Kraken's and The Bravery's lanes in the Eastern Kingdoms (8 and 4 meetings) and
    The Maiden's Fancy's off Theramore (10). Menethil to the open sea passes those lanes whichever way it goes
  - Around Orgrimmar's tower and Bladefist Bay's (F-142, 250 yards apart): The Thundercaller meets F-142's Kezan
    zeppelins 22 times, and The Iron Eagle 7 times, mostly on stock's own nodes by the tower. F-142's two zeppelins
    meet each other 29 times
  - At shared harbours and towers (Stormwind, Menethil, Undercity, Orgrimmar) a few more, on stock's berths and nodes
  - The timing follows the core's only roughly, so these are how often and where, not to the second

### Requirements
- F-010_patch-open-azeroth, and Open Azeroth's sea tiles on both continents (its ocean patch, patch-OAOcean) on the
  client. Northrend's own tiles already cover its southern sea
- The realm's client DBCs: the paths are TaxiPathNode rows, which the client animates transports from

### Considerations
- The seven transports after the first two are untested in game. The Bravery's direct route and The Thundercaller ran
  in game before their lanes moved
- Crossing an edge is still a map change, with a loading screen for passengers (two a lap, four on The Bravery). The
  transport doesn't jump: it leaves one map and arrives on the other at the same spot
- Clients that met these transports before keep the stock path id in `Cache\WDB\<locale>\gameobjectcache.wdb`. They
  animate the stock path against the new lap time, so the ship stops on screen while the server's sails on. Deleting
  that file fixes it
- One transport per route, as stock, so passengers wait up to a whole lap between departures. A faster speed
  (gameobject_template `Data1`) or a second transport would shorten it
- The crossings stay where continent_bridge.lua's edges agree: Kalimdor to Northrend north of x 11037, Northrend to
  the Eastern Kingdoms north of EK x 5661, and Kalimdor straight to the Eastern Kingdoms at x 3733–4188, −7466–−1600
  or south of −12800. That keeps away from the Kezan and Lost Isles bands, where the lua moves Kalimdor's edge out,
  and from EK x 4188–5661, which the lua links straight to Kalimdor although Northrend's map already lies over it
- The Thundercaller passes Bladefist Bay's tower (F-142) high, out at 140-200 and in at 160, where stock's path ran at
  71, through the tower
- Northspear's stock nodes up the Howling Fjord to Valgarde sample as land in the route tool (ground up to 215); they
  are stock's own, left as they are
- Turning the modpak off needs the world database's stock `Data0` back: 967 (176310), 302 (164871), 292 (176231), 241
  (20808), 285 (175080), 964 (181688), 965 (190536), 737 (181689), 712 (186238)
- Not with F-076's `[F-076]_vanilla_transports.sql`, which points The Bravery at its pre-WotLK path to Menethil Harbor:
  whichever runs later wins, and F-076 runs later in the manifest
