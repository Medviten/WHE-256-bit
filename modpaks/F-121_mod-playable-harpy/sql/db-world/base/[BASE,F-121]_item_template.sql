/* Ensures that race-restricted items include Harpies (as Tauren) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @HarpyMask,
    `allowablerace_2` = `allowablerace_2` | @HarpyMask_2 WHERE `allowablerace` & @TaurenMask AND `allowablerace` != -1;
