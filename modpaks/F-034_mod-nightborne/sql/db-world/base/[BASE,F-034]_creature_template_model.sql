/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@NightborneManasaberCreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@NightborneManasaberCreatureID, 0, @NightborneManasaberDisplay, 1, 1, 12340);
