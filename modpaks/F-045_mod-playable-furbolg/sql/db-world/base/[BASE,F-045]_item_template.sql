/* Ensures that race-restricted items include Furbolgs (as Night Elves) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @FurbolgMask WHERE `allowablerace` & @NightElfMask AND `allowablerace` != -1;
