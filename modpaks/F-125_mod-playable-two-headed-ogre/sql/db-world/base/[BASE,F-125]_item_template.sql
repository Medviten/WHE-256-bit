/* Ensures that race-restricted items include Two-Headed Ogres (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @TwoHeadedOgreMask WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
