/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @WorgenWildMaleCreatureID, @WorgenWildFemaleCreatureID,
    @MountainHorseCreatureID, @SwiftMountainHorseCreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@WorgenWildMaleCreatureID,     0, @WorgenWildMaleDisplay,     1, 1, 12340), -- Running Wild Male
(@WorgenWildFemaleCreatureID,   0, @WorgenWildFemaleDisplay,   1, 1, 12340), -- Running Wild Female
(@MountainHorseCreatureID,      0, @MountainHorseDisplay,      1, 1, 12340), -- Mountain Horse
(@SwiftMountainHorseCreatureID, 0, @SwiftMountainHorseDisplay, 1, 1, 12340); -- Swift Mountain Horse
