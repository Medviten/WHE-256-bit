-- Stats of @TitanHome
DELETE FROM `player_race_stats` WHERE `Race` = @Titan;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Titan, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @TitanHome) AS `home`;
