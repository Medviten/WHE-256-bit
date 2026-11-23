-- Written once by a scratch script (2026-11-22) for F-145..F-148's terrain-only continents; edit by hand.

-- .tele targets on Draenor: TrinityCore retail TDB 1210.26091's game_tele rows for map 1116 that stand on
-- the terrain (within 25 yards of the tiles' ground); those on a building's floor are left out, as the
-- buildings aren't in the client or the server's vmaps: DraenorFrostfireRidge, DraenorBarrierSea
DELETE FROM `game_tele` WHERE `map` = 1116;
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145000, 3714.25, -3882.76, 30.79, 2.114, 1116, 'Stormshield');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145001, -62.91, -884.92, 20.27, 0.791, 1116, 'Draenor');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145002, -10.73, -11.69, 132.45, 4.994, 1116, 'DraenorShadowmoonValley');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145003, 1868.25, 543.89, 36.89, 0.822, 1116, 'DraenorTheCursedWoods');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145004, 792.98, -661.44, -34.45, 5.799, 1116, 'DraenorEmbaariVillage');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145005, 6035.97, 2747.90, 204.47, 4.291, 1116, 'DraenorThunderPass');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145006, 7201.84, 6143.85, 118.19, 5.211, 1116, 'DraenorCircleOfBlood');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145007, 2434.15, 2375.28, 126.58, 5.448, 1116, 'DraenorTalrador');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145008, 2892.45, 3496.20, 60.26, 4.009, 1116, 'DraenorShattrath');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145009, 1904.64, 2748.87, 133.66, 2.657, 1116, 'DraenorAuchindoun');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145010, 3046.93, 2259.74, 119.87, 3.419, 1116, 'DraenorTuurem');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145011, 3250.92, 1007.09, 39.57, 5.547, 1116, 'DraenorTangarra');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145012, 3205.78, 832.34, 81.91, 4.514, 1116, 'DraenorKhadagarsTower');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145013, 3444.42, 3122.29, 20.40, 0.009, 1116, 'DraenorShatariAnchorage');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145014, -587.88, 1080.18, 32.31, 1.023, 1116, 'DraenorSpiresOfArak');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145015, 261.10, 1306.36, 0.37, 2.318, 1116, 'DraenorHarvestingPits');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145016, -2117.71, 1255.85, 14.12, 3.083, 1116, 'DraenorPinchwhistlePoint');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145017, -1243.20, 1948.67, 22.57, 3.228, 1116, 'DraenorBloodmanePridelands');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145018, -166.49, 1862.79, 34.14, 3.522, 1116, 'DraenorShadowGlade');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145019, 596.59, 2410.67, 196.98, 3.766, 1116, 'DraenorTerrokarPass');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145020, 3324.23, 4759.55, 124.41, 1.306, 1116, 'DraenorNagrand');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145021, 2000.47, 5057.39, 193.49, 3.052, 1116, 'DraenorGatesOfGrommash');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145022, 2693.53, 6341.21, 48.83, 3.606, 1116, 'DraenorSpiritWoods');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145023, 3659.56, 7226.28, 10.44, 2.006, 1116, 'DraenorHighmaul');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145024, 6803.53, 1219.95, 69.69, 5.618, 1116, 'DraenorGorgrond');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145025, 7242.45, 902.16, 76.86, 1.385, 1116, 'DraenorSteamburstCauldron');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145026, 6847.86, 418.14, 79.44, 3.698, 1116, 'DraenorEverbloomWilds');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145027, 6126.31, 528.02, 16.23, 5.233, 1116, 'DraenorCrimsonFen');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145028, 5536.02, 1189.81, 93.15, 5.798, 1116, 'DraenorRazorbloom');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (145029, 5406.03, 1922.05, 171.85, 5.244, 1116, 'DraenorGorgrondPass');
