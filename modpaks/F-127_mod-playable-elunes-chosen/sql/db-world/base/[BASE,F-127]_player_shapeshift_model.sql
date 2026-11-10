/* Elune's Chosen druid forms copy whatever the Home race (NightElf) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @EluneChosen;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @EluneChosen, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @EluneChosenHome
GROUP BY `ShapeshiftID`, `GenderID`;
