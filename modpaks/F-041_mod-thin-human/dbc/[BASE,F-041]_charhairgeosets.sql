-- charhairgeosets: 8 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @ThinHuman;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Male,    0,  0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Male,    1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Male,    2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Male,    3,  4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Female,  0,  0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Female,  1,  2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Female,  2,  3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @ThinHuman, @Female,  3,  4, 0);
