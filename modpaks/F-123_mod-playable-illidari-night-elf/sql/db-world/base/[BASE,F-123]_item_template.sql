/* Ensures that race-restricted items include Illidari Night Elves (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @IllidariNightElfMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
