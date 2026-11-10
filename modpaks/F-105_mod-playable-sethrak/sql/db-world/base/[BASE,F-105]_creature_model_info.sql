/* Model info for the player displays: bounding radius and combat reach of the Human displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@SethrakMaleDisplay, @SethrakFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`)
SELECT @SethrakMaleDisplay,   `BoundingRadius`, `CombatReach`, 0, 0 FROM `creature_model_info` WHERE `DisplayID` = 49
UNION ALL
SELECT @SethrakFemaleDisplay, `BoundingRadius`, `CombatReach`, 1, 0 FROM `creature_model_info` WHERE `DisplayID` = 50;
