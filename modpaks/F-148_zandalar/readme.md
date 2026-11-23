# mod-worgoblin-high-elf
## F-148_zandalar

### Features
- Zandalar (Battle for Azeroth's map 1642, `Zandalar`) as a visitable continent, for the 604 converted 3.3.5a tiles in `Patch-8.mpq` (from
  `D:\WoW\Continent Maps\5. Kul Tiras, Zandalar (kultiras, zandalar) - Stable-ish`)
- One zone, "Zandalar" (area 61148), covering the whole map: zone text, exploration (area bit 4091) and flying (F-006's flags)
- `.tele` targets from TrinityCore's retail TDB (24), e.g. `.tele Zuldazar`, `.tele TempleOfAkunda`, `.tele Ataldazar`
- Terrain only: no creatures, objects, quests, flight paths, graveyards, lights, music, world map or minimap

### Setup
- Client: the tiles ship in WHE-common's `modpaks/F-148_zandalar/World/Maps/Zandalar` (deploy-dbc.sh copies them into the realm patch)
- Server: map 1642's `.map` files and an empty `1642.vmtree` in the worldserver's DataDir, built from those tiles:
  `python tools/models/swap_server_maps.py 1642 <WHE-common>/modpaks/F-148_zandalar/World/Maps/Zandalar <DATA_DIR> --new-map`
  (`<DATA_DIR>/dbc` holds `LiquidType.dbc`). Copy `maps/1642*.map` and `vmaps/1642.vmtree` to the server. No mmaps
- Keep it after F-010 in the manifest: Open Azeroth's row for map 1642 is at expansion 7, which the core refuses to let a 3.3.5 account enter

### Considerations
- Most of the art is missing: the tiles name 60 of 76 tileset textures, 1534 of 2822 doodads and 419 of 458 WMOs that no 3.3.5 client has, so the ground is partly untextured, with
  few trees or buildings. Adding them (from retail, converted, e.g. with `tools/models/mop_assets.py --tiles`) needs no change here
- The tiles were checked on 2026-11-22: every MCIN/MCNK/MHDR offset is sound, and retail's .tele heights match the
  ground within a few yards wherever they stand on terrain; targets on buildings' floors were left out
- Retail's area ids are replaced by the one zone in the shipped tiles (`tools/models/adt_set_area.py 61148`); there aren't
  enough free area bits below 4096 for retail's subzones. The source tiles in `Patch-8.mpq` keep them
- The `1642.vmtree` is empty, so nothing blocks line of sight, matching the missing buildings
- Not ported to the 32-bit flavour
