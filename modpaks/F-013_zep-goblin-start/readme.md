# mod-worgoblin-high-elf
## F-013_zep-goblin-start

### Features
- The Cataclysm Goblin starting zone from [Zeppelin-Craft](https://github.com/ZepplinCore-Development/Zeppelin-Craft): Kezan and the Lost Isles, with their creatures, quests, phases and scripts
- New Goblin characters start in Kezan, except Death Knights, and see the Goblin intro cinematic

### Requirements
- F-010_patch-open-azeroth, whose Kalimdor holds both zones, and its map files
- F-023_mod-playable-goblin, which has the Bilgewater Cartel and "PLAYER, Goblin" factions. F-024_mod-playable-worgen too for the Worgen NPC model
- `patches/core/goblin-start.patch` and a recompile: phasing (`phase_definitions`), the zone's C++ scripts and SmartAI events. It applies to the `whe-patch-base` tag
- The client assets below
- Keep it after F-002 in the manifest, so that ARAC's extra classes also start in Kezan

### Client assets
Zeppelin-Craft doesn't keep its models and textures in git, so these come from its client patches and are in [WHE-common](https://github.com/Medviten/WHE-common). To see which files your client still lacks, list the files in the DBC SQL and run `tools/checks/check_f013_assets.py`.

New Goblin characters play the intro cinematic on their first login, so the client needs `Cameras\FlyByGoblin.m2`. The server also needs it, as `Cameras/FlyByGoblin.m2` in its data directory, to load the area around the camera. Older clients crash without the file, while clients with the camera guard skip the cinematic.

### Updating
`tools/races/zep_goblin_port.py <zep-goblin-start> <this folder>` regenerates `dbc/` and `sql/`, so make changes in that script, `variables.sql` or `patches/` rather than in the SQL. To rebuild the patch, apply these patches from Zeppelin-Craft's `zpaks/core-azerothcore/patches` to `whe-patch-base` in order and save the diff: 0031, 0032, 0034-0044, 0047-0050, 0052, 0053.

### Known Issues
- No terrain changes between phases: the town and the burning island need `zep-lost-isles-terrain`, core patch 0055 and a client change, none of which are ported. The server keeps using the base island
- Only tested as SQL so far, on the default modpaks plus F-010: not compiled and not played. Off-by-default modpaks' SQL wasn't tried with it, but their core patches combine with this one
- Other than the Goblin starts, the only existing rows it changes are 25 stock class quests, which Goblins lose because they get their own versions, and display 26556, whose zero bounding radius and combat reach it fixes. That also affects the stock aircraft sharing the display
- Stock NPCs spawned in the zones (Spirit Healer, rats, frogs, crabs...) keep their stock templates instead of Zeppelin's, so anything Zeppelin's zones expected from its versions is missing
