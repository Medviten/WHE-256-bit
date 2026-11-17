/* Ensures that race-restricted items include Fungarians (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @FungarianMask,
    `allowablerace_2` = `allowablerace_2` | @FungarianMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
