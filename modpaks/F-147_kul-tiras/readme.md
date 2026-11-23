# mod-worgoblin-high-elf
## F-147_kul-tiras

### Features
- Kul Tiras (Battle for Azeroth's map 1643, `KulTiras`) as a visitable continent, for the 600 converted 3.3.5a tiles in `Patch-8.mpq` (from
  `D:\WoW\Continent Maps\5. Kul Tiras, Zandalar (kultiras, zandalar) - Stable-ish`)
- One zone, "Kul Tiras" (area 61147), covering the whole map: zone text, exploration (area bit 4092) and flying (F-006's flags)
- `.tele` targets from TrinityCore's retail TDB (43), e.g. `.tele TiragardeSoundNorth`, `.tele Drustvar`, `.tele StormSongValley`, `.tele MechagonIsland`
- Terrain, its textures and the WMOs (buildings) in the tiles; no doodads (trees, rocks, props), creatures, objects, quests, flight paths, graveyards, lights, music, world map or minimap

### Setup
- Client: WHE-common's `patch-KulTiras.MPQ` (tiles in `World/Maps/KulTiras`, terrain textures and WMOs). Copy it into the client's
  Data folder as `patch-KulTiras.MPQ`; don't link it (see F-134: reading art through a link from a USB disk hangs loads)
- Server: map 1643's `.map` files and an empty `1643.vmtree` in the worldserver's DataDir, built from those tiles:
  `python tools/models/swap_server_maps.py 1643 <WHE-common>/patch-KulTiras.MPQ/World/Maps/KulTiras <DATA_DIR> --new-map`
  (`<DATA_DIR>/dbc` holds `LiquidType.dbc`). Copy `maps/1643*.map` and `vmaps/1643.vmtree` to the server. No mmaps
- Keep it after F-010 in the manifest: Open Azeroth's row for map 1643 is at expansion 7, which the core refuses to let a 3.3.5 account enter

### Considerations
- Art: retail 12.1.5.70961's terrain textures and WMOs, fetched and converted with
  `python -I tools/models/mop_assets.py modpaks/F-147_kul-tiras <stage> --common-out <WHE-common>/patch-KulTiras.MPQ --version 12.1.5.70961
  --tiles <WHE-common>/patch-KulTiras.MPQ/World/Maps/<dir> --no-doodads --fetch --convert`, then
  `tools/models/wmo_mop_fixups.py <stage>-out`, then the first command again with `--install`. Doodads are left out (`--no-doodads`): without them the
  ground is bare apart from the buildings, and the WMOs' own doodad sets point at models no client has. One sky cube map the WMOs name
  (`tileset/terrain cube maps/tcb_sicklysky_s.blp`) isn't in the community listfile, so it's missing
- The tiles were checked on 2026-11-22: every MCIN/MCNK/MHDR offset is sound, and retail's .tele heights match the
  ground within a few yards wherever they stand on terrain; targets on buildings' floors were left out
- Retail's area ids are replaced by the one zone in the shipped tiles (`tools/models/adt_set_area.py 61147`); there aren't
  enough free area bits below 4096 for retail's subzones. The source tiles in `Patch-8.mpq` keep them
- The `1643.vmtree` is empty, so nothing blocks line of sight, matching the missing buildings
- Not ported to the 32-bit flavour
