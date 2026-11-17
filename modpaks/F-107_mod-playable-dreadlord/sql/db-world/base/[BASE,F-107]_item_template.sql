/* Ensures that race-restricted items include Dreadlords (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @DreadlordMask,
    `allowablerace_2` = `allowablerace_2` | @DreadlordMask_2 WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
