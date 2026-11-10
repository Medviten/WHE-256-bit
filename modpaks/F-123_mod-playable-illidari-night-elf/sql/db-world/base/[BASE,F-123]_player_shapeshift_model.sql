/* Illidari Night Elf druid forms copy whatever the Home race (NightElf) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @IllidariNightElf;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @IllidariNightElf, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @IllidariNightElfHome
GROUP BY `ShapeshiftID`, `GenderID`;
