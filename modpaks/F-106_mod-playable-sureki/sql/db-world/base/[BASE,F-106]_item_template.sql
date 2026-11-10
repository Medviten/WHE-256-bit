/* Ensures that race-restricted items include Sureki (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SurekiMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
