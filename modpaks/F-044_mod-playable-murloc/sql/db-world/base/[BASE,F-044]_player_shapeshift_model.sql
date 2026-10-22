/* Murloc druid forms copy whatever the Troll has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @Murloc;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @Murloc, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @Troll
GROUP BY `ShapeshiftID`, `GenderID`;
