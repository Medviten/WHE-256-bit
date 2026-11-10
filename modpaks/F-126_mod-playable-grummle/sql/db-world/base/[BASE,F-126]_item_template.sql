/* Ensures that race-restricted items include Grummles (as Dwarf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @GrummleMask WHERE `allowablerace` & @DwarfMask AND `allowablerace` != -1;
