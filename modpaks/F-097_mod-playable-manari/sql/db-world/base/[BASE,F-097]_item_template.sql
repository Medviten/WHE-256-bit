/* Ensures that race-restricted items include Manari (as BloodElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @ManariMask,
    `allowablerace_2` = `allowablerace_2` | @ManariMask_2 WHERE `allowablerace` & @BloodElfMask AND `allowablerace` != -1;
