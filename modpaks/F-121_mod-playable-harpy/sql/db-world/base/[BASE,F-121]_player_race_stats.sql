-- Stats of @HarpyHome
DELETE FROM `player_race_stats` WHERE `Race` = @Harpy;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Harpy, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @HarpyHome) AS `home`;
