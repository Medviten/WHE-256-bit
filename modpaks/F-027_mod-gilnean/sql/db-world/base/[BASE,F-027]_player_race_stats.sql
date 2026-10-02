DELETE FROM `player_race_stats` WHERE `Race` = @Gilnean;
INSERT INTO `player_race_stats` (`Race`,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit`)
SELECT @Gilnean,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit` FROM `player_race_stats` WHERE `Race` = @Human LIMIT 1;
