-- Stats of @FurbolgHome
DELETE FROM `player_race_stats` WHERE `Race` = @Furbolg;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Furbolg, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @FurbolgHome) AS `home`;
