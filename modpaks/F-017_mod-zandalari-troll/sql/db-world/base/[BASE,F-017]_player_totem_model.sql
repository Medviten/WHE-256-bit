
DELETE FROM `player_totem_model` WHERE `RaceID` IN (@ZandalariTroll);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES 
(1, @ZandalariTroll, @TrollFireTotem),
(2, @ZandalariTroll, @TrollEarthTotem),
(3, @ZandalariTroll, @TrollWaterTotem),
(4, @ZandalariTroll, @TrollAirTotem);
