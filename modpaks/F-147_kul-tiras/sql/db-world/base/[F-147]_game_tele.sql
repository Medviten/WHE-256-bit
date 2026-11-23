-- Written once by a scratch script (2026-11-22) for F-145..F-148's terrain-only continents; edit by hand.

-- .tele targets on Kul Tiras: TrinityCore retail TDB 1210.26091's game_tele rows for map 1643 that stand on
-- the terrain (within 25 yards of the tiles' ground); those on a building's floor are left out, as the
-- buildings aren't in the client or the server's vmaps: Boralus, Tradewindsmarket
DELETE FROM `game_tele` WHERE `map` = 1643;
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147000, -604.10, -346.10, 158.32, 6.209, 1643, 'TiragardeSoundSouth');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147001, 803.02, 1055.27, 82.96, 0.758, 1643, 'TiragardeSoundNorth');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147002, 803.02, 1055.27, 82.96, 0.758, 1643, 'Norwingtonestate');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147003, 1194.16, 14.10, 31.82, 6.087, 1643, 'Hatherford');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147004, -78.54, -1045.81, 81.11, 1.544, 1643, 'Bridgeport');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147005, -900.85, -644.46, 117.91, 5.699, 1643, 'Kenningslodge');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147006, -1867.57, -630.50, 69.23, 6.272, 1643, 'Freehold');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147007, 15.81, -2630.14, 21.70, 5.353, 1643, 'Toldagor');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147008, 843.73, 1889.46, 1.80, 1.488, 1643, 'Anglepointwharf');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147009, 1628.21, 1979.77, 287.13, 4.037, 1643, 'Waningglacier');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147010, -634.31, 3140.37, 323.54, 4.798, 1643, 'Drustvar');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147011, -634.31, 3140.37, 323.54, 4.798, 1643, 'AromsStand');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147012, -1506.48, 3738.69, 5.19, 0.894, 1643, 'FalconHurst');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147013, -894.82, 3894.99, 46.66, 5.795, 1643, 'CrimsonForest');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147014, 235.23, 3639.17, 144.12, 5.612, 1643, 'Corlain');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147015, 732.94, 3951.12, 103.69, 3.515, 1643, 'WhiteGroveChapel');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147016, 781.62, 3372.67, 232.65, 3.048, 1643, 'WaycrestManor');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147017, -1393.93, 1869.16, 165.13, 5.937, 1643, 'Golkoval');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147018, -1037.11, 1288.53, 6.45, 0.490, 1643, 'FletchersHollow');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147019, -907.23, 901.77, 137.70, 3.695, 1643, 'Vigilhill');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147020, -633.81, 1886.54, 108.49, 3.113, 1643, 'BarrowknollCemetery');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147021, -76.57, 2142.74, 46.10, 4.775, 1643, 'Fallhaven');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147022, 151.65, 1631.31, 1.87, 0.079, 1643, 'CarversHarbor');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147023, 3320.00, 1436.64, 42.86, 6.279, 1643, 'Fortdaelin');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147024, 2992.30, 913.20, 14.70, 4.139, 1643, 'Deadwash');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147025, 2382.24, 810.86, 187.91, 0.091, 1643, 'BriarbackKraul');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147026, 2507.29, -19.85, 54.86, 0.067, 1643, 'Brennadam');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147027, 2507.29, -19.85, 54.86, 0.067, 1643, 'StormSongValley');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147028, 2944.04, -552.24, 35.35, 0.236, 1643, 'MarinersStrand');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147029, 3627.15, -123.23, 103.42, 0.197, 1643, 'SageHold');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147030, 3913.98, 484.44, 116.26, 2.942, 1643, 'WarfangHold');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147031, 4155.56, -1102.78, 158.20, 4.842, 1643, 'ShrineOfTheStorm');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147032, 2837.74, 5200.77, 40.07, 2.268, 1643, 'MechagonIsland');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147033, 2434.20, 6161.55, 2.40, 1.518, 1643, 'WesternSpray');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147034, 2734.85, 5338.54, 73.47, 2.258, 1643, 'JunkwattDepot');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147035, 2901.59, 4930.22, 60.37, 1.924, 1643, 'TheHeaps');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147036, 2776.50, 4987.74, 1.14, 3.242, 1643, 'TheOutflow');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147037, 3122.08, 5148.01, 19.74, 2.620, 1643, 'BondosYard');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147038, 3018.77, 5515.36, 52.00, 6.268, 1643, 'TheFleetingForest');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147039, 3264.58, 5223.85, 18.38, 0.542, 1643, 'ScrapboneDen');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147040, 3332.95, 4862.50, 0.56, 2.502, 1643, 'ProspectusBay');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147041, 3189.32, 4973.59, 24.84, 2.787, 1643, 'Rustbolt');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (147042, 3380.10, 4595.10, 15.65, 3.651, 1643, 'SparkweaverPoint');
