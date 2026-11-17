/* Ensures that race-restricted items include Liches (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @LichMask,
    `allowablerace_2` = `allowablerace_2` | @LichMask_2 WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
