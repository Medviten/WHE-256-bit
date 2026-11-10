-- Retail's ZandalariTroll totems (dbc/[F-017]_retail_totems.sql)
DELETE FROM `player_totem_model` WHERE `RaceID` = @ZandalariTroll;
INSERT INTO `player_totem_model` (`TotemID`, `RaceID`, `ModelID`) VALUES
(1, @ZandalariTroll, @ZandalariTrollFireTotem),
(2, @ZandalariTroll, @ZandalariTrollEarthTotem),
(3, @ZandalariTroll, @ZandalariTrollWaterTotem),
(4, @ZandalariTroll, @ZandalariTrollAirTotem);
