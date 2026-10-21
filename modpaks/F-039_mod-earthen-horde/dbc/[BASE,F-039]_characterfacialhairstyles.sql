-- characterfacialhairstyles: 22 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @HordeEarthen;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@HordeEarthen, @Male,    0,  0,  0,  0,  0,  0),
(@HordeEarthen, @Male,    1,  1,  0,  0,  0,  0),
(@HordeEarthen, @Male,    2,  2,  0,  0,  0,  0),
(@HordeEarthen, @Male,    3,  3,  0,  0,  0,  0),
(@HordeEarthen, @Male,    4,  4,  0,  0,  0,  0),
(@HordeEarthen, @Male,    5,  5,  0,  0,  0,  0),
(@HordeEarthen, @Male,    6,  6,  0,  0,  0,  0),
(@HordeEarthen, @Male,    7,  7,  0,  0,  0,  0),
(@HordeEarthen, @Male,    8,  8,  0,  0,  0,  0),
(@HordeEarthen, @Male,    9,  9,  0,  0,  0,  0),
(@HordeEarthen, @Male,   10, 10,  0,  0,  0,  0),
(@HordeEarthen, @Female,  0,  0,  0,  0,  0,  0),
(@HordeEarthen, @Female,  1,  1,  0,  0,  0,  0),
(@HordeEarthen, @Female,  2,  2,  0,  0,  0,  0),
(@HordeEarthen, @Female,  3,  3,  0,  0,  0,  0),
(@HordeEarthen, @Female,  4,  4,  0,  0,  0,  0),
(@HordeEarthen, @Female,  5,  5,  0,  0,  0,  0),
(@HordeEarthen, @Female,  6,  6,  0,  0,  0,  0),
(@HordeEarthen, @Female,  7,  7,  0,  0,  0,  0),
(@HordeEarthen, @Female,  8,  8,  0,  0,  0,  0),
(@HordeEarthen, @Female,  9,  9,  0,  0,  0,  0),
(@HordeEarthen, @Female, 10, 10,  0,  0,  0,  0);
