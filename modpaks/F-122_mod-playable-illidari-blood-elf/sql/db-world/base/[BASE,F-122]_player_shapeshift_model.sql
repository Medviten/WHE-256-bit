/* Illidari Blood Elf druid forms copy whatever the Home race (BloodElf) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @IllidariBloodElf;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @IllidariBloodElf, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @IllidariBloodElfHome
GROUP BY `ShapeshiftID`, `GenderID`;
