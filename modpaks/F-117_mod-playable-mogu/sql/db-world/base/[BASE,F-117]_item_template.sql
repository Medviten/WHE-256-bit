/* Ensures that race-restricted items include Mogu (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @MoguMask,
    `allowablerace_2` = `allowablerace_2` | @MoguMask_2 WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
