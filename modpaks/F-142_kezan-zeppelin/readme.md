# mod-worgoblin-high-elf
## F-142_kezan-zeppelin

### Features
- A zeppelin between Bladefist Bay below Orgrimmar and Kezan: taxi path 14200, gameobject 1420002 (the stock
  zeppelin's model, display 3031), transport guid 14202. It leaves Bladefist Bay's zeppelin tower from its west berth,
  goes south over the sea, docks at Kezan's goblin tower in place of the north one of its two static zeppelins, and
  comes back into Bladefist Bay from the east. One minute at each tower
- A goblin elevator in Kezan's zeppelin tower, up the shaft on its east face to the landing by the zeppelins:
  gameobject 1420001 (spawn guid 14200001), Cataclysm's goblin elevator (display 9693, `goblin_elevator.m2`, which
  Open Azeroth's maps ship) with its animation (Cataclysm's gameobject 204246) stretched to this shaft's 39.4 yards
- Made by `tools/races/airship_routes.py kezan_zeppelin` (the route) and `tools/races/kezan_elevator.py` (the
  elevator); change the scripts, not the files

### Requirements
- F-010_patch-open-azeroth (Kezan's terrain and tower)
- Open Azeroth's maps (patch-OAMaps) from 2026-11-21 on: they add Bladefist Bay's zeppelin tower and hide Kezan's
  north static zeppelin, which this one replaces. With older maps the zeppelin docks at Bladefist Bay in thin air and
  at Kezan inside the static one
- The realm's client DBCs (the path, the elevator's display and animation are DBC rows)

### Considerations
- Untested in game
- With F-140_hidden-transports the zeppelin is meant to stay hidden until the Pandaria intro's first trip; that row
  comes with the intro quests
- Players reach Kezan only with the continent bridge (lua_scripts/open-azeroth/continent_bridge.lua) from
  2026-11-21 on, which no longer sends them to the Eastern Kingdoms there
