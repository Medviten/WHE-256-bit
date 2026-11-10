/* Sethrak druid forms copy whatever the Home race (Human) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @Sethrak;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @Sethrak, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @SethrakHome
GROUP BY `ShapeshiftID`, `GenderID`;
