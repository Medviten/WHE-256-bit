-- Stats of @TwoHeadedOgreHome
DELETE FROM `player_race_stats` WHERE `Race` = @TwoHeadedOgre;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @TwoHeadedOgre, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @TwoHeadedOgreHome) AS `home`;
