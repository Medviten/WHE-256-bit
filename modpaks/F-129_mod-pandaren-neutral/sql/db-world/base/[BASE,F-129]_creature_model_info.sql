/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @NeutralPandarenMount1Display, @NeutralPandarenMount2Display, @NeutralPandarenMount3Display, @NeutralPandarenMount4Display
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@NeutralPandarenMount1Display,   1, 1.5, 2, 0),
(@NeutralPandarenMount2Display, 1, 1.5, 2, 0),
(@NeutralPandarenMount3Display,  1, 1.5, 2, 0),
(@NeutralPandarenMount4Display,  1, 1.5, 2, 0);
