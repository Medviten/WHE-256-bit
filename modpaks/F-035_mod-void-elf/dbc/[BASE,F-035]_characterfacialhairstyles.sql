-- characterfacialhairstyles: 13 inserts, 0 updates, 0 deletes
-- Male: none, then beards (geoset group 1: 102-108). Female: geoset group 3 (2-5). Only geosets the models have.

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @VoidElf;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@VoidElf, @Male,    0, 0, 0, 0, 0, 0),
(@VoidElf, @Male,    1, 2, 0, 0, 0, 0),
(@VoidElf, @Male,    2, 3, 0, 0, 0, 0),
(@VoidElf, @Male,    3, 4, 0, 0, 0, 0),
(@VoidElf, @Male,    4, 5, 0, 0, 0, 0),
(@VoidElf, @Male,    5, 6, 0, 0, 0, 0),
(@VoidElf, @Male,    6, 7, 0, 0, 0, 0),
(@VoidElf, @Male,    7, 8, 0, 0, 0, 0),
(@VoidElf, @Female,  0, 0, 0, 0, 0, 0),
(@VoidElf, @Female,  1, 0, 2, 0, 0, 0),
(@VoidElf, @Female,  2, 0, 3, 0, 0, 0),
(@VoidElf, @Female,  3, 0, 4, 0, 0, 0),
(@VoidElf, @Female,  4, 0, 5, 0, 0, 0);
