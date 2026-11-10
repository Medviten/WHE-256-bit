/* Ensures that race-restricted items include Orcs (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @AllianceOrcMask WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
