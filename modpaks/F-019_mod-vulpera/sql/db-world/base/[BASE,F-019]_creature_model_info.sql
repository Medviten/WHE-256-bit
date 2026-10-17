/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @VulperaMount1Display, @VulperaMount2Display
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@VulperaMount1Display, 1, 1.5, 2, 0),
(@VulperaMount2Display, 1, 1.5, 2, 0);
