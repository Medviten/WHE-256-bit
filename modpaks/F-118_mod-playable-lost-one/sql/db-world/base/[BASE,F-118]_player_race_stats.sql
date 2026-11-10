-- Stats of @LostOneHome
DELETE FROM `player_race_stats` WHERE `Race` = @LostOne;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @LostOne, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @LostOneHome) AS `home`;
