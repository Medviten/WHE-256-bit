# mod-worgoblin-high-elf
## F-137_exiles-reach

### Features
- Exile's Reach (retail's map 2175, the Shadowlands new player island) as a visitable map, terrain only so far
- Its 16 areas with retail's English names (zone text, exploration), every one flyable
- Retail's map of the island (world map, single zone map like the Wandering Isle) and its minimaps
- Retail's lights of the map (sky, fog and water colours)
- `.tele ExilesReach` and one target per subarea (`.tele DarkmaulCitadel`, `.tele HarpyRoost`, ...)
- TrinityCore's six graveyards of the island
- The island's spawns from TrinityCore's retail TDB (1210): 873 creatures of 133 kinds (wildlife, murlocs,
  quilboar, ogres, harpies, worgs, spiders, the Alliance and Horde crews, Jaina, Thrall, Wrathion, the undead army)
  and 28 objects, with their waypoints, in retail's looks where they aren't dressed NPCs (models and textures in
  patch-ER.MPQ). Retail's quest-stage phases are per-spawn visibility conditions, so each crew member shows where
  your quest progress puts them, and each faction sees its own crew
- 101 quests of both factions' chains, the class quests (3.3.5a's classes) and the dungeon's: texts, objectives,
  quest items and their drops, map markers, faction and class restrictions (see the quest port plan, plan.md)
- Core patch `patches/core/quest-visibility-refresh.patch`: rechecks those visibility conditions when a quest
  changes

### Setup
- Client files: WHE-common's `patch-ER.MPQ` (tiles, models, buildings, textures, world map and minimaps). Copy it
  into the client's Data folder as `patch-ER.MPQ`; don't link it (see F-134: reading art through a link from a USB
  disk made map loads crawl)
- Server: map 2175's `.map` files and an empty `2175.vmtree` in the worldserver's DataDir, built from the converted
  tiles: `python tools/models/swap_server_maps.py 2175 <tiles> <DATA_DIR> --new-map` (`<DATA_DIR>/dbc/LiquidType.dbc`
  must exist). No vmaps or mmaps yet; F-090 is needed before building mmaps for a map id of 1000 and up
- Keep it after F-010 in the manifest

### How it was made
1. Tiles: `python tools/models/wago_folder.py world/maps/2175/ <src> --version 12.1.5.70961 --exclude "(_obj1|_lod)\.adt$"`
   (1202 tiles, mostly open sea: the ship intros sail in the North Sea parts of the map)
2. `python tools/models/cata_adt_to_wotlk.py <src>/world/maps/2175 <tiles> --cata-dbc <MoP dbc> --stock-dbc <stock dbc>
   --effects <stock GroundEffectTexture.dbc> --name ExilesReach --listfile <community listfile> --wdt`
3. DBC and world rows: `python -I -X utf8 tools/races/retail_map_port.py <csv> <stock dbc> <tiles> modpaks
   modpaks/F-137_exiles-reach --graveyards <tdb_graveyards.txt>`. `<csv>` holds wago.tools' exports of 12.1.5.70961
   (Map, AreaTable, Light, LightParams, LightData, UiMap, UiMapAssignment); the graveyards are TrinityCore's retail
   TDB's (1210) `world_safe_locs` rows of map 2175, pulled out as `wsl|id|map|x|y|z|facing|comment` lines
4. Art: `python -I tools/models/mop_assets.py modpaks/F-137_exiles-reach <stage> --common-out <WHE-common>/patch-ER.MPQ
   --version 12.1.5.70961 --tiles <tiles> --fetch --convert --install`
5. World map: `python -I tools/models/retail_map_art.py <csv> 1409 ExilesReach <WHE-common>/patch-ER.MPQ`
6. Minimaps: `python -I tools/models/mop_minimaps.py <tiles> ExilesReach <WHE-common>/patch-ER.MPQ --source 2175
   --version 12.1.5.70961`
7. Spawns and quests: `python -I -X utf8 tools/races/retail_world_port.py <TDB_full_world_1210.26091_*.sql> <csv>
   modpaks/F-137_exiles-reach --cache <pickle>` (`<csv>` also needs the tables its docstring lists), then step 4
   again with a new `<stage>` (without `--tiles`) for the models, textures and icons it lists
8. F-134's art fix-ups on `<WHE-common>/patch-ER.MPQ`: `tools/models/mop_m2_env.py`, `mop_m2_nobatch.py`,
   `wmo_mop_fixups.py` (each `python -I <script> <WHE-common>/patch-ER.MPQ`)

### Known Issues
- Not tried in game yet
- Quests are the data stage (plan.md stage 1): no start on the island yet, and nothing scripted. TrinityCore
  names the givers of only 30 quests; 35 more are inferred (the faction's NPC at retail's turn-in marker, the giver
  the previous quest's ender), and 36 have no giver or ender yet (the ship intro, the class quests, the Darkmaul
  finale: their NPCs are summoned by scripts). 25 criteria-tree objectives (emotes, buying, casting a class
  spell, ...) are dropped, so some quests complete with less. Without the core patch, quest-stage NPCs only update
  when you move
- Scripts aren't ported: casters only melee, rescues, escorts and the boar ride don't run (plan.md stage 3)
- Dressed story NPCs (the crews) wear a stock NPC look of their race and sex for now (plan.md stage 2)
- No gear rewards yet (retail's quest packages) and RewardMoney 0
- Levels follow the quest route by area (retail scales them); enemies have no weapons (retail item ids)
- Hrun the Exiled is a stock skeleton (retail dresses one through CreatureDisplayInfoExtra)
- No grass: retail's ground effect ids aren't in 3.3.5a's GroundEffectTexture.dbc, so the converter clears them
- No baked terrain shadows (F-134's adt_bake_shadows.py): baked tiles would also need 2175 in the client's
  `bakedShadowMaps` CVar, or they double up with the real-time ones
- Minimaps are retail's 512 x 512 tiles (stock's are 256 x 256); not checked in game
- Map id 2175 is above 1000: not checked in the client
- Only the 256-bit flavour exists so far
- Generated: change the scripts, not the SQL
