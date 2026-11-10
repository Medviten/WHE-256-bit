/* Ensures that race-restricted items include Saberon (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SaberonMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
