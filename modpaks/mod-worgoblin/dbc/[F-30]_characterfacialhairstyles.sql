-- [F-30] mod-worgoblin: characterfacialhairstyles
-- Reintroduces Fel Orc entries as race 34

DELETE FROM `characterfacialhairstyles` WHERE `race` = 34 AND `gender` = 0 AND `variation_id` = 0;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES (12, 0, 0, 0, 0, 0, 0, 0);
DELETE FROM `characterfacialhairstyles` WHERE `race` = 34 AND `gender` = 1 AND `variation_id` = 0;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES (12, 0, 0, 0, 0, 0, 0, 0);
