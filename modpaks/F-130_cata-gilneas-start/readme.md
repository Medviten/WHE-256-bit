# mod-worgoblin-high-elf
## F-130_cata-gilneas-start

### Features
- The Cataclysm Worgen starting zone from [Project Neltharion](https://github.com/ProjectNeltharion)'s 4.3.4 world database: Gilneas City, Duskhaven, the Northern Headlands, Greymane Manor, Stormglen and Tal'doren, with their creatures, quests, phases and scripts (121 quests, 324 creatures, 121 objects)
- New Worgen characters, except Death Knights, start in Gilneas City by Prince Liam Greymane, after Cataclysm's Worgen intro flythrough over the city (`dbc/[F-130]_worgen_intro_cinematic.sql`; `Cameras\FlyByWorgen.m2` and its narration in WHE-common's patch-A.MPQ, MoP Classic's copies, the camera converted with wotlkconv)

### Requirements
- F-010_patch-open-azeroth, whose Eastern Kingdoms has Cataclysm's Gilneas, and its map files. Cataclysm's Gilneas map (654) lies at the same coordinates, so the zone is spawned on map 0 unchanged
- F-024_mod-playable-worgen (the Worgen race, its Gilneas faction 1134 and its models) and F-027_mod-gilnean
- `patches/core/gilneas-start.patch` and a recompile. It applies after F-013's `goblin-start.patch` (to the `whe-patch-base` tag), whose core support it uses: zone phasing (`phase_definitions`), phase conditions, vehicle bars, quest/movie SmartAI events. The 256-bit core has both
- `GilneasStartZone.Enable = 1` in `worldserver.conf`. It turns on what `GoblinStartZone.Enable` does as well, and gates the patch's changes to stock behaviour: the Worgen curse being reapplied on login in the stocks, and the Worgen racials below; the scripts only run for the creatures this modpak names

### Worgen racials
As in Cataclysm, Worgen other than Death Knights start as humans and earn their racials in Gilneas. `dbc/[F-130]_worgen_racials.sql` leaves F-024's racial skill line rows (Viciousness, Aberration, Flayer, Darkflight, Two Forms) to Death Knights, and the core patch:
- keeps Human Form (F-024's 68995, with F-063 the altered form aura for both genders, so the player looks like their own character; without F-063 the gendered transforms 68995 / 110020) on them until "Last Stand" (14222) is rewarded
- on that reward, whose cutscene turns them, removes it and teaches the four racials
- teaches Two Forms through "Neither Human Nor Beast" (24593, its 72829 forcecasts 72857 Learn Two Forms)
- turns a Worgen found outside Gilneas without Last Stand (a bot, or a character from before the zone) there, and teaches Two Forms too

Running Wild stays F-024's: taught at level 20 by `src/Worgoblin.cpp`.
- Keep it after F-002 in the manifest. F-013 isn't needed: this modpak creates the `phase_definitions` table too

### Client assets
In WHE-common's `patch-A.MPQ`, from the 4.3.4 client's `art.MPQ` (still downloadable from Blizzard's CDN, the location in [ClientDownloader](https://github.com/The-Cataclysm-Preservation-Project/ClientDownloader)'s `WoW.mfil`; `tools/models/mpq_unpack.py` reads its format-4 archives):
- the 88 NPC bakes the zone's Cataclysm creature displays name, `Textures\BakedNPCTextures\CreatureDisplayExtra-<id>.blp` (the `texture` column of `dbc/[F-130]_creaturedisplayinfoextra.sql`). BLP2, used as they are
- the creature models of `CATA_MODELS` in the port script (mist fox, ettin, raven, crocodile, stagecoach harness and carriage), converted with Kalibro's wotlkconv, then `tools/models/m2_restore_anim_refs.py` (mist fox, raven) and `m2_unshare_tracks.py`. The mastiff is F-128's retail model at the same path; only the Cataclysm mastiff skins (gray, red, yellow) were added

- the NPCs' outfit pieces: `tools/checks/f013_item_assets.py --modpak modpaks/F-130_cata-gilneas-start --art <art.MPQ> --copy` copies the armour and helm textures to WHE-common and stages the Cataclysm item models (helms in every race art.MPQ has, shoulders, weapons) for wotlkconv and `m2_unshare_tracks.py`. Without a helm's race variant an NPC of that race wears a missing-model cube. Only 21 icons are left, of NPC-only displays

Still open: the models of the object displays in `dbc/[F-130]_gameobjectdisplayinfo.sql` that Open Azeroth's patch doesn't have aren't checked yet (Gilneas doodads mostly are)

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

Hand-written on top (`sql/db-world/base/zz_[I-378]_class_quest_wotlk_spells.sql`, loads after the generated files; it and `[I-379]` below are kept in `tools/races/cata_gilneas_fixes/sql/`, which the port copies in, since it rewrites `sql/`): the class trainer quests (14266-14283) are level 4 and practise what the trainer teaches at 4 (Serpent Sting, Frostbolt and Lesser Heal instead of Steady Shot, Arcane Missiles and Flash Heal), as F-013's Kezan quests do; the quests before them give enough XP to reach level 4.

Classes with no Gilneas class quest (ARAC's paladins and shamans, F-100's heroes) can go on without one (`zz_[I-379]_arac_classes.sql`). With F-029_all-trainers in the manifest, a paladin and a shaman trainer also stand beside Sister Almyra in each of her phases. Paladins and shamans then get the natives' three-step class chain too (Gwen Armstead's lead-in, a Judgement / Earth Shock practice quest on the Bloodfang Worgen, Safety in Numbers; `zz_[I-382]_arac_class_quests.sql`), and the shaman trainer gives F-002's Call of Earth.

Level-10 class quests Worgen otherwise only find after leaving Gilneas (`zz_[I-384]_level10_class_quests.sql`, `dbc/[I-384]_*`, kept in `tools/races/cata_gilneas_fixes/`), as F-013 has for the Lost Isles: Huntsman Blake's Taming the Beast (Vilebrood Skitterer, Swamp Crocolisk, Blackwald Fox -> Tame Beast, Beast Training), Vitus Darkwalker's Creature of the Void (subjugate a voidwalker at a summoning circle beside him -> Summon Voidwalker), and with F-029 the shaman trainer's Call of Fire (a Spirit of Fire and Raging Embers in the burning woods south of Stormglen -> Searing Totem, Fire Totem). Their spots are taken from existing spawns and not yet checked in game

### Known Issues
- Not tried in game or loaded into a database yet, and the core patch isn't compiled
- Neltharion's own server NPCs are left out (`NELTHARION_NPCS` in the port): Gnomey, their free-bag vendor, and the props on his spot are F-138_gnomey-helper; XP Rates needs their script
- No terrain swaps: Cataclysm floods Duskhaven and shakes Gilneas (maps 638, 655 and 656), but the phases play on Open Azeroth's post-Cataclysm Gilneas, where the Greymane Wall is open. A terrain modpak like F-102 can add them later
- Worgen change form only at Last Stand (see Worgen racials): Neltharion forces the altered form with 98274, which no client here has, and the curse (68630) only shows the Cataclysm auras. Two Forms and Running Wild themselves are F-063's
- NPCs greet, say farewell and get annoyed in their Cataclysm voices (`dbc/[F-130]_npc_*.sql`, 4.0.6a NPCSounds rows of the displays; the files, retail's .ogg, fetched into WHE-common's patch-A.MPQ with `tools/races/zep_goblin_sounds.py --sql`), but their spoken `creature_text` lines are silent: those sound ids are cleared
- The converted Cataclysm creature models haven't been looked at in game. wotlkconv drops their shadow batches and resets shaders 3.3.5a lacks to the default combiner; their CreatureSoundData ids stock lacks are cleared, so they're silent
- Spells 3.3.5a can't run are left out (68643, 70796, 72764, 94293), with the rows that cast them. The stagecoach ride's 72764 is replaced by boarding directly
- Neltharion's custom SmartAI action 204, its script `npc_woe_mixed_creatures_ai` and its spell 151181 (the stocks scene's script spell) aren't ported
- Creatures' loot references (Cataclysm world drops) are left out; their direct drops, quest items included, are there
- Cataclysm Summon Properties 3122 and 2993 aren't in 3.3.5a: their summons use 64
- Items have Cataclysm armour (raised in 4.0.1, so several times 3.3.5a's at these levels) and no durability
- Only the 256-bit flavour exists so far (no 32-bit copy, no port to `azerothcore-wotlk-32-bit`)
