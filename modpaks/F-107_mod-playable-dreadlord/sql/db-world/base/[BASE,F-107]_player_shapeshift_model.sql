/* Dreadlord druid forms copy whatever the Home race (Undead) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @Dreadlord;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @Dreadlord, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @DreadlordHome
GROUP BY `ShapeshiftID`, `GenderID`;
