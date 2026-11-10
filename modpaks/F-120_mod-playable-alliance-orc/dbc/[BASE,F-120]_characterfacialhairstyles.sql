-- characterfacialhairstyles: 18 inserts, 0 updates, 0 deletes (from CoA 1.9.9's own rows for its race 52)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @AllianceOrc;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@AllianceOrc, @Male,    0, 0, 0, 0, 0, 0),
(@AllianceOrc, @Male,    1, 0, 0, 0, 0, 0),
(@AllianceOrc, @Male,    2, 2, 0, 0, 0, 0),
(@AllianceOrc, @Male,    3, 3, 0, 0, 0, 0),
(@AllianceOrc, @Male,    4, 4, 0, 0, 0, 0),
(@AllianceOrc, @Male,    5, 5, 0, 0, 0, 0),
(@AllianceOrc, @Male,    6, 6, 0, 0, 0, 0),
(@AllianceOrc, @Male,    7, 7, 0, 0, 0, 0),
(@AllianceOrc, @Male,    8, 8, 0, 0, 0, 0),
(@AllianceOrc, @Male,    9, 9, 0, 0, 0, 0),
(@AllianceOrc, @Male,   10, 10, 0, 0, 0, 0),
(@AllianceOrc, @Female,  0, 0, 0, 0, 0, 0),
(@AllianceOrc, @Female,  1, 0, 2, 0, 0, 0),
(@AllianceOrc, @Female,  2, 0, 3, 0, 0, 0),
(@AllianceOrc, @Female,  3, 0, 4, 0, 0, 0),
(@AllianceOrc, @Female,  4, 0, 5, 0, 0, 0),
(@AllianceOrc, @Female,  5, 0, 6, 0, 0, 0),
(@AllianceOrc, @Female,  6, 0, 7, 0, 0, 0);
