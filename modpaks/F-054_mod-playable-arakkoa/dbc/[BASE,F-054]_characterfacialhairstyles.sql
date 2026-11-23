-- characterfacialhairstyles: 8 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 79)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Arakkoa;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Arakkoa, @Male,    0, 1, 2, 2, 0, 0),
(@Arakkoa, @Male,    1, 2, 2, 2, 0, 0),
(@Arakkoa, @Male,    2, 3, 2, 2, 0, 0),
(@Arakkoa, @Male,    3, 4, 2, 2, 0, 0),
(@Arakkoa, @Male,    4, 5, 2, 2, 0, 0),
(@Arakkoa, @Female,  0, 2, 2, 3, 2, 2),
(@Arakkoa, @Female,  1, 4, 2, 3, 2, 2),
(@Arakkoa, @Female,  2, 5, 2, 3, 2, 2);
