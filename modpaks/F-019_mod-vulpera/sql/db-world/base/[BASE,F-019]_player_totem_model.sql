-- Retail's Vulpera totems (dbc/[F-019]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @Vulpera;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Vulpera, @VulperaFireTotem),
(2, @Vulpera, @VulperaEarthTotem),
(3, @Vulpera, @VulperaWaterTotem),
(4, @Vulpera, @VulperaAirTotem);
