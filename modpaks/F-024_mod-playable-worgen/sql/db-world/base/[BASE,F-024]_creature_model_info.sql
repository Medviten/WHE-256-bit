/* Add model info for mounts and other NPCs */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @WorgenMaleDisplay,     @WorgenFemaleDisplay,
    @WorgenWildMaleDisplay, @WorgenWildFemaleDisplay,
    @WorgenMount1Display,  @WorgenMount2Display,
    @LordHarfordDisplay
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@WorgenMaleDisplay,          0.406, 1.5, 0, 0), -- Worgen
(@WorgenFemaleDisplay,        0.406, 1.5, 1, 0), -- Worgenette
(@WorgenWildMaleDisplay,      0.406, 1.5, 0, 0), -- Running Wild Male
(@WorgenWildFemaleDisplay,    0.406, 1.5, 1, 0), -- Running Wild Female
(@WorgenMount1Display,           1, 1.5, 2, 0), -- Horse
(@WorgenMount2Display,      1, 1.5, 2, 0), -- Quik-horse
(@LordHarfordDisplay,         0.406, 1.5, 0, 0); -- Lord Harford
