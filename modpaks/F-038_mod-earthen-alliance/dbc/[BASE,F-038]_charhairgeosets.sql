-- charhairgeosets: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @AllianceEarthen;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceEarthen, @Male,    0,  0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @AllianceEarthen, @Female,  0,  0, 1);
