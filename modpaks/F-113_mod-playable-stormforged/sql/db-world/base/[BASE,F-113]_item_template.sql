/* Ensures that race-restricted items include Stormforged (as Dwarf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @StormforgedMask,
    `allowablerace_2` = `allowablerace_2` | @StormforgedMask_2 WHERE `allowablerace` & @DwarfMask AND `allowablerace` != -1;
