-- Stats of @AllianceOrcHome
DELETE FROM `player_race_stats` WHERE `Race` = @AllianceOrc;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @AllianceOrc, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @AllianceOrcHome) AS `home`;
