/* Ensures that race-restricted items include Elune's Chosen (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @EluneChosenMask,
    `allowablerace_2` = `allowablerace_2` | @EluneChosenMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
