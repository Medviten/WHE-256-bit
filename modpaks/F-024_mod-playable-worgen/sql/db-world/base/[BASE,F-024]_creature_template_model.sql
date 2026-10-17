/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @WorgenWildMaleCreatureID, @WorgenWildFemaleCreatureID,
    @WorgenMount1CreatureID, @WorgenMount2CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@WorgenWildMaleCreatureID,     0, @WorgenWildMaleDisplay,     1, 1, 12340), -- Running Wild Male
(@WorgenWildFemaleCreatureID,   0, @WorgenWildFemaleDisplay,   1, 1, 12340), -- Running Wild Female
(@WorgenMount1CreatureID,      0, @WorgenMount1Display,      1, 1, 12340), -- Mountain Horse
(@WorgenMount2CreatureID, 0, @WorgenMount2Display, 1, 1, 12340); -- Swift Mountain Horse
