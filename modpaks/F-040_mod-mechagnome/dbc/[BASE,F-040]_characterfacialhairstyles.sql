-- characterfacialhairstyles: 7 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Mechagnome;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Mechagnome, @Male,    0,  0,  0,  0,  0,  0),
(@Mechagnome, @Male,    1,  2,  0,  0,  0,  0),
(@Mechagnome, @Male,    2,  3,  0,  0,  0,  0),
(@Mechagnome, @Male,    3,  4,  0,  0,  0,  0),
(@Mechagnome, @Male,    4,  5,  0,  0,  0,  0),
(@Mechagnome, @Male,    5,  6,  0,  0,  0,  0),
(@Mechagnome, @Female,  0,  0,  0,  0,  0,  0);
