/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@NightborneManasaberDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@NightborneManasaberDisplay, 1, 1.5, 2, 0);
