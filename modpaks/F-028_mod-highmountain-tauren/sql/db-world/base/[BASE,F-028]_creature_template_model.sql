/* Add models for racial mount */

DELETE FROM `creature_template_model` WHERE `CreatureID` = @HighmountainThunderhoofCreatureID;
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@HighmountainThunderhoofCreatureID, 0, @HighmountainThunderhoofDisplay, 1, 1, 12340);
