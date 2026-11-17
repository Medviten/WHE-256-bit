/* Ensures that race-restricted items include Orcs (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @AllianceOrcMask,
    `allowablerace_2` = `allowablerace_2` | @AllianceOrcMask_2 WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
