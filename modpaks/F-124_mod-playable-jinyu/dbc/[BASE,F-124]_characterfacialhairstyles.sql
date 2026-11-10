-- characterfacialhairstyles: 2 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 78)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Jinyu;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Jinyu, @Male,    0, 0, 0, 0, 0, 0),
(@Jinyu, @Female,  0, 0, 0, 0, 0, 0);
