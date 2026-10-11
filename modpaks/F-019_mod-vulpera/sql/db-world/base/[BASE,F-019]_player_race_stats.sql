DELETE FROM `player_race_stats` WHERE `Race` = @Vulpera;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`) VALUES
(@Vulpera, -3, 2, 0, 3, -2); -- copied from goblin
