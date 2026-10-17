-- characterfacialhairstyles: 17 inserts, 0 updates, 0 deletes

-- Insertions
-- geoset_1 picks the 1xx geoset: male beards 101-108 (retail beards), female hair 101-107 (retail hair 201-207,
-- renumbered in the M2 skin). Variation 0 is clean shaven / no braids.
DELETE FROM `characterfacialhairstyles` WHERE `race` = (@HighmountainTauren);
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@HighmountainTauren, @Male,   0, 0, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   1, 1, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   2, 2, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   3, 3, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   4, 4, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   5, 5, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   6, 6, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   7, 7, 0, 0, 0, 0),
(@HighmountainTauren, @Male,   8, 8, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 0, 0, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 1, 1, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 2, 2, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 3, 3, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 4, 4, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 5, 5, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 6, 6, 0, 0, 0, 0),
(@HighmountainTauren, @Female, 7, 7, 0, 0, 0, 0);
