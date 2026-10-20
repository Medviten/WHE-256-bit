-- charhairgeosets: 11 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Vrykul;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Male,    0,  0, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Male,    1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Male,    2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Male,    3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Male,    4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Male,    5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Female,  0,  0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Female,  1,  1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Female,  2,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Female,  3,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Vrykul, @Female,  4,  4, 0);
