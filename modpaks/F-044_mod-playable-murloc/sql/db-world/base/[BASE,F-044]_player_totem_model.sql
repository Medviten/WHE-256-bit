DELETE FROM `player_totem_model` WHERE `RaceID` IN (@Murloc);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Murloc, @TrollFireTotem),
(2, @Murloc, @TrollEarthTotem),
(3, @Murloc, @TrollWaterTotem),
(4, @Murloc, @TrollAirTotem);
