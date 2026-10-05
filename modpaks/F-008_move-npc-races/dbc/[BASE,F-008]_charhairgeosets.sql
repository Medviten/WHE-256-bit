-- [F-30] mod-worgoblin: charhairgeosets

DELETE FROM `charhairgeosets` WHERE `race` IN (@NPCFelOrc, @NPCNaga, @NPCBroken, @NPCSkeleton, @NPCVrykul, @NPCTuskarr, @NPCForestTroll, @NPCTaunka, @NPCNorthrendSkeleton, @NPCIceTroll);
UPDATE `charhairgeosets` SET `race` = @NPCFelOrc            WHERE `race` = 12;
UPDATE `charhairgeosets` SET `race` = @NPCNaga              WHERE `race` = 13;
UPDATE `charhairgeosets` SET `race` = @NPCBroken            WHERE `race` = 14;
UPDATE `charhairgeosets` SET `race` = @NPCSkeleton          WHERE `race` = 15;
UPDATE `charhairgeosets` SET `race` = @NPCVrykul            WHERE `race` = 16;
UPDATE `charhairgeosets` SET `race` = @NPCTuskarr           WHERE `race` = 17;
UPDATE `charhairgeosets` SET `race` = @NPCForestTroll       WHERE `race` = 18;
UPDATE `charhairgeosets` SET `race` = @NPCTaunka            WHERE `race` = 19;
UPDATE `charhairgeosets` SET `race` = @NPCNorthrendSkeleton WHERE `race` = 20;
UPDATE `charhairgeosets` SET `race` = @NPCIceTroll          WHERE `race` = 21;

/*
Original range:
247
264–265
294–295
297–299
301–302
304–307
314–325
327–334
435–436
438–444
*/
