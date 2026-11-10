-- charhairgeosets: 2 inserts, 0 updates, 0 deletes (from the skin colours (option 0) of CoA's appearance catalog EsteriaDreadlord.bin)

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @Dreadlord;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Dreadlord, @Male,    0,  0, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @Dreadlord, @Female,  0,  0, 0);
