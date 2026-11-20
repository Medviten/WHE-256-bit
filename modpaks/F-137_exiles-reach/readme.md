# mod-worgoblin-high-elf
## F-137_exiles-reach

### Features
- Exile's Reach (retail's map 2175, the Shadowlands new player island) as a visitable map
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
- A start zone: races whose `player_race_template` row has `exiles_reach = 1` (F-091's default: most custom
  races; stock races and the race modpaks that keep their home race's start set 0) start on the island's beach,
  except Death Knights (`zz_[F-137]_start.sql`). With the Wandering Isle start on, the races it takes (Pandaren, and
  Hozen, Mogu and Jinyu with them) go there instead
- Character creation shows those races retail's Stormwind or Orgrimmar scene (UI_Alliance / UI_Horde in
  WHE-common). The client can't see `exiles_reach`: `ExilesReachKeepStart` in `data/patch-A.MPQ/Interface/GlueXML/
  GlueParent.lua` lists the races writing 0, so a race modpak that sets 0 adds its file string there
- The ship intro: the Alliance Ship and the Horde Transport sail retail's loops off the island as continent
  transports, with their crews on deck. With `ExilesReachStartZone.Enable = 1` (core patch below) those new
  characters start aboard their faction's ship instead of the beach:
  Warming Up (hit a Combat Dummy), Stand Your Ground (spar with Private Cole / Grunt Throg, who yield at 30%
  health), Brace for Impact (turning it in wrecks the ship: you wake on the beach)
- Darkmaul Citadel (retail's map 2236) as a 5-player dungeon: its terrain, its 36 creatures (Tunk, Gor'groth,
  Kalecgos and their guards), in and out through the portals at the citadel's gate (`.tele DarkmaulCitadel` lands
  at its entrance). Killing Gor'groth stops his ritual for the dungeon quest; talking to Kalecgos credits leaving
  and sends you to Stormwind or Orgrimmar, bound there: the way off the island
- Every quest of both chains, the class quests and the Darkmaul gate's can be done: Wowhead's givers and enders (saved
  quest pages, `--wowhead`), the NPCs and objects TrinityCore only summons spawned at Wowhead's map points (the gate's
  leaders, the class trainers and ghosts, catapults, runestones; 44 NPCs, 11 objects), each shown to its faction
  until its quests are done. Steps retail scripts (bandaging, riding, rescues, spars, class ability practice, scenes)
  are talking to the NPC (gossip credit); items it hands over come from talking to the quest NPC, or from chests
  placed beside the class quests' NPCs. An End to Beginnings as retail: Kalecgos at the gate flies you to Stormwind
  or Orgrimmar, where Captain Garrick / Warlord Breka Grimaxe end it
- Core patches: `patches/core/quest-visibility-refresh.patch` rechecks those visibility conditions when a quest
  changes; `patches/core/exiles-reach-start.patch` adds `ExilesReachStartZone.Enable`, boards new characters and
  scripts Kalecgos (`npc_darkmaul_kalecgos`)

### Setup
- Client files: WHE-common's `patch-ER.MPQ` (tiles, models, buildings, ships, textures, world map and minimaps).
  Copy it into the client's Data folder as `patch-ER.MPQ`; don't link it (see F-134: reading art through a link from
  a USB disk made map loads crawl)
- Server: the `.map` files of maps 2175 and 2236 and an empty `2175.vmtree` / `2236.vmtree` in the worldserver's
  DataDir, built from the converted tiles: `python tools/models/swap_server_maps.py <map> <tiles> <DATA_DIR> --new-map`
  (`<DATA_DIR>/dbc/LiquidType.dbc` must exist). No vmaps or mmaps yet; F-090 is needed before building mmaps for a
  map id of 1000 and up
- The start: F-091's `exiles_reach` column (rebuild the world database so the table is made again). The ship:
  both core patches, `ExilesReachStartZone.Enable = 1` and `EnableContinentTransport = 1` (the default) in
  worldserver.conf. Without the core patch Kalecgos has no script: talking to him does nothing
- Keep it after F-010 in the manifest (its rows for maps 2175, 2261 and 2369 are replaced)

### How it was made
1. Tiles: `python tools/models/wago_folder.py world/maps/2175/ <src> --version 12.1.5.70961 --exclude "(_obj1|_lod)\.adt$"`
   (1202 tiles, mostly open sea: the ship intros sail in the North Sea parts of the map); the same for
   `world/maps/2236/` (Darkmaul Citadel, 195 tiles)
2. `python tools/models/cata_adt_to_wotlk.py <src>/world/maps/2175 <tiles> --cata-dbc <MoP dbc> --stock-dbc <stock dbc>
   --effects <stock GroundEffectTexture.dbc> --name ExilesReach --listfile <community listfile> --wdt`; the same for
   2236 into `<dungeon tiles>` with `--name DarkmaulCitadel`. Copy both into `patch-ER.MPQ/World/Maps/<name>/`
3. DBC and world rows: `python -I -X utf8 tools/races/retail_map_port.py <csv> <stock dbc> <tiles> modpaks
   modpaks/F-137_exiles-reach --graveyards <tdb_graveyards.txt>`. `<csv>` holds wago.tools' exports of 12.1.5.70961
   (Map, AreaTable, Light, LightParams, LightData, UiMap, UiMapAssignment); the graveyards are TrinityCore's retail
   TDB's (1210) `world_safe_locs` rows of map 2175, pulled out as `wsl|id|map|x|y|z|facing|comment` lines, plus
   row 100096 (Darkmaul Citadel's entrance). The dungeon: the same with `<dungeon tiles> --map 2236 --tag F-137,DC
   --directory DarkmaulCitadel --name "Darkmaul Citadel" --tele-base 22360 --dungeon 2175 721.7 -1838.4`
4. Art: `python -I tools/models/mop_assets.py modpaks/F-137_exiles-reach <stage> --common-out <WHE-common>/patch-ER.MPQ
   --version 12.1.5.70961 --tiles <tiles> --fetch --convert --install` (the dungeon's with `--tiles <dungeon tiles>`)
5. World map: `python -I tools/models/retail_map_art.py <csv> 1409 ExilesReach <WHE-common>/patch-ER.MPQ`
6. Minimaps: `python -I tools/models/mop_minimaps.py <tiles> ExilesReach <WHE-common>/patch-ER.MPQ --source 2175
   --version 12.1.5.70961`; the dungeon's: `<dungeon tiles> DarkmaulCitadel ... --source 2236`
7. Spawns, quests, ships and the dungeon's instance rows: `python -I -X utf8 tools/races/retail_world_port.py
   <TDB_full_world_1210.26091_*.sql> <csv> modpaks/F-137_exiles-reach --cache <pickle>` (`<csv>` also needs the
   tables its docstring lists), then step 4 again with a new `<stage>` (without `--tiles`) for the models, textures
   and icons it lists. The scripted steps are hand-written: `sql/db-world/base/zz_[F-137]_smartai.sql`
8. F-134's art fix-ups on the new art (each `python -I <script> <folder>`): `tools/models/mop_m2_env.py`,
   `mop_m2_nobatch.py`, `wmo_mop_fixups.py`

### Known Issues
- Not tried in game yet, the ships and the dungeon least of all (AzerothCore transports on a map above 1000, combat
  on a moving deck, the sparring's faction switch)
- Quests are mostly the data stage (plan.md): TrinityCore names the givers of only 30 quests; 35 more are inferred
  (the faction's NPC at retail's turn-in marker, the giver the previous quest's ender), and the class quests'
  trainers and the Darkmaul finale's NPCs (An End to Beginnings) are summoned by scripts, so those quests have no
  giver or ender yet. 23 criteria-tree objectives (emotes, buying, casting a class spell, ...) are dropped, so some
  quests complete with less. Without the core patch, quest-stage NPCs only update when you move
- Scripts aren't ported beyond the ship and Darkmaul steps above: casters only melee, rescues, escorts and the boar
  ride don't run (plan.md stage 3)
- The ship intro has no crash scene (retail's cutscene): the turn-in teleports you to the beach. The hunters' pets
  on deck are left out
- New characters' hearthstones are bound to the beach until Kalecgos sends them to their capital. Random bots of
  the races that start here are created on the island too
- Scripted steps are simplified: talking to an NPC stands in for retail's items, rides, spars and scenes
  (OBJECTIVE_TALKS in retail_world_port.py), so they complete at once. Bloodbeak (the harpy rescues) is spawned at Wowhead's spot atop the roost; killing
  it completes the rescue (no ritual event). The class quest chests stand beside their NPCs (no
  positions known). Training Rock has no giver. Retail's emote steps and buying / selling are left out
- Darkmaul Citadel: no boss mechanics (Tunk and Gor'groth only melee), its doors are left out (TrinityCore opens
  them by script), no group finder entry, no vmaps (NPCs standing on the citadel's floors drop to the terrain when
  they move)
- Dressed story NPCs (the crews) wear a stock NPC look of their race and sex for now (plan.md stage 2)
- No gear rewards yet (retail's quest packages) and RewardMoney 0
- Levels follow the quest route by area (retail scales them); enemies have no weapons (retail item ids)
- Hrun the Exiled is a stock skeleton (retail dresses one through CreatureDisplayInfoExtra)
- No grass: retail's ground effect ids aren't in 3.3.5a's GroundEffectTexture.dbc, so the converter clears them
- No baked terrain shadows (F-134's adt_bake_shadows.py): baked tiles would also need 2175 in the client's
  `bakedShadowMaps` CVar, or they double up with the real-time ones
- Retail fogs by density: the lights get a fixed fog distance (22000, as the Wandering Isle) where retail has none
- Minimaps are retail's 512 x 512 tiles (stock's are 256 x 256); not checked in game
- Map ids 2175, 2236, 2261 and 2369 are above 1000: not checked in the client
- Only the 256-bit flavour exists so far
- Generated: change the scripts, not the SQL (except `zz_[F-137]_smartai.sql`)
