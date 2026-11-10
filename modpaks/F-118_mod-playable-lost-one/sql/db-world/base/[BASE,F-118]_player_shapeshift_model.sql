/* Lost One druid forms copy whatever the Home race (Draenei) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @LostOne;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @LostOne, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @LostOneHome
GROUP BY `ShapeshiftID`, `GenderID`;
