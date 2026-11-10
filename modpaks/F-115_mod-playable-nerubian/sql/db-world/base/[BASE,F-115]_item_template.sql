/* Ensures that race-restricted items include Nerubians (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @NerubianMask WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
