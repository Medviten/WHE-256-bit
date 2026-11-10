/* Model info for the player displays: bounding radius and combat reach of the Gnome displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@SporelingMaleDisplay, @SporelingFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`)
SELECT @SporelingMaleDisplay,   `BoundingRadius`, `CombatReach`, 0, 0 FROM `creature_model_info` WHERE `DisplayID` = 1563
UNION ALL
SELECT @SporelingFemaleDisplay, `BoundingRadius`, `CombatReach`, 1, 0 FROM `creature_model_info` WHERE `DisplayID` = 1564;
