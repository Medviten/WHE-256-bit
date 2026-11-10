/* Ensures that race-restricted items include Illidari Blood Elves (as BloodElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @IllidariBloodElfMask WHERE `allowablerace` & @BloodElfMask AND `allowablerace` != -1;
