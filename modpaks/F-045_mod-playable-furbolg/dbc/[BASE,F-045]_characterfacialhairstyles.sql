-- characterfacialhairstyles: 2 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Furbolg;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Furbolg, @Male,    0,  0,  0,  0,  0,  0),
(@Furbolg, @Female,  0,  0,  0,  0,  0,  0);
