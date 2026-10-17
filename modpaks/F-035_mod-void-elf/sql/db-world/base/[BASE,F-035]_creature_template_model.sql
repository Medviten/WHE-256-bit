/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@VoidElfMount1CreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@VoidElfMount1CreatureID,      0, @VoidElfMount1Display,      1, 1, 12340);
