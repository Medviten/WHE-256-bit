/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @HordePandarenMount1Display, @HordePandarenMount2Display, @HordePandarenMount3Display, @HordePandarenMount4Display
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@HordePandarenMount1Display,   1, 1.5, 2, 0),
(@HordePandarenMount2Display, 1, 1.5, 2, 0),
(@HordePandarenMount3Display,  1, 1.5, 2, 0),
(@HordePandarenMount4Display,  1, 1.5, 2, 0);
