-- characterfacialhairstyles: 14 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @ThinHuman;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@ThinHuman, @Male,    0,  0,  0,  0,  0,  0),
(@ThinHuman, @Male,    1,  2,  0,  0,  0,  0),
(@ThinHuman, @Male,    2,  3,  0,  0,  0,  0),
(@ThinHuman, @Male,    3,  4,  0,  0,  0,  0),
(@ThinHuman, @Male,    4,  5,  0,  0,  0,  0),
(@ThinHuman, @Male,    5,  6,  0,  0,  0,  0),
(@ThinHuman, @Male,    6,  7,  0,  0,  0,  0),
(@ThinHuman, @Female,  0,  0,  0,  0,  0,  0),
(@ThinHuman, @Female,  1,  2,  0,  0,  0,  0),
(@ThinHuman, @Female,  2,  3,  0,  0,  0,  0),
(@ThinHuman, @Female,  3,  4,  0,  0,  0,  0),
(@ThinHuman, @Female,  4,  5,  0,  0,  0,  0),
(@ThinHuman, @Female,  5,  6,  0,  0,  0,  0),
(@ThinHuman, @Female,  6,  7,  0,  0,  0,  0);
