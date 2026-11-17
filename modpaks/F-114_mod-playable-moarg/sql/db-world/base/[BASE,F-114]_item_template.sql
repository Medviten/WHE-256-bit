/* Ensures that race-restricted items include Mo'arg (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @MoargMask,
    `allowablerace_2` = `allowablerace_2` | @MoargMask_2 WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
