/* Ensures that race-restricted items include Illidari Night Elves (as NightElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @IllidariNightElfMask,
    `allowablerace_2` = `allowablerace_2` | @IllidariNightElfMask_2 WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
