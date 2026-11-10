-- Stats of @FungarianHome
DELETE FROM `player_race_stats` WHERE `Race` = @Fungarian;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Fungarian, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @FungarianHome) AS `home`;
