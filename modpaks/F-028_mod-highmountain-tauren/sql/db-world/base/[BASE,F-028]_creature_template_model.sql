/* Add models for racial mount */

DELETE FROM `creature_template_model` WHERE `CreatureID` = @HighmountainTaurenMount1CreatureID;
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@HighmountainTaurenMount1CreatureID, 0, @HighmountainTaurenMount1Display, 1, 1, 12340);
