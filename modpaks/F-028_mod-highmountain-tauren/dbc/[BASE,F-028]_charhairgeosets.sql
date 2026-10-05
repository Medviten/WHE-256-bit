-- charhairgeosets: 2 inserts, 0 updates, 0 deletes

-- New entries
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);

DELETE FROM `charhairgeosets` WHERE `race` = @HighmountainTauren;
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Male,   6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @HighmountainTauren, @Female, 6, 8, 0);