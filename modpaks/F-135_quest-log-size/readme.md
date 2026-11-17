# mod-worgoblin-high-elf
## F-135_quest-log-size

### Features
- The quest log holds up to 255 quests instead of 25. The worldserver.conf setting `Quests.LogSize` (25-255) sets how many a character can take
- Needs the core patch, a recompile, and a client that has the client patch. Nothing goes through build-dbc.sh
- The quest log window shows the server's limit (`Quests: 30/255`), with the interface patch
- Playerbots and ALE (Eluna) know about the larger log, with their patches

### How it works
The quest log is part of the player's update fields: 25 slots of 5 fields each. Slots 0-24 keep their stock fields. Slots 25-254 get 1150 new fields after the last stock player field (`PLAYER_QUEST_LOG_EXT_1_1`), followed by `PLAYER_QUEST_LOG_SIZE`, which tells the client the current `Quests.LogSize`. No stock field moves. The new fields are private: only the character's own client receives them, and every other player still gets the stock-sized update.

A character's own update grows from 42 to 78 mask blocks. A stock `Wow.exe`, or a client without the client patch, rejects that, so **every player needs the patched client once the core patch is in**, even with `Quests.LogSize = 25`. The patched client still works on a stock server.

### Core patch
`patches/core/quest-log-size.patch` raises `MAX_QUEST_LOG_SIZE` to 255 and adds the extended fields. It also adds `Quests.LogSize`, which defaults to 255 in the patch. Set it to 25 for the stock log size. The setting is reloadable. If you lower it, characters keep the quests they already have, but can't take new ones until they are below the limit.

The default branch of [azerothcore-wotlk-256-bit](https://github.com/Medviten/azerothcore-wotlk-256-bit) already includes this patch, with `Quests.LogSize = 25`.

### Playerbots patch
`patches/playerbots/quest-log-size.patch` makes the bots count their free quest slots against `Quests.LogSize`. Without it, the core patch still compiles, but bots think they have 255 slots. With a high `Quests.LogSize`, bots take that many quests, so lower it if that's too many for your bots.

### ALE patch
`patches/ale/quest-log-size.patch` is for [mod-ale](https://github.com/azerothcore/mod-ale) (`mod-ale-256-bit`). `player:GetQuestSlotQuestId(255)` would otherwise read past the last field and stop the server on an assert. build-patch.sh writes it to `combined-ale.patch`; apply it from the mod-ale folder.

### Client patch
`patches/client/quest-log-size.patch` applies to the original wowdecomp (moostigre's); [wowdecomp-256-bit](https://github.com/Medviten/wowdecomp-256-bit) already includes it. It's required as soon as the core patch is in (see above). It:
- Accepts the larger update and stores slots 25-254
- Shows every quest in the quest log, quest tracking, the map's quest POIs, quest item looting and quest-related objects
- Fires `QUEST_LOG_UPDATE`, `QUEST_ACCEPTED` and `UNIT_QUEST_LOG_CHANGED` for the new slots
- Adds the Lua function `GetQuestLogCapacity()`: the server's `Quests.LogSize`, or 25 on a server without this patch

### Interface patch
The stock interface assumes 25 quests in two places, so it needs `patches/interface/quest-log-capacity.patch`:
- `QuestLogFrame.lua`: the quest count says `x/25`. With the patch it shows `GetQuestLogCapacity()`
- `UIParent.lua`: a quest shared by a party member, or an escort quest, can't be accepted with 25 quests or more; the popup says the log is full. With the patch the limit is `GetQuestLogCapacity()`

Both fall back to 25 on a client without `GetQuestLogCapacity()`. To install it, extract the stock `Interface/FrameXML/QuestLogFrame.lua` and `UIParent.lua` from your client (`Data/enUS/patch-enUS-3.MPQ` on a patched client), put them in the same paths in your patch folder, and apply the patch from that folder's root:

```text
git apply --ignore-space-change --ignore-whitespace quest-log-capacity.patch
```

### Limitations
- Only the first 25 zone headers in the quest log can be collapsed; later ones stay open. The client saves their state in a 25-bit CVar
- `IsUnitOnQuest` (quest progress shown for party members) only sees a party member's first 25 quests
- Quest tracking is still limited to 25 tracked quests
- A 32-bit flavour (WHE-32-bit) doesn't exist yet
