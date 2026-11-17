/* Ensures that race-restricted items include Drakonid (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @DrakonidMask,
    `allowablerace_2` = `allowablerace_2` | @DrakonidMask_2 WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
