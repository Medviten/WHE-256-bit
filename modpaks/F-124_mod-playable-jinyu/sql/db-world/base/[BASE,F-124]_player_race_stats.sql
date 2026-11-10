-- Stats of @JinyuHome
DELETE FROM `player_race_stats` WHERE `Race` = @Jinyu;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Jinyu, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @JinyuHome) AS `home`;
