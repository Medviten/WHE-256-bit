/* Ensures that race-restricted items include Lost Ones (as Draenei) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @LostOneMask WHERE `allowablerace` & @DraeneiMask AND `allowablerace` != -1;
