-- characterfacialhairstyles: 15 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @LightforgedDraenei;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@LightforgedDraenei, @Male,   0, 1, 0, 0, 0, 0),
(@LightforgedDraenei, @Male,   1, 2, 0, 0, 0, 0),
(@LightforgedDraenei, @Male,   2, 3, 0, 2, 0, 0),
(@LightforgedDraenei, @Male,   3, 4, 0, 3, 0, 0),
(@LightforgedDraenei, @Male,   4, 5, 0, 4, 0, 0),
(@LightforgedDraenei, @Male,   5, 6, 0, 5, 0, 0),
(@LightforgedDraenei, @Male,   6, 7, 0, 6, 0, 0),
(@LightforgedDraenei, @Male,   7, 8, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 0, 2, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 1, 3, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 2, 4, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 3, 5, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 4, 6, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 5, 7, 0, 0, 0, 0),
(@LightforgedDraenei, @Female, 6, 8, 0, 0, 0, 0);
