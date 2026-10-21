-- charhairgeosets: 14 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Tuskarr;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    0,  1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Male,    6,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  0,  1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Tuskarr, @Female,  6,  7, 0);
