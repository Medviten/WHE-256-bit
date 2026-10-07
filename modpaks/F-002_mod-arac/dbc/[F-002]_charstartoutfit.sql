-- [F-002] mod-arac: charstartoutfit: 0 inserts, 1 updates, 0 deletes

SET @CharStartOutfitID = (SELECT COALESCE(MAX(id), 0) FROM `charstartoutfit`);
-- New entries for stock races only (custom ones are in their modpaks)
UPDATE `charstartoutfit` SET 
    `item_7`         = @LightQuiverItem,
    `item_8`         = @WeatheredCrossbowItem,
    `item_9`         = @RoughArrowItem,
    `display_item_7` = @LightQuiverItemDisplay,
    `display_item_8` = @WeatheredCrossbowItemDisplay,
    `display_item_9` = @RoughArrowItemItemDisplay
WHERE `race` IN (@Human, @NightElf, @Undead) AND `class` = @Hunter AND `display_item_8` = @OldBlunderbussItemDisplay;
