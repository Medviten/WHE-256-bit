-- Stats of @ThinHumanHome
DELETE FROM `player_race_stats` WHERE `Race` = @ThinHuman;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @ThinHuman, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @ThinHumanHome) AS `home`;
