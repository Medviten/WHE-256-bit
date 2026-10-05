-- [F-002] move_npc_races: characterfacialhairstyles

DELETE FROM `characterfacialhairstyles` WHERE `race` IN (@NPCFelOrc, @NPCNaga, @NPCBroken, @NPCSkeleton, @NPCVrykul, @NPCTuskarr, @NPCForestTroll, @NPCTaunka, @NPCNorthrendSkeleton, @NPCIceTroll);
UPDATE `characterfacialhairstyles` SET `race` = @NPCFelOrc            WHERE `race` = 12;
UPDATE `characterfacialhairstyles` SET `race` = @NPCNaga              WHERE `race` = 13;
UPDATE `characterfacialhairstyles` SET `race` = @NPCBroken            WHERE `race` = 14;
UPDATE `characterfacialhairstyles` SET `race` = @NPCSkeleton          WHERE `race` = 15;
UPDATE `characterfacialhairstyles` SET `race` = @NPCVrykul            WHERE `race` = 16;
UPDATE `characterfacialhairstyles` SET `race` = @NPCTuskarr           WHERE `race` = 17;
UPDATE `characterfacialhairstyles` SET `race` = @NPCForestTroll       WHERE `race` = 18;
UPDATE `characterfacialhairstyles` SET `race` = @NPCTaunka            WHERE `race` = 19;
UPDATE `characterfacialhairstyles` SET `race` = @NPCNorthrendSkeleton WHERE `race` = 20;
UPDATE `characterfacialhairstyles` SET `race` = @NPCIceTroll          WHERE `race` = 21;
