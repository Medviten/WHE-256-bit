/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @GilneanMaleTemplate,     @GilneanFemaleTemplate
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@GilneanMaleTemplate,          0, @GilneanMaleDisplay,      1, 1, 12340), -- Gilnean Male
(@GilneanFemaleTemplate,        0, @GilneanFemaleDisplay,    1, 1, 12340); -- Gilnean Female
