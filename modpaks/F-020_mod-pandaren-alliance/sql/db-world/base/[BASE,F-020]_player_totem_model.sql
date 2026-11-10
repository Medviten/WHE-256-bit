-- Retail's Pandaren totems (dbc/[F-020]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @AlliancePandaren;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @AlliancePandaren, @PandarenFireTotem),
(2, @AlliancePandaren, @PandarenEarthTotem),
(3, @AlliancePandaren, @PandarenWaterTotem),
(4, @AlliancePandaren, @PandarenAirTotem);
