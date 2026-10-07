-- [F-30] mod-worgoblin: vocaluisounds
-- Moving Skeleton entry to the new race id (25) – the others aren't really needed

UPDATE `vocaluisounds` SET `race_id` = @NPCGoblin            WHERE `race_id` =  9;
UPDATE `vocaluisounds` SET `race_id` = @NPCFelOrc            WHERE `race_id` = 12;
UPDATE `vocaluisounds` SET `race_id` = @NPCNaga              WHERE `race_id` = 13;
UPDATE `vocaluisounds` SET `race_id` = @NPCBroken            WHERE `race_id` = 14;
UPDATE `vocaluisounds` SET `race_id` = @NPCSkeleton          WHERE `race_id` = 15;
UPDATE `vocaluisounds` SET `race_id` = @NPCVrykul            WHERE `race_id` = 16;
UPDATE `vocaluisounds` SET `race_id` = @NPCTuskarr           WHERE `race_id` = 17;
UPDATE `vocaluisounds` SET `race_id` = @NPCForestTroll       WHERE `race_id` = 18;
UPDATE `vocaluisounds` SET `race_id` = @NPCTaunka            WHERE `race_id` = 19;
UPDATE `vocaluisounds` SET `race_id` = @NPCNorthrendSkeleton WHERE `race_id` = 20;
UPDATE `vocaluisounds` SET `race_id` = @NPCIceTroll          WHERE `race_id` = 21;

-- race_id: 848
