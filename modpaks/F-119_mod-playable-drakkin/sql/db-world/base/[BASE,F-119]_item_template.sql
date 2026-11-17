/* Ensures that race-restricted items include Drakkin (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @DrakkinMask,
    `allowablerace_2` = `allowablerace_2` | @DrakkinMask_2 WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
