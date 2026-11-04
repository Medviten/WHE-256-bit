/* Ensures that race-restricted items include Cultists (as Undead) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @CultistMask,
    `allowablerace_2` = `allowablerace_2` | @CultistMask_2 WHERE `allowablerace` & @UndeadMask AND `allowablerace` != -1;
