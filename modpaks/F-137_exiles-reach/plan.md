# F-137 Exile's Reach: quest port plan

Decided 2026-11-19: port the Alliance (Captain Garrick) and Horde (Warlord Breka Grimaxe) chains, the class quests
and the Darkmaul Citadel dungeon. Scripted events become data and SmartAI, not ports of TrinityCore's C++
(`zone_exiles_reach.cpp`, 32 scripts, not in any local checkout). Source: TrinityCore's retail TDB 1210.26091.

## What the island has (TDB)

- 103 quests (QuestSortID 10424): one chain per faction (Alliance 54xxx-58xxx, Horde 59xxx), class quests for
  both, two dungeon quests, two repair quests. Objectives: 87 kill, 26 item, 16 object, 25 criteria tree
  (type 14: no 3.3.5a counterpart), 7 area trigger (type 19)
- 929 spawns: 443 unphased (done, `retail_spawns_port.py`), 357 in "See the Army of Undead" (13783), the rest in
  55 quest-stage phases (each companion NPC has a copy per stage)
- 32 C++ creature scripts, 18 SmartAI rows
- The intro (Warming Up, Stand Your Ground, Brace for Impact) runs on a ship transport (npe_transport_guid 29/30)

## Phasing without phase bits

The 55 phases need 48 different condition sets; a phasemask has 31 usable bits, and Alliance and Horde phases
can't share one (a player holding a bit sees every spawn with it). AzerothCore's object visibility conditions
(`conditions` source type 30, SourceGroup 0 creature / 1 object, SourceEntry the entry, SourceId the spawn guid)
are checked in `WorldObject::CanSeeOrDetect` per player. Each phased spawn gets its phase's conditions
(quest states, team) on its guid. Missing in the core: visibility is only rechecked when the player moves, so a
quest state change has to refresh it (core patch, stage 1).

## Quest givers

TrinityCore's TDB names starters / enders for only 30 quests (the parts it scripts). `retail_world_port.py` infers
35 more: the ender is the faction's quest giver within 25 yards of retail's turn-in marker, the starter the
previous quest's ender in the faction's quest lines (QuestLineXQuest 5366/5367 Alliance, 5369/5370 Horde). Still
without one (36): the ship intro (its NPCs stand on the transport), the class quests (their trainers are summoned),
Freeing the Light, Killclaw, Hrun's pit, Darkmaul's finale. Wowhead names them but blocks scripted reads; check its
quest pages by hand when curating these (stage 3).

## Stages

1. (Done 2026-11-19, untested in game) Core: refresh visibility on quest state changes. Generator
   (`retail_world_port.py`): quests (templates, givers and enders, texts, objectives as RequiredNpcOrGo /
   RequiredItem / exploration), phased spawns with visibility conditions, quest items and loot.
2. Story NPC looks: retail dresses them through CreatureDisplayInfoExtra (HD bakes on retail race models); first
   pass uses stock displays of the same race and sex
3. (Done 2026-11-19 as the simple version, untested) Every quest doable: Wowhead's givers / enders and map points
   (`--wowhead`), talk credits for scripted steps, quest chests, loot fixes. Left for a fuller pass: SmartAI for the
   scripted events (beach rescues, followers, the boar ride, prisoners, Hrun's pit, the final fight), creature
   texts, real spars and class ability checks instead of talk credits, Bloodbeak's ritual event
   - Scripts: TrinityCore's zone_exiles_reach.cpp ported to the core's exiles_reach.cpp (gameplay and dialogue; the
     ship and beach walk paths skipped). Texts: creature_text plus retail's broadcast texts (`--hotfixes`), spoken by
     id. Part 1 (2026-11-20, untested): the ships, the beach, the abandoned camp, Enhanced Combat Tactics. Part 2:
     Northbound, Taming the Wilds (teaches taming), the Briarpatch (Geolord, prisoners, quilboar, Gork; stock NPC
     spells for retail's). Part 3: the plains (the scouting copter as a taxi flight, SCOUT_FLIGHTS; the quests'
     lines; Torgok). Left: the re-sizer and the boar ride as retail plays them (an item on the boars, a vehicle:
     a kill and a talk credit for now), Westward Bound's companions, the ogres' TDB SmartAI (animkits, timed lists),
     Hrun's pit and Bloodbeak's ritual as events. Part 4: Tunk, Gor'groth, Hrun the Exiled and Bloodbeak fight with
     two stock NPC spells each (npc_er_boss)
4. (Done 2026-11-19, untested) Start: decided per race (player_race_template.exiles_reach, F-091; the user's list of
   races keeping their start is in the race modpaks); retail's forced first character was turned down. F-137 moves
   those races' playercreateinfo to the beach; `ExilesReachStartZone.Enable` boards them on their faction's sailing
   ship instead (decided: retail's moving ships, not a static one). Kalecgos sends players to their capital. Ships
   as continent transports on retail's paths, crews from TDB's deck maps 2261 / 2369, SmartAI for Warming Up / Stand Your Ground / Brace for Impact (the turn-in teleports to the beach; no crash scene)
5. Class quests (retail abilities replaced where 3.3.5a lacks them; Monk and Demon Hunter versions left out)
6. (Started 2026-11-19, untested) Darkmaul Citadel: terrain (map 2236, `[F-137,DC]` files), spawns, instance rows,
   portals in and out, Gor'groth's kill and Kalecgos' exit as the dungeon quest's credits. Open: boss mechanics, doors,
   An End to Beginnings (its givers are summoned at the end), the group finder
