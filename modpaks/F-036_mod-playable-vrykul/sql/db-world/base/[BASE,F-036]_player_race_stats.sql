/* Set starting stats for Vrykuls */
DELETE FROM `player_race_stats` WHERE `Race` = @Vrykul;
INSERT INTO `player_race_stats` (`Race`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`) VALUES
(@Vrykul, 3, 2, 0, -4, -1); -- Copied from Kul Tiran (Worgen stats)
