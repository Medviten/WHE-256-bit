/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @AlliancePandarenMount1Display, @AlliancePandarenMount2Display, @AlliancePandarenMount3Display, @AlliancePandarenMount4Display
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@AlliancePandarenMount1Display,   1, 1.5, 2, 0),
(@AlliancePandarenMount2Display, 1, 1.5, 2, 0),
(@AlliancePandarenMount3Display,  1, 1.5, 2, 0),
(@AlliancePandarenMount4Display,  1, 1.5, 2, 0);
