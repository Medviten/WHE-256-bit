-- Stats of @StormforgedHome
DELETE FROM `player_race_stats` WHERE `Race` = @Stormforged;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Stormforged, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @StormforgedHome) AS `home`;
