# mod-worgoblin-high-elf
## F-137_exiles-reach

### Features
- Exile's Reach (retail's map 2175, the Shadowlands new player island) as a visitable map, terrain only so far
- Its 16 areas with retail's English names (zone text, exploration), every one flyable
- Retail's map of the island (world map, single zone map like the Wandering Isle) and its minimaps
- Retail's lights of the map (sky, fog and water colours)
- `.tele ExilesReach` and one target per subarea (`.tele DarkmaulCitadel`, `.tele HarpyRoost`, ...)
- TrinityCore's six graveyards of the island

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
7. F-134's art fix-ups on `<WHE-common>/patch-ER.MPQ`: `tools/models/mop_m2_env.py`, `mop_m2_nobatch.py`,
   `wmo_mop_fixups.py` (each `python -I <script> <WHE-common>/patch-ER.MPQ`)

### Known Issues
- Not tried in game yet
- No NPCs, quests or start yet (planned: TrinityCore's retail TDB and scripts, and a switch that starts new
  characters on the island)
- No grass: retail's ground effect ids aren't in 3.3.5a's GroundEffectTexture.dbc, so the converter clears them
- No baked terrain shadows (F-134's adt_bake_shadows.py): baked tiles would also need 2175 in the client's
  `bakedShadowMaps` CVar, or they double up with the real-time ones
- Minimaps are retail's 512 x 512 tiles (stock's are 256 x 256); not checked in game
- Map id 2175 is above 1000: not checked in the client
- Only the 256-bit flavour exists so far
- Generated: change the scripts, not the SQL
