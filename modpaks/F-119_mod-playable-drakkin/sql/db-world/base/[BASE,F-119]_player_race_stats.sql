-- Stats of @DrakkinHome
DELETE FROM `player_race_stats` WHERE `Race` = @Drakkin;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Drakkin, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @DrakkinHome) AS `home`;
