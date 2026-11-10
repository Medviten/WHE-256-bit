-- Stats of @LichHome
DELETE FROM `player_race_stats` WHERE `Race` = @Lich;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Lich, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @LichHome) AS `home`;
