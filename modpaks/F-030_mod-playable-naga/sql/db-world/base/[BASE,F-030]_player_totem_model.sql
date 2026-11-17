-- Retail's Naga totems (dbc/[F-030]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @Naga;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Naga, @NagaFireTotem),
(2, @Naga, @NagaEarthTotem),
(3, @Naga, @NagaWaterTotem),
(4, @Naga, @NagaAirTotem);
