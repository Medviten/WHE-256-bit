/* Ensures that race-restricted items include Skyborne (as BloodElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @HordeSkyborneMask,
    `allowablerace_2` = `allowablerace_2` | @HordeSkyborneMask_2 WHERE `allowablerace` & @BloodElfMask AND `allowablerace` != -1;
