-- characterfacialhairstyles: 18 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Tuskarr;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Tuskarr, @Male,    0,  0,  0,  0,  0,  0),
(@Tuskarr, @Male,    1,  1,  0,  0,  0,  0),
(@Tuskarr, @Male,    2,  2,  0,  0,  0,  0),
(@Tuskarr, @Male,    3,  3,  0,  0,  0,  0),
(@Tuskarr, @Male,    4,  4,  0,  0,  0,  0),
(@Tuskarr, @Male,    5,  5,  0,  0,  0,  0),
(@Tuskarr, @Male,    6,  6,  0,  0,  0,  0),
(@Tuskarr, @Male,    7,  7,  0,  0,  0,  0),
(@Tuskarr, @Male,    8,  8,  0,  0,  0,  0),
(@Tuskarr, @Female,  0,  0,  0,  0,  0,  0),
(@Tuskarr, @Female,  1,  1,  0,  0,  0,  0),
(@Tuskarr, @Female,  2,  2,  0,  0,  0,  0),
(@Tuskarr, @Female,  3,  3,  0,  0,  0,  0),
(@Tuskarr, @Female,  4,  4,  0,  0,  0,  0),
(@Tuskarr, @Female,  5,  5,  0,  0,  0,  0),
(@Tuskarr, @Female,  6,  6,  0,  0,  0,  0),
(@Tuskarr, @Female,  7,  7,  0,  0,  0,  0),
(@Tuskarr, @Female,  8,  8,  0,  0,  0,  0);
