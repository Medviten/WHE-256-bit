/* Ensures that race-restricted items include Harpies (as Tauren) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @HarpyMask WHERE `allowablerace` & @TaurenMask AND `allowablerace` != -1;
