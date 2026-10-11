DELETE FROM `player_race_stats` WHERE `Race` = @LightforgedDraenei;
INSERT INTO `player_race_stats` (`Race`,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit`)
SELECT @LightforgedDraenei,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit` FROM `player_race_stats` WHERE `Race` = @Draenei LIMIT 1;
