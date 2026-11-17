/* Ensures that race-restricted items include Saberon (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SaberonMask,
    `allowablerace_2` = `allowablerace_2` | @SaberonMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
