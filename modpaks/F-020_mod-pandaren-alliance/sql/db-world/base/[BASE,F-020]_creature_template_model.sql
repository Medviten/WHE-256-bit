/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @AlliancePandarenMount1CreatureID, @AlliancePandarenMount2CreatureID, @AlliancePandarenMount3CreatureID, @AlliancePandarenMount4CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@AlliancePandarenMount1CreatureID,   0, @AlliancePandarenMount1Display,   1, 1, 12340),
(@AlliancePandarenMount2CreatureID, 0, @AlliancePandarenMount2Display, 1, 1, 12340),
(@AlliancePandarenMount3CreatureID,  0, @AlliancePandarenMount3Display,  1, 1, 12340),
(@AlliancePandarenMount4CreatureID,  0, @AlliancePandarenMount4Display,  1, 1, 12340);
