/* Ensures that race-restricted items include Stormforged (as Dwarf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @StormforgedMask WHERE `allowablerace` & @DwarfMask AND `allowablerace` != -1;
