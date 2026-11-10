-- Retail's Pandaren totems (dbc/[F-021]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @HordePandaren;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @HordePandaren, @PandarenFireTotem),
(2, @HordePandaren, @PandarenEarthTotem),
(3, @HordePandaren, @PandarenWaterTotem),
(4, @HordePandaren, @PandarenAirTotem);
