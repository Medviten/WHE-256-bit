/* Ensures that race-restricted items include Sporelings (as Gnome) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @SporelingMask WHERE `allowablerace` & @GnomeMask AND `allowablerace` != -1;
