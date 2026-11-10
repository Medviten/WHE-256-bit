-- Stats of @NerubianHome
DELETE FROM `player_race_stats` WHERE `Race` = @Nerubian;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Nerubian, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @NerubianHome) AS `home`;
