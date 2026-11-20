# mod-worgoblin-high-elf
## F-089_server-qol

### Features
- No fatigue in deep water (core patch; `DisableFatigue = 0` turns it off)
- New pet spells that need a target (Firebolt, Bite, Claw, ...) start on autocast, as on retail, so a new imp attacks when told to (core patch; `PetAutocastNewSpells = 0` turns it off)
- Higher limits on the `.modify speed` commands, `.modify mount` and `.modify scale` (core patch)
- Death knight Bloodworms stay defensive instead of pulling every mob in range (core patch)
- No DBC changes and nothing applied by build-dbc.sh, only the core patches

### Core patches
build-patch.sh includes the patches in combined-core.patch while F-089 is in the manifest. To leave one out, delete it from `patches/core`.
- `patches/core/no-fatigue.patch` adds the worldserver.conf setting `DisableFatigue`, with default 1. Set it to 0 for stock behaviour.
- `patches/core/gm-command-limits.patch` raises the highest speed from 50 to 100 for `.modify speed all`, `walk`, `backwalk`, `swim` and `fly` and for `.modify mount`, and widens `.modify scale` from 0.1-10 to 0.001-1000.
- `patches/core/pet-autocast.patch` adds the worldserver.conf setting `PetAutocastNewSpells`, with default 1. AzerothCore's imp never melees: it attacks only by autocasting Firebolt, and stock learns every pet spell with autocast off, so a new imp ignores Attack. Spells a pet already knows keep their saved setting (right-click to change it). Set it to 0 for stock behaviour.
- `patches/core/bloodworms-defensive.patch` fixes a stock bug: Bloodworms were meant to be defensive since 2017, but the guardian setup made them aggressive again right after, so they attacked any hostile creature in aggro range. They still attack the death knight's target and whatever attacks them or the death knight. No setting.
