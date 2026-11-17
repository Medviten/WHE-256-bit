/* Ensures that race-restricted items include Sureki (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SurekiMask,
    `allowablerace_2` = `allowablerace_2` | @SurekiMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
