-- Stats of @DrakonidHome
DELETE FROM `player_race_stats` WHERE `Race` = @Drakonid;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Drakonid, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @DrakonidHome) AS `home`;
