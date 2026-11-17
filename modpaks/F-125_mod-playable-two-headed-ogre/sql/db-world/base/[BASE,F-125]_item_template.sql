/* Ensures that race-restricted items include Two-Headed Ogres (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @TwoHeadedOgreMask,
    `allowablerace_2` = `allowablerace_2` | @TwoHeadedOgreMask_2 WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
