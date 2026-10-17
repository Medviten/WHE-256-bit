/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@MagharOrcMount1Display);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@MagharOrcMount1Display, 1, 1.5, 2, 0);
