/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @HordePandarenMount1CreatureID, @HordePandarenMount2CreatureID, @HordePandarenMount3CreatureID, @HordePandarenMount4CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@HordePandarenMount1CreatureID,   0, @HordePandarenMount1Display,   1, 1, 12340),
(@HordePandarenMount2CreatureID, 0, @HordePandarenMount2Display, 1, 1, 12340),
(@HordePandarenMount3CreatureID,  0, @HordePandarenMount3Display,  1, 1, 12340),
(@HordePandarenMount4CreatureID,  0, @HordePandarenMount4Display,  1, 1, 12340);
