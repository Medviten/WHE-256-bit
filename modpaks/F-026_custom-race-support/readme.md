# mod-worgoblin-high-elf
## F-026_custom-race-support

### Features
- Unified faction update
- Unified skill update
- Unified talent update
- Unified totem update
- Unified capital reputation spillover (requires the 256-bit core's `reputation_spillover_faction` table)
- `patches/core/race-templates.patch` (azerothcore-wotlk): replaces per-race core code with `player_race_template` (see
  F-091_race-setup), so races need no enum entries or recompile. It also creates races without a female model as male,
  and keeps a character or creature with a missing display from crashing the server
- `patches/playerbots/race-templates.patch` (mod-playerbots): the same for bots, using `player_race_template` and
  `playerbots_race_template`. A race missing `CharSections` rows gets appearance 0 for those instead of crashing

### Known Issues
- Racemasks with high defaults haven't all been incorporated yet
