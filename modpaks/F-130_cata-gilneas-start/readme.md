# mod-worgoblin-high-elf
## F-130_cata-gilneas-start

### Features
- The Cataclysm Worgen starting zone from [Project Neltharion](https://github.com/ProjectNeltharion)'s 4.3.4 world database: Gilneas City, Duskhaven, the Northern Headlands, Greymane Manor, Stormglen and Tal'doren, with their creatures, quests, phases and scripts (121 quests, 324 creatures, 121 objects)
- New Worgen characters, except Death Knights, start in Gilneas City by Prince Liam Greymane

### Requirements
- F-010_patch-open-azeroth, whose Eastern Kingdoms has Cataclysm's Gilneas, and its map files. Cataclysm's Gilneas map (654) lies at the same coordinates, so the zone is spawned on map 0 unchanged
- F-024_mod-playable-worgen (the Worgen race, its Gilneas faction 1134 and its models) and F-027_mod-gilnean
- `patches/core/gilneas-start.patch` and a recompile. It applies after F-013's `goblin-start.patch` (to the `whe-patch-base` tag), whose core support it uses: zone phasing (`phase_definitions`), phase conditions, vehicle bars, quest/movie SmartAI events. The 256-bit core has both
- `GilneasStartZone.Enable = 1` in `worldserver.conf`. It turns on what `GoblinStartZone.Enable` does as well, and gates the patch's one change to stock behaviour (the Worgen curse being reapplied on login in the stocks); the scripts only run for the creatures this modpak names
- Keep it after F-002 in the manifest. F-013 isn't needed: this modpak creates the `phase_definitions` table too

### Client assets
Not collected yet. `tools/checks/f013_item_assets.py --modpak modpaks/F-130_cata-gilneas-start` lists the item icons, models and textures the client lacks, and copies what Zeppelin-Craft's extracted files have with `--copy`. The zone's items have all theirs; the 179 files it reports are the NPCs' outfit pieces (armour textures, which the bakes below already contain, and 7 helm and shoulder models). Beyond those, the zone needs:
- the NPC bakes its Cataclysm creature displays name, `Textures\BakedNpcTextures\CreatureDisplayExtra-<id>.blp` (88; the list is the `texture` column of `dbc/[F-130]_creaturedisplayinfoextra.sql`). The client draws a humanoid NPC from its bake, so without one the NPC is untextured. If the community listfile has them for a Cataclysm Classic build, they can be downloaded from wago.tools the way `tools/races/zep_goblin_sounds.py` gets F-013's sounds (not checked)
- the models of the object displays in `dbc/[F-130]_gameobjectdisplayinfo.sql` that Open Azeroth's patch doesn't have (Gilneas doodads mostly are)

### Updating
The SQL is generated; make changes in the scripts or `tools/races/cata_gilneas_fixes/`, not in `dbc/` or `sql/`.
1. Extract the zone from Neltharion's world database (`source/sql/base/world.zip`, unpacked; ~3 minutes, ~30 s once the file is cached):
   ```
   python tools/races/cata_zone_extract.py <world.sql> <extract> --map 654 --map 655 --zone 4714 --zone 4755 \
     --creature 35170,35188,35230,35231,35370,35631,35753,35905,35907,36331,36450,36451,36555,36560,36741,37927,37953,38148,38286,38538,38540,38612,38756,38765,38766,38767,38768,43338,50415,50420,75138
   ```
   The `--creature` ones are summoned only by spells or by the core patch's scripts; the port lists any it still misses.
2. Port it: `python tools/races/cata_gilneas_port.py <extract> modpaks/F-130_cata-gilneas-start`. It reads the 4.0.6a client DBCs (`References/Cataclysm/Cataclysm_data/dbc`) and stock 3.3.5a's, rewrites `dbc/` and `sql/`, and prints what it had to leave out.

What the port does (details at the top of the script):
- Neltharion's TrinityCore rows become AzerothCore's, as Zeppelin-Craft's generator does for F-013; new spawn guids (13000001+, objects 7000001+), gossip menus and texts (520000+), waypoint paths (13000001+)
- Cataclysm spells, items, item displays, creature displays, NPC looks and faction templates that stock lacks come from the 4.0.6a client (`cata406_dbc_port.py`, `cata_items.py`); spell visuals and visual kits whose ids stock uses for something else stay stock's
- Neltharion's own server spells (151xxx) and the 4.3.4-only ones are rebuilt as Spell.dbc rows from Neltharion's `spell_dbc` / `spelleffect_dbc`
- Cataclysm's quest invisibility types 18, 30 and 36 become 9, 10 and 11: AzerothCore only has 0-11
- "Cast spell X on NPC" quest objectives (`RequiredSpellCast`), which AzerothCore lacks, become SmartAI credit on the NPC
- Stock creatures and objects the zone spawns (critters, Spirit Healer, herbs, ore) keep their stock rows; so does quest 3861

### Known Issues
- Not tried in game or loaded into a database yet, and the core patch isn't compiled
- No terrain swaps: Cataclysm floods Duskhaven and shakes Gilneas (maps 638, 655 and 656), but the phases play on Open Azeroth's post-Cataclysm Gilneas, where the Greymane Wall is open. A terrain modpak like F-102 can add them later
- Worgen don't change form with the story: Neltharion forces the altered form with 98274, which no client here has, and the curse (68630) only shows the Cataclysm auras. Two Forms and Running Wild are F-063's
- No intro cinematic, and NPC voices are silent: the zone's Cataclysm sound ids are cleared from `creature_text`
- 11 creature displays use Cataclysm models nothing here has (dogs, bats, Koroth, the ettin...): they show display 646 until the models are converted
- Spells 3.3.5a can't run are left out (68643, 70796, 72764, 81040, 94293), with the rows that cast them. The stagecoach ride's 72764 is replaced by boarding directly
- Neltharion's custom SmartAI action 204, its script `npc_woe_mixed_creatures_ai` and its spell 151181 (the stocks scene's script spell) aren't ported
- Creatures' loot references (Cataclysm world drops) are left out; their direct drops, quest items included, are there
- Cataclysm Summon Properties 3122 and 2993 aren't in 3.3.5a: their summons use 64
- Items have Cataclysm armour (raised in 4.0.1, so several times 3.3.5a's at these levels) and no durability
- Only the 256-bit flavour exists so far (no 32-bit copy, no port to `azerothcore-wotlk-32-bit`)
