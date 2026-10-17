/* Add model info for mount */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@VoidElfMount1Display);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@VoidElfMount1Display,           1, 1.5, 2, 0);
