/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @CaravanHyena1CreatureID, @CaravanHyena2CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@CaravanHyena1CreatureID, 0, @CaravanHyena1Display, 1, 1, 12340),
(@CaravanHyena2CreatureID, 0, @CaravanHyena2Display, 1, 1, 12340);
