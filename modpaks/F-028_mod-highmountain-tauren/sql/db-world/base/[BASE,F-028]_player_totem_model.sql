-- Retail's HighmountainTauren totems (dbc/[F-028]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @HighmountainTauren;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @HighmountainTauren, @HighmountainTaurenFireTotem),
(2, @HighmountainTauren, @HighmountainTaurenEarthTotem),
(3, @HighmountainTauren, @HighmountainTaurenWaterTotem),
(4, @HighmountainTauren, @HighmountainTaurenAirTotem);
