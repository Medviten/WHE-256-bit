/* Ensures that race-restricted items include Sethrak (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SethrakMask,
    `allowablerace_2` = `allowablerace_2` | @SethrakMask_2 WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
