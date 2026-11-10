/* Orc druid forms copy whatever the Home race (Human) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @AllianceOrc;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @AllianceOrc, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @AllianceOrcHome
GROUP BY `ShapeshiftID`, `GenderID`;
