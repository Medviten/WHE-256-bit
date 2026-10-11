-- charhairgeosets: 25 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Taunka;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,    9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,   10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,   11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Male,   12, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female,  9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female, 10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Taunka, @Female, 11, 13, 0);
