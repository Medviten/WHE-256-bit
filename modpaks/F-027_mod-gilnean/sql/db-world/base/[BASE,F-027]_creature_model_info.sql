/* Add model info for morphing */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @GilneanMaleDisplay,   @GilneanFemaleDisplay
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@GilneanMaleDisplay,        0.306, 1.5, 0, 0), -- Gilnean Male
(@GilneanFemaleDisplay,      0.306, 1.5, 1, 0); -- Gilnean Female
