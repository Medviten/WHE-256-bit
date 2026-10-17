/* Add model info for mounts and other NPCs */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@HobgoblinDisplay, @GoblinMount1Display, @GoblinMount2Display, @GallyLumpstainDisplay);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@HobgoblinDisplay, 0.2325, 1.5, 0, 0), -- Gobber
(@GoblinMount1Display, 0.35, 1.5, 2, 0), -- Trike
(@GoblinMount2Display, 0.35, 1.5, 2, 0), -- Quik-trike
(@GallyLumpstainDisplay, 0.306, 1.5, 0, 0); -- Gally Lumpstain
