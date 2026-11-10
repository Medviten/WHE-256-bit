-- charhairgeosets: 24 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 61)

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @IllidariNightElf;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    0,  1, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    6,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    7,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    8,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,    9, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,   10, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Male,   11, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  0,  1, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female,  9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female, 10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @IllidariNightElf, @Female, 11, 13, 0);
