/* Ensures that race-restricted items include Fungarians (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @FungarianMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
