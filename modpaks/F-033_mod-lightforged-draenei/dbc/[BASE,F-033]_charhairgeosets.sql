-- charhairgeosets: 62 inserts, 0 updates, 6 deletes

-- New entries
DELETE FROM `charhairgeosets` WHERE `race` = @LightforgedDraenei;
SET @CharHairGeosetsID = (SELECT COALESCE(MAX(id), 0) FROM `charhairgeosets`);
INSERT INTO `charhairgeosets` (`id`, `race`, `gender`, `variation`, `geoset`, `show_scalp`) VALUES
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 0, 2, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 1, 3, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 7, 9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 8, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 9, 11, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 10, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 2, 4, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 3, 5, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 4, 6, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 5, 7, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 6, 8, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 7, 9, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 11, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 12, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 13, 15, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 14, 16, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Female, 15, 17, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 8, 0, 1),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 9, 10, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 11, 12, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 12, 13, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 13, 14, 0),
(@CharHairGeosetsID := @CharHairGeosetsID +1, @LightforgedDraenei, @Male, 10, 11, 0);
