/* Ensures that race-restricted items include Grummles (as Dwarf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @GrummleMask,
    `allowablerace_2` = `allowablerace_2` | @GrummleMask_2 WHERE `allowablerace` & @DwarfMask AND `allowablerace` != -1;
