/* Ensures that race-restricted items include Nerubians (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @NerubianMask,
    `allowablerace_2` = `allowablerace_2` | @NerubianMask_2 WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
