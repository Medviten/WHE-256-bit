/* Ensures that race-restricted items include Titans (as Dwarf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @TitanMask,
    `allowablerace_2` = `allowablerace_2` | @TitanMask_2 WHERE `allowablerace` & @DwarfMask AND `allowablerace` != -1;
