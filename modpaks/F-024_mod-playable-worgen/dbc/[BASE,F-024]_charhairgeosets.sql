-- charhairgeosets: 27 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Worgen;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,    9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,   10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Male,   11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female,  9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female, 10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female, 11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female, 12, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female, 13, 15, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Worgen, @Female, 14, 16, 0);
