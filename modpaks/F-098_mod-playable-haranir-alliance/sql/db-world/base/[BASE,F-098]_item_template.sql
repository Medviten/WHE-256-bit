/* Ensures that race-restricted items include Haranir (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @AllianceHaranirMask,
    `allowablerace_2` = `allowablerace_2` | @AllianceHaranirMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
