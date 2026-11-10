-- Retail's KulTiran totems (dbc/[F-025]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @KulTiran;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @KulTiran, @KulTiranFireTotem),
(2, @KulTiran, @KulTiranEarthTotem),
(3, @KulTiran, @KulTiranWaterTotem),
(4, @KulTiran, @KulTiranAirTotem);
