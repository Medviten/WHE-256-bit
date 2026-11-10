-- charhairgeosets: 25 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 52)

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @AllianceOrc;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    0,  0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    6,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    7,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    8,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,    9, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,   10, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Male,   11, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  0,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  1,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  2,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  3,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  4,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  5,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  6,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  7,  0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  8,  9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female,  9, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female, 10, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female, 11, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceOrc, @Female, 12, 13, 0);
