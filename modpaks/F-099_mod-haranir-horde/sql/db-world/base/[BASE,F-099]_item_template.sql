/* Ensures that race-restricted items include Haranir (as Troll) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @HordeHaranirMask,
    `allowablerace_2` = `allowablerace_2` | @HordeHaranirMask_2 WHERE `allowablerace` & @TrollMask AND `allowablerace` != -1;
