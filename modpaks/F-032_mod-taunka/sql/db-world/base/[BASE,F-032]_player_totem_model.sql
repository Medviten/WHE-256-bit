-- Tauren ones
DELETE FROM `player_totem_model` WHERE `RaceID` IN (@Taunka);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES 
(1, @Taunka, @TaurenFireTotem),
(2, @Taunka, @TaurenEarthTotem),
(3, @Taunka, @TaurenWaterTotem),
(4, @Taunka, @TaurenAirTotem);
