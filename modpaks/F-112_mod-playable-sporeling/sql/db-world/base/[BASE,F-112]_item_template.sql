/* Ensures that race-restricted items include Sporelings (as Gnome) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SporelingMask,
    `allowablerace_2` = `allowablerace_2` | @SporelingMask_2 WHERE `allowablerace` & @GnomeMask AND `allowablerace` != -1;
