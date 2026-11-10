/* Grummle druid forms copy whatever the Home race (Dwarf) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @Grummle;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @Grummle, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @GrummleHome
GROUP BY `ShapeshiftID`, `GenderID`;
