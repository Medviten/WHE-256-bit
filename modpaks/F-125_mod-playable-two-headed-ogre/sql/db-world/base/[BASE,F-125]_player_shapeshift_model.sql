/* Two-Headed Ogre druid forms copy whatever the Home race (Orc) has (F-011 or stock) */
DELETE FROM `player_shapeshift_model` WHERE `RaceID` = @TwoHeadedOgre;
INSERT INTO `player_shapeshift_model` (`ShapeshiftID`, `RaceID`, `CustomizationID`, `GenderID`, `ModelID`)
SELECT `ShapeshiftID`, @TwoHeadedOgre, 255, `GenderID`, MIN(`ModelID`)
FROM `player_shapeshift_model`
WHERE `RaceID` = @TwoHeadedOgreHome
GROUP BY `ShapeshiftID`, `GenderID`;
