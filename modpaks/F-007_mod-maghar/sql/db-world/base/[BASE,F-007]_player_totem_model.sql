-- Retail's MagharOrc totems (dbc/[F-007]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @MagharOrc;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @MagharOrc, @MagharOrcFireTotem),
(2, @MagharOrc, @MagharOrcEarthTotem),
(3, @MagharOrc, @MagharOrcWaterTotem),
(4, @MagharOrc, @MagharOrcAirTotem);
