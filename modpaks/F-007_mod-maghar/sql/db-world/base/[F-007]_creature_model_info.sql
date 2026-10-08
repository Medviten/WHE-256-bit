DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@MagharOrcMaleDisplay, @MagharOrcFemaleDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@MagharOrcMaleDisplay,   0.306, 1.5, 0, 0),
(@MagharOrcFemaleDisplay, 0.306, 1.5, 1, 0);
