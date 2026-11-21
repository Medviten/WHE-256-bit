# mod-worgoblin-high-elf
## F-134_mop-wandering-isle

### Features
- The Wandering Isle (Mists of Pandaria's map 860, `NewRaceStartZone`, the Pandaren starting zone on Shen-zin Su) as a visitable map
- Its 34 5.4.8 areas with English names from retail's AreaTable (zone text, exploration), every one flyable
- MoP's map of the island and its explored-area overlays
- `.tele TheWanderingIsle`
- Its NPCs, objects and quests, from the TrinityCore MoP Classic port's Wandering Isle import: 369 creatures (2289 spawns), 158 objects (898 spawns), 91 quests, with gossip, SmartAI, waypoint paths, loot, the island's phases and its quest invisibility, the MoP spells and vehicles they use, and the island's scripted events (the core patch's `wandering_isle.cpp`)
- With `WanderingIsleStartZone.Enable = 1`, new Pandaren characters (F-020 / F-021), except Death Knights, start on the island by Master Shang Xi with "Much to Learn"
- Hozen (F-064, Horde), Mogu (F-117) and Jinyu (F-124, Alliance) start with the Pandaren of their side when their modpak is on: the island's
  Pandaren quests (their side's Pandaren's) take them too, which also lets WanderingIsleStartZone.Enable move them there,
  and they get the Pandaren outfit below (`WI_KIN` in tools/races/mop_wandering_isle_port.py). Without the Wandering
  Isle start they go to Exile's Reach (F-137) or their home race's start
