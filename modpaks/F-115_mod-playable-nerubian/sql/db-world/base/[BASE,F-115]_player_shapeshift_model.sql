/* Nerubian druid forms copy whatever the Home race (Undead) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @Nerubian;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @Nerubian, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @NerubianHome
GROUP BY `ShapeshiftID`, `GenderID`;
