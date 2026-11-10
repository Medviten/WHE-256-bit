/* Ensures that race-restricted items include Mogu (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @MoguMask WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
