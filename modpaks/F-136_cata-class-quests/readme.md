# mod-worgoblin-high-elf
## F-136_cata-class-quests

### Features
- Cataclysm's class practice quests in the eight stock starting areas (Northshire, Coldridge Valley, Deathknell, Camp Narache, the Valley of Trials, Shadowglen, Ammen Vale, Sunstrider Isle), from [Project Neltharion](https://github.com/ProjectNeltharion)'s 4.3.4 world database: 48 quests in which the class trainer teaches a spell and the player practises it on a training dummy or heals a wounded NPC
- The dummies and wounded NPCs (Wounded Trainee, Militia, Sentinel, Deathguard, Brave, Darkspear Watcher) with their spawns
- Echo Isles' priest and druid quests are moved to the Valley of Trials, which Cataclysm left without them; its druid trainer is Zen'tabra, Echo Isles' troll druid, in place of F-029's tauren Gart Mistrunner. New Tinkertown's and Echo Isles' other quests aren't ported: Coldridge Valley and the Valley of Trials have the same class's quest already

### How it differs from Cataclysm
- The quest giver is the trainer of the quest's class who stands in that area here, stock's or F-029's (F-029 places the counterparts of Cataclysm's new race/class trainers, so it's required); the texts name that trainer. F-029 reuses stock trainer entries, so a zone condition keeps each trainer to its own area's quest. Where two trainers can stand at a spot (Shadowglen's mage, which F-029 replaces with a Gilnean one under F-024), the text says "your trainer"
- Open to the area's whole faction (config.sql masks), not one race, so ARAC's and the custom races' characters get them too, and one quest per class (ExclusiveGroup). Cataclysm's prerequisite letters and follow-up quests mostly aren't here, so the quests have neither
- As F-013's Kezan quests ([I-273]): level 4, and the spells 3.3.5a trains far above it become ones the trainers teach at 4: Serpent Sting for Steady Shot, Frostbolt for Arcane Missiles, Lesser Heal for Flash Heal, Earth Shock for Primal Strike (Cataclysm-only). Texts that describe the old spell are rewritten. Every rank of the spell gives credit
- Credit is SmartAI on the dummies and wounded NPCs (AzerothCore has no "cast spell on NPC" objective); Neltharion's own SmartAI on them is left out. The dummies use F-013's core script `npc_zep_training_dummy` (no damage, keeps SmartAI)

### Requirements
- F-029_all-trainers. Keep F-136 after it and after F-002 (whose update opens every class quest to every race, both factions), and before F-010: it replaces one of F-029's spawns, and F-010's move scripts relocate the Ammen Vale and Sunstrider Isle dummies with the rest of those areas
- The core's `npc_zep_training_dummy` (F-013's `goblin-start.patch`; the 256-bit core has it). Without it the dummies take damage and can die
- Client assets: the wounded NPCs' bakes, `Textures\BakedNpcTextures\CreatureDisplayExtra-*.blp` (the `texture` column of `dbc/[F-136]_creaturedisplayinfoextra.sql`), are in WHE-common, from the 4.3.4 client's art.MPQ

### Updating
The SQL is generated: `python tools/races/cata_class_quests_port.py <world.sql> modpaks/F-136_cata-class-quests` (Neltharion's `source/sql/base/world.zip`, unpacked; the base world SQL of `azerothcore-wotlk-256-bit` says which trainers stand where, `--acore` to point elsewhere). It reuses F-130's `cata_gilneas_port.py` for the row conversion. Text fixes, swapped spells and the transplanted quests are at the top of the script. `tools/checks/f013_item_assets.py --modpak modpaks/F-136_cata-class-quests --art <art.MPQ>` checks the item art.

### Known Issues
- Not tried in game or loaded into a database yet
- The spawn heights are Cataclysm's: Neltharion's dummies and wounded NPCs stand where they did in 4.3.4, which may float or sink a little on 3.3.5a or Open Azeroth terrain. The Valley of Trials' Darkspear Watchers are placed three yards from its dummies
- Only the starting areas' quests; Cataclysm's other starting-area changes (Northshire's and Coldridge's new chains) aren't part of it
- 256-bit only so far
