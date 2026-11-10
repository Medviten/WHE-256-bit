/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @NeutralPandarenMount1CreatureID, @NeutralPandarenMount2CreatureID, @NeutralPandarenMount3CreatureID, @NeutralPandarenMount4CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@NeutralPandarenMount1CreatureID,   0, @NeutralPandarenMount1Display,   1, 1, 12340),
(@NeutralPandarenMount2CreatureID, 0, @NeutralPandarenMount2Display, 1, 1, 12340),
(@NeutralPandarenMount3CreatureID,  0, @NeutralPandarenMount3Display,  1, 1, 12340),
(@NeutralPandarenMount4CreatureID,  0, @NeutralPandarenMount4Display,  1, 1, 12340);
