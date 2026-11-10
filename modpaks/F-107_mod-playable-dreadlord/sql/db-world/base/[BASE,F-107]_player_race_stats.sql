-- Stats of @DreadlordHome
DELETE FROM `player_race_stats` WHERE `Race` = @Dreadlord;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Dreadlord, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @DreadlordHome) AS `home`;
