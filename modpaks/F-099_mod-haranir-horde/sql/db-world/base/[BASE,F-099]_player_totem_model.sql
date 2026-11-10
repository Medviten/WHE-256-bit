-- Retail's Haranir totems (dbc/[F-099]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @HordeHaranir;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @HordeHaranir, @HaranirFireTotem),
(2, @HordeHaranir, @HaranirEarthTotem),
(3, @HordeHaranir, @HaranirWaterTotem),
(4, @HordeHaranir, @HaranirAirTotem);
