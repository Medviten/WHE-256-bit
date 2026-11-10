-- Stats of @IllidariBloodElfHome
DELETE FROM `player_race_stats` WHERE `Race` = @IllidariBloodElf;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @IllidariBloodElf, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @IllidariBloodElfHome) AS `home`;
