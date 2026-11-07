/* Ensures that race-restricted items include Skyborne (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @AllianceSkyborneMask,
    `allowablerace_2` = `allowablerace_2` | @AllianceSkyborneMask_2 WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
