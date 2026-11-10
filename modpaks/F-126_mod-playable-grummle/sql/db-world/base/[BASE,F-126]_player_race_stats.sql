-- Stats of @GrummleHome
DELETE FROM `player_race_stats` WHERE `Race` = @Grummle;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Grummle, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @GrummleHome) AS `home`;
