-- characterfacialhairstyles: 12 inserts, 0 updates, 0 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = (@Taunka);
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Taunka, @Male,   0, 2, 0, 0, 0, 0),
(@Taunka, @Male,   1, 3, 0, 0, 0, 0),
(@Taunka, @Male,   2, 4, 0, 0, 0, 0),
(@Taunka, @Male,   3, 2, 0, 0, 0, 0),
(@Taunka, @Male,   4, 3, 0, 0, 0, 0),
(@Taunka, @Male,   5, 4, 0, 0, 0, 0),
(@Taunka, @Male,   6, 2, 0, 0, 0, 0),
(@Taunka, @Female, 0, 0, 0, 0, 0, 0),
(@Taunka, @Female, 1, 0, 0, 2, 0, 0),
(@Taunka, @Female, 2, 0, 0, 3, 0, 0),
(@Taunka, @Female, 3, 0, 0, 4, 0, 0),
(@Taunka, @Female, 4, 0, 0, 5, 0, 0);
