/* Ensures that race-restricted items include Jinyu (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @JinyuMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
