/* Ensures that race-restricted items include Titans (as Dwarf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @TitanMask WHERE `allowablerace` & @DwarfMask AND `allowablerace` != -1;
