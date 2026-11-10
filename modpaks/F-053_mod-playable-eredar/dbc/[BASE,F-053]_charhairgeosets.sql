-- charhairgeosets: 26 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 55)

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Eredar;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    0,  2, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    7,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,    9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,   10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,   11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Male,   12, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  0,  1, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  6,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  7,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  8,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female,  9, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female, 10, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female, 11, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Eredar, @Female, 12, 13, 0);
