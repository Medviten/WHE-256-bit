/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@MagharOrcMount1CreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@MagharOrcMount1CreatureID, 0, @MagharOrcMount1Display, 1, 1, 12340);
