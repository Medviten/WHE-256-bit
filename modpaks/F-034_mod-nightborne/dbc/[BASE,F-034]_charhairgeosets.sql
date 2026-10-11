-- charhairgeosets: 28 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Nightborne;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Male,   6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Nightborne, @Female, 6, 8, 0);