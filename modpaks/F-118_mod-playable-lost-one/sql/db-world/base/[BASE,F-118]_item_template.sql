/* Ensures that race-restricted items include Lost Ones (as Draenei) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @LostOneMask,
    `allowablerace_2` = `allowablerace_2` | @LostOneMask_2 WHERE `allowablerace` & @DraeneiMask AND `allowablerace` != -1;
