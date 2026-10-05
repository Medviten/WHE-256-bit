DELETE FROM `player_race_stats` WHERE `Race` = @HighmountainTauren;
INSERT INTO `player_race_stats` (`Race`,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit`)
SELECT @HighmountainTauren,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit` FROM `player_race_stats` WHERE `Race` = @Tauren LIMIT 1;