- MoP's Pandaren starting gear (`dbc/[F-134]_wi_charstartoutfit.sql`, from 5.4.8's CharStartOutfit.dbc): the Trainee's set, food and Hearthstone for Pandaren warriors, hunters, rogues, priests, shamans and mages of both factions. No weapon, as in MoP: the class weapon is looted from the Iron Bough in "The Lesson of the Iron Bough", and the outfit only shows it in character creation's preview (hunters get the stock Rough Arrows and Light Quiver, as 3.3.5's crossbow needs ammo). Monk's outfit is left out (class 10 is F-100's Hero); the classes ARAC adds keep F-020 / F-021's outfits
- Class trainers and class quests (`zz_[I-387]_class_trainers_quests.sql`, `dbc/[I-387]_*`): Mists of Pandaria taught spells while levelling, so the island had no trainers at all. A trainer per class stands in the middle of Master Shang Xi's training grounds (the paladin, warlock and druid ones, ARAC's, only with F-029), each with a level-4 practice quest on the training targets or the Injured Trainees beside them; the shaman trainer gives F-002's Call of Earth. At Korga Strongmane's camp by the Wreck of the Skyseeker the hunter, shaman, warlock and druid trainers give level-10 chains: Taming the Beast (Ash Moth, Pei-Wu Tiger Cub, Pei-Wu Tiger), Creature of the Void, Call of Fire and Bear Form. Their spots are taken from existing spawns and not yet checked in game; the taming rods need F-013's core patch
- NPC greetings, farewells and annoyed lines in their MoP voices (`dbc/[F-134]_wi_npc_*.sql`: 5.4.8 NPCSounds rows of the displays, files named through the community listfile; fetched into WHE-common's patch-MoP.MPQ with `tools/races/zep_goblin_sounds.py --sql`). Spoken `creature_text` lines stay silent
- MoP's Pandaren intro flythrough over the island (`dbc/[F-134]_pandaren_intro_cinematic.sql`, `Cameras\FlyByPandaren.m2` and its narration in WHE-common's patch-MoP.MPQ). With the start switch off Pandaren still get it, over wherever they start

### Setup
- Client files (in WHE-common's `patch-MoP.MPQ`, shared with F-133: link or copy it into the client's Data folder tagged with the realm, e.g. `patch-MoP.256-bit.MPQ`, as F-133's World map art must not reach realms without F-133): the island's 100 tiles, its WDT and WDL, and the map art
- Server: map 860's `.map` files and a `860.vmtree` in the worldserver's DataDir, built from the converted tiles:
  `python tools/models/swap_server_maps.py 860 <tiles> <DATA_DIR> --new-map` (see F-133's readme). No mmaps
- Keep it after F-010 in the manifest: Open Azeroth also has map 860, at expansion 0 but without the rest
- Needs F-129, F-020 and F-021 (the Pandaren races and models the quests and NPCs use)
- `patches/core/wandering-isle-start.patch` and a recompile: the start, the island's scripts (`src/server/scripts/Custom/wandering_isle.cpp`, ported from the TrinityCore MoP Classic port, and `wandering_isle_ids.h`, which the port script writes with `--core`), MoP's quest invisibility types (the core's 12 invisibility types become 32; the island uses 5-30) and phase auras merged with the zone's phases (F-013's PhaseMgr now ORs them, as Cataclysm's did, instead of one replacing the other). It applies after F-013's `goblin-start.patch` and F-130's `gilneas-start.patch`; the 256-bit core has all three. `WanderingIsleStartZone.Enable = 1` in `worldserver.conf` turns it on, and with it everything `GoblinStartZone.Enable` does (the island's phases are `phase_definitions`, which this modpak creates). `playercreateinfo` isn't changed, so with the switch off the Pandaren start where they did

### How the tiles were made
MoP Classic's tiles (5.5.4) name textures and models by file id, which 3.3.5 can't read:
1. `python tools/models/wago_folder.py world/maps/newracestartzone/ <src> --exclude "_obj1\.adt$"`
2. `python tools/models/cata_adt_to_wotlk.py <src>/world/maps/newracestartzone <tiles> --cata-dbc <MoP dbc> --stock-dbc <stock dbc> --effects <stock GroundEffectTexture.dbc> --name NewRaceStartZone --listfile community-listfile.csv --wdt`
   (the [community listfile](https://github.com/wowdev/wow-listfile) names the file ids)
3. `python tools/races/mop_map_port.py <MoP dbc> <stock dbc> AreaTable.csv <tiles> modpaks modpaks/F-134_mop-wandering-isle --map 860 --tag F-134 --directory NewRaceStartZone --name "The Wandering Isle" --tele-base 86100`
4. `python tools/models/mop_map_art.py <MoP dbc> <WHE-common>/patch-MoP.MPQ --map 860`

### How the NPCs and quests were made
`python -I -X utf8 tools/races/mop_wandering_isle_port.py <trinitycore-mop-classic>/sql/updates/world/mop_classic modpaks/F-134_mop-wandering-isle --core <azerothcore-wotlk-256-bit>`
Then `python -I tools/models/mop_assets.py modpaks/F-134_mop-wandering-isle <stage> --common-out <WHE-common>/patch-MoP.MPQ --fetch --convert --install` for the art.
(`D:/wow-scratch/wi/db2/ItemSparse.csv` by default: wago.tools' English ItemSparse of 5.5.4.70449, for item names; `--data` to point elsewhere)

It replays the MoP port's generated import (`2026_10_18_02_world.sql`, from TrinityCore master's TDB 1210 with SkyFire 5.4.8 levels) and its later sniff audit and fixes in an in-memory database (`tools/races/tc_sql_load.py`), rewrites the rows to AzerothCore's tables and writes only its own files, `sql/db-world/base/zz_[AUTO,F-134]_wi_*.sql` and `dbc/[F-134]_wi_*.sql`, plus `wi_assets.txt`. It prints what it had to leave out. Details are at the top of the script:
- spawns get new guids (creatures and objects 13400001+), waypoint paths 13400001+, gossip menus 1340000+; MoP's creature, object and quest ids are kept unless config.sql or another modpak uses one (one creature moves to 1340000+, displays WHE allocates move to 1340000+)
- TrinityCore phase ids become phasemask bits and `phase_area` becomes `phase_definitions` rows for zone 5736 with an area condition
- Pandaren race masks become F-020 / F-021's (`@AlliancePandarenMask | @HordePandarenMask`)
- SmartAI waypoint actions and events move to AzerothCore's (232-236, 108/109); MoP's monk training emotes become the stock unarmed ones
- creature displays, NPC looks (with MoP's bake names), models, object displays, faction templates, area triggers and items come from the 5.4.8 DBCs (`References/MoP/MoP_data/dbc`, `tools/races/mop_items.py`); Pandaren NPCs use F-129's Pandaren models
- vehicles: the MoP Vehicle and VehicleSeat rows of the carts, poles, balloon, draft and the player-as-vehicle of None Left Behind (aura 296), in 3.3.5a's layout
- spells: every MoP spell the rows and the C++ use, and the spells those trigger, from the 5.4.8 split spell tables (`tools/races/mop_spells.py`, English text from wago.tools' SpellName.csv and Spell.csv in `--data`); TrinityCore's two server-side kill-credit spells from its `serverside_spell` rows. Cast time, range and radius indices map to stock rows with the same values, missing icons and summon properties are added. Phase auras get the port's phasemask bits (5.4.8 keeps the phase in MiscValueB); invisibility types 34-37 move to free ones below 32. Effects and auras 3.3.5a lacks become dummies the scripts can hook (the alternate power bars, Zhao-Ren's firework); a spell with more than three effects triggers a hidden helper spell with the rest from its third slot (like F-002's druid Arcane Torrent)

### Known Issues
- Not tried in game yet, and the core patch isn't compiled
- The scripts are compiled-checked only. Differences from TrinityCore's: area trigger exits are polled (3.3.5a clients only report entering); the meditation and Shen-zin Su bars count their aura ticks instead of filling an alternate power bar (3.3.5a has none, so there is no bar on screen); Zhao-Ren and the balloon fly polled spline legs; Li Fei's duel credits the attacker's group instead of a tap list
- Spells: no visuals yet (MoP's visual kits are a different system; spells work, but show no casting or impact effects). Spell values come from the 5.4.8 rows without MoP's spell scaling. Spells left out: 117492 and 128808 (Zhao-Ren's death; targets 3.3.5a lacks), 128607 (not in 5.4.8)
- Art: in WHE-common's `patch-MoP.MPQ` (`tools/models/mop_assets.py`: the files `wi_assets.txt`, the item displays and the creature skins name that no client file has, from MoP Classic 5.5.4 on wago.tools, converted with wotlkconv and `m2_unshare_tracks.py`, textures capped at 1024): 151 models and 930 textures, not looked at in game yet. 43 files have no source: 40 MoP item files later builds renamed (Pandaren starter leather, `buckle_panstart_a_01`, a belt icon) and 3 MoP Classic lacks (an LOD model, sunhat race variants)
- Gossip menus show stock's "Greetings, $n." (MoP's menu texts are in no source here); quests give no money (MoP's comes from QuestMoneyReward) and no Shang Xi's Academy reputation (faction 1216 isn't in 3.3.5a)
- The finale: F-020 / F-021's Pandaren already have their side, so the spirit of Master Shang Xi completes "A New Fate" (31450) and sends them to Stormwind or Orgrimmar (bound there) instead of MoP's faction choice, exit movie and Aysa / Ji waiting in the capitals
- Only the 256-bit flavour exists so far
- Generated: change the scripts, not the SQL
