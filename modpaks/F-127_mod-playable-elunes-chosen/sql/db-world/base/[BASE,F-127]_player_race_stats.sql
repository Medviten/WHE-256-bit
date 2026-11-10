-- Stats of @EluneChosenHome
DELETE FROM `player_race_stats` WHERE `Race` = @EluneChosen;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @EluneChosen, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`
FROM (SELECT * FROM `player_race_stats` WHERE `Race` = @EluneChosenHome) AS `home`;
