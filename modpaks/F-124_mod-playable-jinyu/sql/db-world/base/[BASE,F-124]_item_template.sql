/* Ensures that race-restricted items include Jinyu (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @JinyuMask,
    `allowablerace_2` = `allowablerace_2` | @JinyuMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
