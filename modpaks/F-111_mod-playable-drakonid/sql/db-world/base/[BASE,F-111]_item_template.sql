/* Ensures that race-restricted items include Drakonid (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @DrakonidMask WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
