-- charhairgeosets: 2 inserts, 0 updates, 0 deletes (donor client: one bald style, no scalp)

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Murloc;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Murloc, @Male,   0, 0, 0),
(@CharHairGeosetsID := @CharHairGeosetsID + 1, @Murloc, @Female, 0, 0, 0);
