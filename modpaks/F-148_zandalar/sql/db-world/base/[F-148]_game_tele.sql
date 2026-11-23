-- Written once by a scratch script (2026-11-22) for F-145..F-148's terrain-only continents; edit by hand.

-- .tele targets on Zandalar: TrinityCore retail TDB 1210.26091's game_tele rows for map 1642 that stand on
-- the terrain (within 25 yards of the tiles' ground); those on a building's floor are left out, as the
-- buildings aren't in the client or the server's vmaps: Voldun, Atulaman, Nazwatha, Nazmir, HeartOfDarkness, Dazaralor
DELETE FROM `game_tele` WHERE `map` = 1642;
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148000, 248.18, 3065.86, 190.85, 3.138, 1642, 'TempleOfAkunda');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148001, 630.24, 4398.85, 10.44, 5.476, 1642, 'PortOfZemlan');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148002, 630.24, 4398.85, 10.44, 5.476, 1642, 'Zemlan');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148003, 1950.08, 4774.83, 94.24, 4.706, 1642, 'TerraceOfTheDevoted');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148004, 2839.28, 4186.72, 9.83, 4.714, 1642, 'ShatterStoneHarbor');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148005, 2062.77, 2835.96, 50.03, 4.934, 1642, 'VulperaHideaway');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148006, 3161.08, 3151.26, 121.59, 3.159, 1642, 'Slitheringgulch');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148007, 3360.42, 2492.46, 43.10, 5.452, 1642, 'TortakaRefuge');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148008, 2570.42, 1367.40, 19.76, 3.163, 1642, 'TheNecropolis');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148009, 2590.94, 477.19, 7.84, 5.488, 1642, 'TorgasRest');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148010, 1623.26, -772.92, 3.03, 1.737, 1642, 'KragwasBurrow');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148011, 1620.67, 1369.17, 20.97, 3.169, 1642, 'TerraceOfSorrow');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148012, 1742.18, 2241.74, 71.16, 3.892, 1642, 'Shoaljaitarpits');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148013, 770.90, 1378.48, 19.55, 6.254, 1642, 'ZuljanRuins');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148014, 45.56, 1820.03, 354.43, 4.332, 1642, 'GardenOfTheLoa');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148015, -805.10, 1962.61, 720.34, 2.102, 1642, 'Ataldazar');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148016, -2597.48, 2051.26, 40.23, 3.119, 1642, 'Xibala');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148017, -251.44, 188.63, 220.89, 0.261, 1642, 'Talgurub');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148018, 370.38, 83.49, 236.70, 0.324, 1642, 'NesingwaryStrek');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148019, 465.99, -803.33, 21.18, 1.438, 1642, 'Zebahari');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148020, -836.32, -1176.19, 0.83, 0.996, 1642, 'Atalgral');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148021, -1580.37, -1198.01, 1.73, 3.932, 1642, 'TalanjisRebuke');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148022, -477.32, 576.84, 220.35, 3.155, 1642, 'Zuldazar');
INSERT INTO `game_tele` (`id`, `position_x`, `position_y`, `position_z`, `orientation`, `map`, `name`) VALUES (148023, 3169.07, 3151.21, 121.54, 6.283, 1642, 'TempleOfSethraliss');
