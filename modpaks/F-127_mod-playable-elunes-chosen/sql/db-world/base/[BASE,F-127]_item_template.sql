/* Ensures that race-restricted items include Elune's Chosen (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @EluneChosenMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
