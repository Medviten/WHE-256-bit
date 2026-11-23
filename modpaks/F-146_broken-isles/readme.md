# mod-worgoblin-high-elf
## F-146_broken-isles

### Features
- Broken Isles (Legion's map 1220, `Troll Raid`) as a visitable continent, for the 729 converted 3.3.5a tiles in `Patch-7.mpq` (from
  `D:\WoW\Continent Maps\4. Broken Isles (troll raid) - Stable-ish`)
- One zone, "Broken Isles" (area 61146), covering the whole map: zone text, exploration (area bit 4093) and flying (F-006's flags)
- `.tele` targets from TrinityCore's retail TDB (8), e.g. `.tele Azsuna`, `.tele Highmountain`, `.tele Stormheim`
- Terrain only: no creatures, objects, quests, flight paths, graveyards, lights, music, world map or minimap

### Setup
- Client: the tiles ship in WHE-common's `modpaks/F-146_broken-isles/World/Maps/Troll Raid` (deploy-dbc.sh copies them into the realm patch)
- Server: map 1220's `.map` files and an empty `1220.vmtree` in the worldserver's DataDir, built from those tiles:
  `python tools/models/swap_server_maps.py 1220 <WHE-common>/modpaks/F-146_broken-isles/World/Maps/Troll Raid <DATA_DIR> --new-map`
  (`<DATA_DIR>/dbc` holds `LiquidType.dbc`). Copy `maps/1220*.map` and `vmaps/1220.vmtree` to the server. No mmaps
- Keep it after F-010 in the manifest: Open Azeroth's row for map 1220 is at expansion 6, which the core refuses to let a 3.3.5 account enter

### Considerations
- Most of the art is missing: the tiles name 92 of 157 tileset textures, 2168 of 4626 doodads and 466 of 553 WMOs that no 3.3.5 client has, so the ground is partly untextured, with
  few trees or buildings. Adding them (from retail, converted, e.g. with `tools/models/mop_assets.py --tiles`) needs no change here
- The tiles were checked on 2026-11-22: every MCIN/MCNK/MHDR offset is sound, and retail's .tele heights match the
  ground within a few yards wherever they stand on terrain; targets on buildings' floors were left out
- Retail's area ids are replaced by the one zone in the shipped tiles (`tools/models/adt_set_area.py 61146`); there aren't
  enough free area bits below 4096 for retail's subzones. The source tiles in `Patch-7.mpq` keep them
- The `1220.vmtree` is empty, so nothing blocks line of sight, matching the missing buildings
- Not ported to the 32-bit flavour
