/* Ensures that race-restricted items include Dracthyr (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @HordeDracthyrMask,
    `allowablerace_2` = `allowablerace_2` | @HordeDracthyrMask_2 WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
