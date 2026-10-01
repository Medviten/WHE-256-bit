/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @CaravanHyena1Display, @CaravanHyena2Display
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@CaravanHyena1Display, 1, 1.5, 2, 0),
(@CaravanHyena2Display, 1, 1.5, 2, 0);
