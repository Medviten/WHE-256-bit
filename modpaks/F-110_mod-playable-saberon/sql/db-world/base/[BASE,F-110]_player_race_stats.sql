-- Stats of @SaberonHome
DELETE FROM `player_race_stats` WHERE `Race` = @Saberon;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Saberon, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @SaberonHome) AS `home`;
