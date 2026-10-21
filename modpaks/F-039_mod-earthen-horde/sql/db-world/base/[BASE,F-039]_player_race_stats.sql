-- Stats of @HordeEarthenHome
DELETE FROM `player_race_stats` WHERE `Race` = @HordeEarthen;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @HordeEarthen, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @HordeEarthenHome) AS `home`;
