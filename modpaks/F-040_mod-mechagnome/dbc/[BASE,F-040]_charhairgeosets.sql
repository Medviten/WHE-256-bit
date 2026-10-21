-- charhairgeosets: 16 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Mechagnome;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    0,  1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Male,    6,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  0,  1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  4,  5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  5,  6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  6,  7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  7,  8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Mechagnome, @Female,  8,  9, 0);
