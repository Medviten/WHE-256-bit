-- Retail's Haranir totems (dbc/[F-098]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @AllianceHaranir;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @AllianceHaranir, @HaranirFireTotem),
(2, @AllianceHaranir, @HaranirEarthTotem),
(3, @AllianceHaranir, @HaranirWaterTotem),
(4, @AllianceHaranir, @HaranirAirTotem);
