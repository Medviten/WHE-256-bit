-- characterfacialhairstyles: 21 inserts, 0 updates, 0 deletes (stock Blood Elf)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Darkfallen;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Darkfallen, @Male,    0, 0, 0, 0, 0, 2),
(@Darkfallen, @Male,    1, 2, 0, 0, 0, 2),
(@Darkfallen, @Male,    2, 3, 0, 0, 0, 2),
(@Darkfallen, @Male,    3, 4, 0, 0, 0, 2),
(@Darkfallen, @Male,    4, 5, 0, 0, 0, 2),
(@Darkfallen, @Male,    5, 6, 0, 0, 0, 2),
(@Darkfallen, @Male,    6, 7, 0, 0, 0, 2),
(@Darkfallen, @Male,    7, 8, 0, 0, 0, 2),
(@Darkfallen, @Male,    8, 9, 0, 0, 0, 2),
(@Darkfallen, @Male,    9, 10, 0, 0, 0, 2),
(@Darkfallen, @Female,  0, 0, 0, 0, 0, 2),
(@Darkfallen, @Female,  1, 0, 2, 0, 0, 2),
(@Darkfallen, @Female,  2, 0, 3, 0, 0, 2),
(@Darkfallen, @Female,  3, 0, 4, 0, 0, 2),
(@Darkfallen, @Female,  4, 0, 5, 0, 0, 2),
(@Darkfallen, @Female,  5, 0, 6, 0, 0, 2),
(@Darkfallen, @Female,  6, 0, 7, 0, 0, 2),
(@Darkfallen, @Female,  7, 0, 8, 0, 0, 2),
(@Darkfallen, @Female,  8, 0, 9, 0, 0, 2),
(@Darkfallen, @Female,  9, 0, 10, 0, 0, 2),
(@Darkfallen, @Female, 10, 0, 11, 0, 0, 2);
