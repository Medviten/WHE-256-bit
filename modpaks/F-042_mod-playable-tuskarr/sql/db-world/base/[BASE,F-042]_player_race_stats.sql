-- Stats of @TuskarrHome
DELETE FROM `player_race_stats` WHERE `Race` = @Tuskarr;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Tuskarr, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @TuskarrHome) AS `home`;
