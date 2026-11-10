-- characterfacialhairstyles: the Neutral Pandaren rows of F-129, for this race
DELETE FROM `characterfacialhairstyles` WHERE `race` = @HordePandaren;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`)
SELECT @HordePandaren, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`
FROM (SELECT * FROM `characterfacialhairstyles` WHERE `race` = @NeutralPandaren) AS `n`;
