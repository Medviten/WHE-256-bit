DELETE FROM `player_totem_model` WHERE `RaceID` IN (@LostOne);
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @LostOne, @DraeneiFireTotem),
(2, @LostOne, @DraeneiEarthTotem),
(3, @LostOne, @DraeneiWaterTotem),
(4, @LostOne, @DraeneiAirTotem);
