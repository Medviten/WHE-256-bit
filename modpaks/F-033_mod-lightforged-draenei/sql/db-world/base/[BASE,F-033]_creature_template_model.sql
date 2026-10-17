/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @LightforgedDraeneiMount1CreatureID, @LightforgedDraeneiMount2CreatureID,
    @LightforgedDraeneiMount3CreatureID, @LightforgedDraeneiMount4CreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@LightforgedDraeneiMount1CreatureID,    0, @LightforgedDraeneiMount1Display,      1, 1, 12340),
(@LightforgedDraeneiMount2CreatureID,  0, @LightforgedDraeneiMount2Display,    1, 1, 12340),
(@LightforgedDraeneiMount3CreatureID,    0, @LightforgedDraeneiMount3Display,      1, 1, 12340),
(@LightforgedDraeneiMount4CreatureID,    0, @LightforgedDraeneiMount4Display,      1, 1, 12340);
