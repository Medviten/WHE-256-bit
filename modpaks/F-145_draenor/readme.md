# mod-worgoblin-high-elf
## F-145_draenor

### Features
- Draenor (Warlords of Draenor's map 1116, `Draenor`) as a visitable continent, for the 1221 converted 3.3.5a tiles in `Patch-6.mpq` (from
  `D:\WoW\Continent Maps\3. Draenor (draenor) - Stable-ish`)
- One zone, "Draenor" (area 61145), covering the whole map: zone text, exploration (area bit 4094) and flying (F-006's flags)
- `.tele` targets from TrinityCore's retail TDB (30), e.g. `.tele DraenorShadowmoonValley`, `.tele DraenorNagrand`, `.tele Stormshield`
- Terrain, its textures and the WMOs (buildings) in the tiles; no doodads (trees, rocks, props), creatures, objects, quests, flight paths, graveyards, lights, music, world map or minimap

### Setup
- Client: WHE-common's `patch-Draenor.MPQ` (tiles in `World/Maps/Draenor`, terrain textures and WMOs). Copy it into the client's
  Data folder as `patch-Draenor.MPQ`; don't link it (see F-134: reading art through a link from a USB disk hangs loads)
- Server: map 1116's `.map` files and an empty `1116.vmtree` in the worldserver's DataDir, built from those tiles:
  `python tools/models/swap_server_maps.py 1116 <WHE-common>/patch-Draenor.MPQ/World/Maps/Draenor <DATA_DIR> --new-map`
  (`<DATA_DIR>/dbc` holds `LiquidType.dbc`). Copy `maps/1116*.map` and `vmaps/1116.vmtree` to the server. No mmaps
- Keep it after F-010 in the manifest: Open Azeroth's row for map 1116 is at expansion 5, which the core refuses to let a 3.3.5 account enter

### Considerations
- Art: retail 12.1.5.70961's terrain textures and WMOs, fetched and converted with
  `python -I tools/models/mop_assets.py modpaks/F-145_draenor <stage> --common-out <WHE-common>/patch-Draenor.MPQ --version 12.1.5.70961
  --tiles <WHE-common>/patch-Draenor.MPQ/World/Maps/<dir> --no-doodads --fetch --convert`, then
  `tools/models/wmo_mop_fixups.py <stage>-out`, then the first command again with `--install`. Doodads are left out (`--no-doodads`): without them the
  ground is bare apart from the buildings, and the WMOs' own doodad sets point at models no client has
- The tiles were checked on 2026-11-22: every MCIN/MCNK/MHDR offset is sound, and retail's .tele heights match the
  ground within a few yards wherever they stand on terrain; targets on buildings' floors were left out
- Retail's area ids are replaced by the one zone in the shipped tiles (`tools/models/adt_set_area.py 61145`); there aren't
  enough free area bits below 4096 for retail's subzones. The source tiles in `Patch-6.mpq` keep them
- The vmtree is empty, so the buildings don't block line of sight or movement on the server yet
- Not ported to the 32-bit flavour
