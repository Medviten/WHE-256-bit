# mod-worgoblin-high-elf
## F-005_mod-azerothcore-high-elf

### Features
- Playable High Elves
    - Racial abilities (based on TurtleWoW's)
        - Enchanting bonus nerfed (identical to Blood Elf bonus)
    - Racial faction: High Elven Loyalists

### Known Issues
- Blood Elf voices reference things like going to Undercity and flying bats
- Racials have no animation

### CoA Custom 1.9 racials
- Commented out (the race already has racials); remove the comment markers in the CoA blocks to use them
- From CoA race 14 (High Elf), renumbered; blocks at the end of `[BASE,F-005]_spell.sql`, `_skilllineability.sql` and `_spellicon.sql`
    - Quel'dorei Torrent: Silence all enemies within $a1 yards for $d and restores $81002s3% of your Mana, ${$81002m2/10)} Rage$?s805000[, $81002s1 Focus,][] and $81002s1 Energy. Non-player victim spellcasting is also interrupted for $32747d.
    - Farstrider's Step: Escape the effects of any immobilization or movement speed reduction effect and become immune to them for $81001d.
    - Arcane Acuity: Intellect increased by $s1%.
    - Magic Resistance: Reduces the damage taken by Arcane spells by $s1%.
