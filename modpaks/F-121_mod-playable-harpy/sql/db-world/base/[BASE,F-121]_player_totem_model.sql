DELETE FROM `player_totem_model` WHERE `RaceID` IN (@Harpy);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Harpy, @TaurenFireTotem),
(2, @Harpy, @TaurenEarthTotem),
(3, @Harpy, @TaurenWaterTotem),
(4, @Harpy, @TaurenAirTotem);
