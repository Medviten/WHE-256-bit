/* Ensures that race-restricted items include Dreadlords (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @DreadlordMask WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
