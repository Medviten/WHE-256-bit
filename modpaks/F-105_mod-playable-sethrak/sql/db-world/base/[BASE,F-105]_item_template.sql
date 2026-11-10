/* Ensures that race-restricted items include Sethrak (as Human) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SethrakMask WHERE `allowablerace` & @HumanMask AND `allowablerace` != -1;
