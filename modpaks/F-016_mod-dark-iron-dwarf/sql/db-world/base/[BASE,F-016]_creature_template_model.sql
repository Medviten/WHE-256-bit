/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@DarkIronDwarfMount1CreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@DarkIronDwarfMount1CreatureID, 0, @DarkIronDwarfMount1Display, 1, 1, 12340);
