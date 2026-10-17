/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@NightborneMount1CreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@NightborneMount1CreatureID, 0, @NightborneMount1Display, 1, 1, 12340);
