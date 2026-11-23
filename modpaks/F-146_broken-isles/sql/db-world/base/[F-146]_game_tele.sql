-- Written once by a scratch script (2026-11-22) for F-145..F-148's terrain-only continents; edit by hand.

-- .tele targets on Broken Isles: TrinityCore retail TDB 1210.26091's game_tele rows for map 1220 that stand on
-- the terrain (within 25 yards of the tiles' ground); those on a building's floor are left out, as the
-- buildings aren't in the client or the server's vmaps: DalaranCity, Suramar, DalaranLegion, HallRogue, HallDK, NightborneSpawn
DELETE FROM `game_tele` WHERE `map` = 1220;
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146000, -218.95, 5600.90, 61.11, 3.324, 1220, 'Azsuna');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146001, 4492.69, 4836.35, 661.71, 1.370, 1220, 'Highmountain');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146002, 3854.78, 2020.04, 242.64, 3.290, 1220, 'Stormheim');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146003, -1306.66, 1741.40, 7.32, 0.091, 1220, 'BrokenShore');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146004, -3400.00, 4827.46, 27.83, 3.560, 1220, 'EyeAzshara');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146005, 4113.75, 7459.81, 48.23, 0.908, 1220, 'HallDruid');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146006, 4529.88, 5246.98, 862.19, 3.056, 1220, 'HallHunter');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (146007, 3811.66, 6344.61, 185.37, 0.900, 1220, 'Darkheart');
