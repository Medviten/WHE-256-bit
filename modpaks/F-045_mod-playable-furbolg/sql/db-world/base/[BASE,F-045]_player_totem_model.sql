-- Retail's Furbolg totems (dbc/[F-045]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @Furbolg;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @Furbolg, @FurbolgFireTotem),
(2, @Furbolg, @FurbolgEarthTotem),
(3, @Furbolg, @FurbolgWaterTotem),
(4, @Furbolg, @FurbolgAirTotem);
