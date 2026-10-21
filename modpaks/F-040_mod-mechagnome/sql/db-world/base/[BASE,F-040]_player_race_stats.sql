-- Stats of @MechagnomeHome
DELETE FROM `player_race_stats` WHERE `Race` = @Mechagnome;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Mechagnome, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @MechagnomeHome) AS `home`;
