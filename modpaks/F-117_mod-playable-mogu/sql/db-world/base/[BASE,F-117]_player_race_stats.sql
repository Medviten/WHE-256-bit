-- Stats of @MoguHome
DELETE FROM `player_race_stats` WHERE `Race` = @Mogu;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Mogu, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @MoguHome) AS `home`;
