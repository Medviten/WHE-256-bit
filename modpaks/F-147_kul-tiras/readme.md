# mod-worgoblin-high-elf
## F-147_kul-tiras

### Features
- Kul Tiras (Battle for Azeroth's map 1643, `KulTiras`) as a visitable continent, for the 600 converted 3.3.5a tiles in `Patch-8.mpq` (from
  `D:\WoW\Continent Maps\5. Kul Tiras, Zandalar (kultiras, zandalar) - Stable-ish`)
- One zone, "Kul Tiras" (area 61147), covering the whole map: zone text, exploration (area bit 4092) and flying (F-006's flags)
- `.tele` targets from TrinityCore's retail TDB (43), e.g. `.tele TiragardeSoundNorth`, `.tele Drustvar`, `.tele StormSongValley`, `.tele MechagonIsland`
- Terrain only: no creatures, objects, quests, flight paths, graveyards, lights, music, world map or minimap

### Setup
- Client: the tiles ship in WHE-common's `modpaks/F-147_kul-tiras/World/Maps/KulTiras` (deploy-dbc.sh copies them into the realm patch)
- Server: map 1643's `.map` files and an empty `1643.vmtree` in the worldserver's DataDir, built from those tiles:
  `python tools/models/swap_server_maps.py 1643 <WHE-common>/modpaks/F-147_kul-tiras/World/Maps/KulTiras <DATA_DIR> --new-map`
  (`<DATA_DIR>/dbc` holds `LiquidType.dbc`). Copy `maps/1643*.map` and `vmaps/1643.vmtree` to the server. No mmaps
- Keep it after F-010 in the manifest: Open Azeroth's row for map 1643 is at expansion 7, which the core refuses to let a 3.3.5 account enter

### Considerations
- Most of the art is missing: the tiles name 54 of 89 tileset textures, 1745 of 3519 doodads and 258 of 320 WMOs that no 3.3.5 client has, so the ground is partly untextured, with
  few trees or buildings. Adding them (from retail, converted, e.g. with `tools/models/mop_assets.py --tiles`) needs no change here
- The tiles were checked on 2026-11-22: every MCIN/MCNK/MHDR offset is sound, and retail's .tele heights match the
  ground within a few yards wherever they stand on terrain; targets on buildings' floors were left out
- Retail's area ids are replaced by the one zone in the shipped tiles (`tools/models/adt_set_area.py 61147`); there aren't
  enough free area bits below 4096 for retail's subzones. The source tiles in `Patch-8.mpq` keep them
- The `1643.vmtree` is empty, so nothing blocks line of sight, matching the missing buildings
- Not ported to the 32-bit flavour
