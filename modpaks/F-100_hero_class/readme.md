# mod-worgoblin-high-elf
## F-100_hero_class

### Features
- A playable Hero class (class id 10, which stock leaves unused), for every race, that can learn any class's spells
- Uses any class trainer. Spells are bought and level up as they do for the class itself
- Spends talent points in any class's trees, with the usual 71 points and tier rules. The talent frame gets a class picker
- Has mana, rage, energy and runic power at once. Each spell draws on its own, and extra bars appear below the player frame when they matter. Runes appear once a Death Knight spell is known
- Equips anything it has the skill for, including class-restricted items and any relic. Armor and weapon skills come from trainers and weapon masters, as for other classes
- Tames and summons pets of any kind
- Other classes aren't affected, and nor are characters on a client or server without the class

### Spells that aren't normally at a trainer
What a class starts with and what it gets from its quests are never on its trainers. Later ranks need the first, so `[BASE,F-100]_trainer.sql` adds both for free, in `trainer` rows 190000 + class, which only a Hero can reach. Examples: Fireball, Battle Stance, Summon Voidwalker, Tame Beast and Bear Form.

Class quests stay closed to a Hero, unlike quests for several classes. It doesn't need the shaman's four totems.

### Stats
Base stats, mana, crit, regeneration, and dodge and parry limits are Paladin's. Attack power is Paladin's plus 1 per Agility, and ranged attack power is Hunter's.

### Core patch
`patches/core/hero-class.patch` adds the class. build-patch.sh includes it in combined-core.patch while F-100 is in the manifest.

The client's spell modifier packets have no spell family, so `Player::AddSpellMod` adds one for a Hero, in a trailing field stock clients never see.

### Playerbots patch
`patches/playerbots/hero-class.patch` stops random bots from being created as Heroes, because no bot AI can play one.

### Client patch
`patches/client/hero-class.patch` applies to [wowdecomp-256-bit](https://github.com/Medviten/wowdecomp-256-bit), not yet to the original wowdecomp. It's required to play a Hero:
- Reads a Hero's spell modifiers per spell family. Without this, its talents don't show in tooltips and it can't cast a spell its talents made affordable
- `SetHeroTalentClass` and `GetHeroTalentClass`: shows one class's trees at a time in the stock talent frame
- `SetHeroSpellTabPage` and `GetHeroSpellTabPage`: pages the spellbook's tabs, of which the frame only has eight
- Opens class-restricted items, combo points, hunter pet handling, tracking and LFG roles to the class

### Interface files
Copy `interface/Interface` into your patch folder, or client root for the addon, then add this line to `Interface/GlueXML/GlueXML.toc`, above the `GlueLocalizationPost.xml` line:

```text
HeroClass_CharacterCreate.lua
```

- `Interface/GlueXML/HeroClass_CharacterCreate.lua`: an eleventh class button and the class's texts. It goes above the sixth button
- `Interface/AddOns/HeroClass`: the talent class picker, spellbook page arrows, extra resource bars and runes

### Known Issues
- Tentative and untested in game
- Item tooltips can still show a class-restricted item's class line in red, though the Hero can use it
- All classes share one combo point pool. Overpower closes its window by clearing it, so Overpower and rogue finishers interfere
- Only one form or stance applies at a time, as spells from different classes aren't meant to mix. Class-specific abilities can behave oddly together
- Item scripts and boss mechanics that pick by class (e.g. Nefarian's class calls, class trinkets) treat a Hero as no class

### Considerations
- Keep it after the race modpaks, F-002 and anything that moves a race's start in the manifest. It copies all of them
- Modelled on `mod-classless-wildcard` by Dustin Hendrickson (Esteria's fork), which converts a whole realm to one class, and on CoA's class 10. This modpak keeps the other classes and uses none of its code
