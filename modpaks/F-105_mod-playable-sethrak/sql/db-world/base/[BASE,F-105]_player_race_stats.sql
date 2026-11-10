-- Stats of @SethrakHome
DELETE FROM `player_race_stats` WHERE `Race` = @Sethrak;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Sethrak, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @SethrakHome) AS `home`;
