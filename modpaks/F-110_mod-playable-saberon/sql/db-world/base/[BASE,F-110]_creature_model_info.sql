/* Model info for the player displays: bounding radius and combat reach of the NightElf displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@SaberonMaleDisplay, @SaberonFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`)
SELECT @SaberonMaleDisplay,   `BoundingRadius`, `CombatReach`, 0, 0 FROM `creature_model_info` WHERE `DisplayID` = 55
UNION ALL
SELECT @SaberonFemaleDisplay, `BoundingRadius`, `CombatReach`, 1, 0 FROM `creature_model_info` WHERE `DisplayID` = 56;
