-- Stats of @SurekiHome
DELETE FROM `player_race_stats` WHERE `Race` = @Sureki;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Sureki, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @SurekiHome) AS `home`;
