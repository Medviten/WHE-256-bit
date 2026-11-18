# mod-worgoblin-high-elf
## F-029_all-trainers

### Features
- All class trainers in all stock capitals
- Class trainers in the stock starting areas for the classes those zones lack (spawns from mod-uac)
- Class trainers in the second towns (Goldshire, Kharanos, Dolanaar, Azure Watch, Razor Hill, Bloodhoof Village, Brill, Falconwing Square) for the classes those towns lack, 25 in all: Cataclysm's own trainers for its new race/class pairs where it had one (Benjamin Foxworthy, Halbin Frosthammer, Jabul, Seer Alsoomse, Sunwalker Iopi, Dedlow Wormwood, Lothan Silverblade; from Neltharion, at their Cataclysm spots, with the trainer list and gossip of a stock trainer of their class), and for the rest new NPCs (`[F-029]_second_town_trainers.sql`), each a copy of a stock trainer of the same class and faction (look, gossip, trainer list, none of its quests) under a new name, beside a stock trainer of the town. They also start their faction's level 10-20 class breadcrumbs to the capital trainers, as the stock second-town trainers of their class do (`[F-029]_second_town_quests.sql`). Goldshire's and Brill's hunter trainers give a Taming the Beast chain of their own on the zone's beasts (`zz_[I-381]_hunter_taming.sql`, `dbc/[I-381]_*`; Stonetusk Boar, Forest Spider, Young Forest Bear / Greater Duskbat, Vicious Night Web Spider, Worg), built like F-013's Kezan chain, for Tame Beast and Beast Training
- Mage and warlock trainers in Teldrassil for Worgen, if F-024 is in the manifest (their displays are in its DBCs)
- Sets `@AllTrainersEnabled` (`variables.sql`), so other modpaks can add trainers for the classes their zones lack: F-130 puts a paladin and a shaman trainer in Gilneas, F-013 a paladin and a druid trainer in Kezan and the Lost Isles, F-134 its paladin, warlock and druid trainers on the Wandering Isle
- Cataclysm's class practice quests in the eight stock starting areas (below)
- The transmog NPCs it used to spawn are in F-131_transmog-npcs now

### Cataclysm class quests
Cataclysm's level-3 quests in which the class trainer teaches a spell and the player practises it on a training dummy or heals a wounded NPC, from [Project Neltharion](https://github.com/ProjectNeltharion)'s 4.3.4 world database (`zz_[AUTO,F-029]_*.sql`, `dbc/`): 48 quests in Northshire, Coldridge Valley, Deathknell, Camp Narache, the Valley of Trials, Shadowglen, Ammen Vale and Sunstrider Isle, with their dummies and wounded NPCs (Wounded Trainee, Militia, Sentinel, Deathguard, Brave, Darkspear Watcher) and their spawns.
- Echo Isles' priest and druid quests are moved to the Valley of Trials, which Cataclysm left without them; its druid trainer is Zen'tabra, Echo Isles' troll druid, in place of the tauren Gart Mistrunner. New Tinkertown's and Echo Isles' other quests aren't ported: Coldridge Valley and the Valley of Trials have the same class's quest already
- The quest giver is the trainer of the quest's class who stands in that area here, stock's or this modpak's (the counterparts of Cataclysm's new race/class trainers); the texts name that trainer. The modpak reuses stock trainer entries, so a zone condition keeps each trainer to its own area's quest. Where two trainers can stand at a spot (Shadowglen's mage, a Gilnean one under F-024), the text says "your trainer"
- Open to every race of the area's faction (a team condition, race mask 0, so F-002's update that opens class quests to both factions leaves them alone), so ARAC's and the custom races' characters get them too; one quest per class (ExclusiveGroup). Cataclysm's prerequisite letters and follow-up quests mostly aren't here, so the quests have neither
- As F-013's Kezan quests ([I-273]): level 4, and the spells 3.3.5a trains far above it become ones the trainers teach at 4: Serpent Sting for Steady Shot, Frostbolt for Arcane Missiles, Lesser Heal for Flash Heal, Earth Shock for Primal Strike (Cataclysm-only). Texts that describe the old spell are rewritten. Every rank of the spell gives credit
- Credit is SmartAI on the dummies and wounded NPCs (AzerothCore has no "cast spell on NPC" objective); Neltharion's own SmartAI on them is left out. The dummies use F-013's core script `npc_zep_training_dummy` (no damage, keeps SmartAI)
- The WotLK priest "Garments of ..." quests, which Cataclysm replaced with Healing the Wounded, are no longer offered; their "In Favor of ..." breadcrumbs to the first town's priest trainer stay

Requirements:
- The core's `npc_zep_training_dummy` (F-013's `goblin-start.patch`; the 256-bit core has it). Without it the dummies take damage and can die. The taming rods need that patch's rod fallback (I-376), which no longer depends on `GoblinStartZone.Enable`
- Client assets: the wounded NPCs' bakes, `Textures\BakedNpcTextures\CreatureDisplayExtra-*.blp` (the `texture` column of `dbc/[F-029]_creaturedisplayinfoextra.sql`), are in WHE-common, from the 4.3.4 client's art.MPQ

Updating: the `zz_[AUTO,F-029]_*.sql` files and `dbc/` are generated: `python tools/races/cata_class_quests_port.py <world.sql> modpaks/F-029_all-trainers` (Neltharion's `source/sql/base/world.zip`, unpacked; the base world SQL of `azerothcore-wotlk-256-bit` says which trainers stand where, `--acore` to point elsewhere). It replaces only those files; the rest of the modpak is hand-written. It reuses F-130's `cata_gilneas_port.py` for the row conversion. Text fixes, swapped spells and the transplanted quests are at the top of the script. `tools/checks/f013_item_assets.py --modpak modpaks/F-029_all-trainers --art <art.MPQ>` checks the item art.

### Known Issues
- Not yet compatible with the Open Azeroth modpack
- The class quests aren't tried in game or loaded into a database yet. Their spawn heights are Cataclysm's: Neltharion's dummies and wounded NPCs stand where they did in 4.3.4, which may float or sink a little on 3.3.5a or Open Azeroth terrain. The Valley of Trials' Darkspear Watchers are placed three yards from its dummies
- The class quests are 256-bit only so far
