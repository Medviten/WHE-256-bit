/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @GilneanMaleCreatureID,     @GilneanFemaleCreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@GilneanMaleCreatureID,          0, @GilneanMaleDisplay,      1, 1, 12340), -- Gilnean Male
(@GilneanFemaleCreatureID,        0, @GilneanFemaleDisplay,    1, 1, 12340); -- Gilnean Female
