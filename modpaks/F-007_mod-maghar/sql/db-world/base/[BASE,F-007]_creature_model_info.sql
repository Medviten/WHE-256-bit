/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@MagharDirewolfDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@MagharDirewolfDisplay, 1, 1.5, 2, 0);
