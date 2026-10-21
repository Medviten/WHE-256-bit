/* Add model info for player displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@HordeEarthenMaleDisplay, @HordeEarthenFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@HordeEarthenMaleDisplay,          0.406, 1.5, 0, 0),
(@HordeEarthenFemaleDisplay,        0.406, 1.5, 1, 0);
