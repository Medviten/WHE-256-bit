-- Stats of @AllianceEarthenHome
DELETE FROM `player_race_stats` WHERE `Race` = @AllianceEarthen;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @AllianceEarthen, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @AllianceEarthenHome) AS `home`;
