/* Add model info for mounts and other NPCs */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @LightforgedDraeneiMount1Display, @LightforgedDraeneiMount2Display,
    @LightforgedDraeneiMount3Display, @LightforgedDraeneiMount4Display
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@LightforgedDraeneiMount2Display, 1, 1.5, 2, 0),
(@LightforgedDraeneiMount3Display,   1, 1.5, 2, 0),
(@LightforgedDraeneiMount4Display,   1, 1.5, 2, 0),
(@LightforgedDraeneiMount1Display,   1, 1.5, 2, 0);
