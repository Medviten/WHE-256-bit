-- characterfacialhairstyles: 19 inserts, 0 updates, 0 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Ogre;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Ogre, @Male,    0, 2, 2, 2, 0, 0),
(@Ogre, @Male,    1, 1, 3, 3, 0, 0),
(@Ogre, @Male,    2, 1, 4, 4, 0, 0),
(@Ogre, @Male,    4, 2, 1, 1, 0, 0),
(@Ogre, @Male,    5, 3, 5, 5, 0, 0),
(@Ogre, @Male,    6, 3, 0, 0, 0, 0),
(@Ogre, @Male,    7, 4, 1, 1, 0, 0),
(@Ogre, @Male,    8, 5, 2, 2, 0, 0),
(@Ogre, @Male,    9, 5, 3, 3, 0, 0),
(@Ogre, @Female,  0, 2, 2, 2, 0, 0),
(@Ogre, @Female,  1, 3, 3, 3, 0, 0),
(@Ogre, @Female,  2, 0, 4, 4, 0, 0),
(@Ogre, @Female,  4, 6, 6, 6, 0, 0),
(@Ogre, @Female,  5, 2, 2, 2, 0, 0),
(@Ogre, @Female,  6, 3, 3, 3, 0, 0),
(@Ogre, @Female,  7, 4, 4, 4, 0, 0),
(@Ogre, @Female,  8, 5, 5, 5, 0, 0),
(@Ogre, @Female,  9, 6, 6, 6, 0, 0),
(@Ogre, @Female, 10, 4, 4, 4, 0, 0);
