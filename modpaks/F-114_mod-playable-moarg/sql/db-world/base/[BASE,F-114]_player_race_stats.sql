-- Stats of @MoargHome
DELETE FROM `player_race_stats` WHERE `Race` = @Moarg;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Moarg, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @MoargHome) AS `home`;
