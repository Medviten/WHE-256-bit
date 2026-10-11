/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@MagharDirewolfCreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@MagharDirewolfCreatureID, 0, @MagharDirewolfDisplay, 1, 1, 12340);
