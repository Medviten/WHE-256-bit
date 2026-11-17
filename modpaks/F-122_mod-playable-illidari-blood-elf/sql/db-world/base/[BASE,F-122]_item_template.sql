/* Ensures that race-restricted items include Illidari Blood Elves (as BloodElf) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @IllidariBloodElfMask,
    `allowablerace_2` = `allowablerace_2` | @IllidariBloodElfMask_2 WHERE `allowablerace` & @BloodElfMask AND `allowablerace` != -1;
