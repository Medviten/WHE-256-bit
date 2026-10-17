/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@ZandalariTrollMount1CreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@ZandalariTrollMount1CreatureID, 0, @ZandalariTrollMount1Display, 1, 1, 12340);
