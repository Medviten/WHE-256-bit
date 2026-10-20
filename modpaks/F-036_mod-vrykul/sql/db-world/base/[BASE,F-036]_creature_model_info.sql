/* Add model info for player displays */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@VrykulMaleDisplay, @VrykulFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@VrykulMaleDisplay,          0.406, 1.5, 0, 0),
(@VrykulFemaleDisplay,        0.406, 1.5, 1, 0);
