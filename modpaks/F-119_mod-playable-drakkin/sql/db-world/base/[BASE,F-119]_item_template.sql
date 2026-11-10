/* Ensures that race-restricted items include Drakkin (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @DrakkinMask WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
