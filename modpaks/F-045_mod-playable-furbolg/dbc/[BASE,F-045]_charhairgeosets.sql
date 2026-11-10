-- charhairgeosets: 32 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 50)

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Furbolg;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,   10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,   11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,   12, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,   13, 15, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,   14, 16, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,   15, 17, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female, 10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female, 11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female, 12, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female, 13, 15, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female, 14, 16, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female, 19, 21, 0);
