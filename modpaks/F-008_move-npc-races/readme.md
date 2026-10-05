# mod-worgoblin-high-elf
## F-008_move-npc-races

### Features
- Moves NPC races well above the playable range to make room for more playable races.

### Known Issues
- Not idempotent. Use with caution. (Should just fail to do anything if you run it twice, though.)
- Use unmodified DBCs! This will turn your ID 12 Worgen into whatever ID @NPCFelOrc is set to if you let it.
