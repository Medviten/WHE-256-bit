/* Model info for the player displays: bounding radius and combat reach of the Dwarf displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@StormforgedMaleDisplay, @StormforgedFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`)
SELECT @StormforgedMaleDisplay,   `BoundingRadius`, `CombatReach`, 0, 0 FROM `creature_model_info` WHERE `DisplayID` = 53
UNION ALL
SELECT @StormforgedFemaleDisplay, `BoundingRadius`, `CombatReach`, 1, 0 FROM `creature_model_info` WHERE `DisplayID` = 54;
