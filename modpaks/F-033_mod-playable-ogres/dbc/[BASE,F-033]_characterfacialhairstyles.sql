-- characterfacialhairstyles: 21 inserts, 3 updates, 39 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = 15 AND `gender` = 0 AND `variation_id` = 0;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES (15, 0, 0, 0, 0, 0, 0, 0);
