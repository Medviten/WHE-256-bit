/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@KulTiranMount1CreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@KulTiranMount1CreatureID, 0, @KulTiranMount1Display, 1, 1, 12340);
