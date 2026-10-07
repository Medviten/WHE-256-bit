-- Tauren ones
DELETE FROM `player_totem_model` WHERE `RaceID` IN (@HighmountainTauren);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES 
(1, @HighmountainTauren, @TaurenFireTotem),
(2, @HighmountainTauren, @TaurenEarthTotem),
(3, @HighmountainTauren, @TaurenWaterTotem),
(4, @HighmountainTauren, @TaurenAirTotem);
