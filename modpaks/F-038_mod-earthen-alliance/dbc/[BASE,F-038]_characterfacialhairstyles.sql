-- characterfacialhairstyles: 22 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @AllianceEarthen;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@AllianceEarthen, @Male,    0,  0,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    1,  1,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    2,  2,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    3,  3,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    4,  4,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    5,  5,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    6,  6,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    7,  7,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    8,  8,  0,  0,  0,  0),
(@AllianceEarthen, @Male,    9,  9,  0,  0,  0,  0),
(@AllianceEarthen, @Male,   10, 10,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  0,  0,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  1,  1,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  2,  2,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  3,  3,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  4,  4,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  5,  5,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  6,  6,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  7,  7,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  8,  8,  0,  0,  0,  0),
(@AllianceEarthen, @Female,  9,  9,  0,  0,  0,  0),
(@AllianceEarthen, @Female, 10, 10,  0,  0,  0,  0);
