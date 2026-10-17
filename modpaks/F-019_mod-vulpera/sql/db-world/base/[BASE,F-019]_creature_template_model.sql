/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @VulperaMount1CreatureID, @VulperaMount2CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@VulperaMount1CreatureID, 0, @VulperaMount1Display, 1, 1, 12340),
(@VulperaMount2CreatureID, 0, @VulperaMount2Display, 1, 1, 12340);
