# mod-worgoblin-high-elf
## F-134_mop-wandering-isle

### Features
- The Wandering Isle (Mists of Pandaria's map 860, `NewRaceStartZone`, the Pandaren starting zone on Shen-zin Su) as a visitable map
- Its 34 5.4.8 areas with English names from retail's AreaTable (zone text, exploration), every one flyable
- MoP's map of the island and its explored-area overlays
- `.tele TheWanderingIsle`
- Terrain only: no creatures, objects, quests or graveyards

### Setup
- Client files (in WHE-common's `modpaks/F-134_mop-wandering-isle`, which `deploy-dbc.sh` copies into the realm's own patch when `LOCAL_COMMON_DIR` is set): the island's 100 tiles, its WDT and WDL, and the map art
- Server: map 860's `.map` files and a `860.vmtree` in the worldserver's DataDir, built from the converted tiles:
  `python tools/models/swap_server_maps.py 860 <tiles> <DATA_DIR> --new-map` (see F-133's readme). No mmaps
- Keep it after F-010 in the manifest: Open Azeroth also has map 860, at expansion 0 but without the rest

### How the tiles were made
MoP Classic's tiles (5.5.4) name textures and models by file id, which 3.3.5 can't read:
1. `python tools/models/wago_folder.py world/maps/newracestartzone/ <src> --exclude "_obj1\.adt$"`
2. `python tools/models/cata_adt_to_wotlk.py <src>/world/maps/newracestartzone <tiles> --cata-dbc <MoP dbc> --stock-dbc <stock dbc> --effects <stock GroundEffectTexture.dbc> --name NewRaceStartZone --listfile community-listfile.csv --wdt`
   (the [community listfile](https://github.com/wowdev/wow-listfile) names the file ids)
3. `python tools/races/mop_map_port.py <MoP dbc> <stock dbc> AreaTable.csv <tiles> modpaks modpaks/F-134_mop-wandering-isle --map 860 --tag F-134 --directory NewRaceStartZone --name "The Wandering Isle" --tele-base 86100`
4. `python tools/models/mop_map_art.py <MoP dbc> <WHE-common>/modpaks/F-134_mop-wandering-isle --map 860`

### Considerations
- Most of the art is missing, as on Pandaria (F-133): 17 of the 20 terrain textures, 337 of the 435 doodads and 43 of the 44 buildings aren't in any 3.3.5 client
- MoP's ground effect ids (grass and the like) aren't in the client and are cleared
- Not on a moving turtle: 3.3.5 terrain can't move (only transports do), so like retail the island is its own map
- Generated: change the scripts, not the SQL
