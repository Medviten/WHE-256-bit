-- characterfacialhairstyles: 8 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 50)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Furbolg;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Furbolg, @Male,    0, 2, 0, 0, 0, 0),
(@Furbolg, @Male,    1, 3, 0, 0, 0, 0),
(@Furbolg, @Male,    2, 4, 0, 0, 0, 0),
(@Furbolg, @Male,    3, 5, 0, 0, 0, 0),
(@Furbolg, @Male,    4, 6, 0, 0, 0, 0),
(@Furbolg, @Male,    5, 7, 0, 0, 0, 0),
(@Furbolg, @Male,    6, 8, 0, 0, 0, 0),
(@Furbolg, @Female,  0, 0, 0, 0, 0, 0);
