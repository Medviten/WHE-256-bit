/* Add model info for player displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@AllianceEarthenMaleDisplay, @AllianceEarthenFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@AllianceEarthenMaleDisplay,          0.406, 1.5, 0, 0),
(@AllianceEarthenFemaleDisplay,        0.406, 1.5, 1, 0);
