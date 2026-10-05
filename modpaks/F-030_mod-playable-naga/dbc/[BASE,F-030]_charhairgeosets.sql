-- charhairgeosets: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Naga;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Male,   0, 1, 1),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Male,   1, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Male,   2, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Male,   3, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Male,   4, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Female, 0, 1, 1),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Female, 1, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Female, 2, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Female, 3, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Naga, @Female, 4, 5, 0);
