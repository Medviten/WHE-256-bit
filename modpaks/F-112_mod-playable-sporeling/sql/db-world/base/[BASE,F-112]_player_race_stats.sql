-- Stats of @SporelingHome
DELETE FROM `player_race_stats` WHERE `Race` = @Sporeling;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Sporeling, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @SporelingHome) AS `home`;
