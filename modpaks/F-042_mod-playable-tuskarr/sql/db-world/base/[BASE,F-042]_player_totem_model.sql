-- Retail's Tuskarr totems (dbc/[F-042]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @Tuskarr;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Tuskarr, @TuskarrFireTotem),
(2, @Tuskarr, @TuskarrEarthTotem),
(3, @Tuskarr, @TuskarrWaterTotem),
(4, @Tuskarr, @TuskarrAirTotem);
