-- Retail's DarkIronDwarf totems (dbc/[F-016]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @DarkIronDwarf;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @DarkIronDwarf, @DarkIronDwarfFireTotem),
(2, @DarkIronDwarf, @DarkIronDwarfEarthTotem),
(3, @DarkIronDwarf, @DarkIronDwarfWaterTotem),
(4, @DarkIronDwarf, @DarkIronDwarfAirTotem);
