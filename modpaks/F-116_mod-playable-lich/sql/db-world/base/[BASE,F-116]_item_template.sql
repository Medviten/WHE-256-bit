/* Ensures that race-restricted items include Liches (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @LichMask WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
