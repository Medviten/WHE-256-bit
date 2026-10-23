-- charhairgeosets: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Furbolg;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Male,    0,  1, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Furbolg, @Female,  0,  1, 0);
