# mod-worgoblin-high-elf
## F-045_mod-playable-furbolg

### Features
- Playable Furbolg (Alliance)
    - Model and textures from Project Reforged's playable Furbolg (`Character\Furbolg\FurbolgRace.m2`): one model
      for both genders
    - Customization: CoA's (see Look)
    - Home: Night Elf (classes, start position, action bars, stats, race-restricted quests and items); start
      outfits from Night Elf, other classes from the next Alliance race
    - Kin: Tauren (voice, emotes and names copied at build time, model data, helmet prefix)

### Look
Model, textures and customization from Ilusixn's CoA 1.9.9 release (CoA race 50), put in place by `tools/races/coa199_replace.py`. Author: Project Reforged; see `CREDITS.md` in the release, which must ship with these files.

### Known Issues
- No racial mount
- No hair or facial styles (the model has no geosets)
- No "no accessories" option (Project Reforged's transparent accessory texture is not available)
- Racial faction name and description are placeholders
- Uses Tauren helmet models (client prefix 'Ta'); helmet geosets are not adjusted

### CoA Custom 1.9 racials
- Active: learned with the racial skill line
- From CoA race 50 (Furbolg), renumbered; blocks at the end of `[BASE,F-045]_spell.sql`, `_skilllineability.sql` and `_spellicon.sql`
    - Ursine Fury: Increases your attack and casting speed by $s1% for $d. Does not stack with other similar cast speed increasing effects.
    - Thick Fur: Reduces the damage taken by Nature spells by $s1%.
    - Furbolg Endurance: Base Health increased by $s1%.
    - Gift of the Grove: Herbalism skill increased by $s1.
