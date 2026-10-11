/* Add model info for mounts and other NPCs */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @LightforgedFelcrusherHolyCreatureID, @LightforgedFelcrusherPurpleCreatureID,
    @LightforgedFelcrusherBlueCreatureID, @LightforgedFelcrusherDarkCreatureID
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@LightforgedFelcrusherPurpleDisplay, 1, 1.5, 2, 0),
(@LightforgedFelcrusherBlueDisplay,   1, 1.5, 2, 0),
(@LightforgedFelcrusherDarkDisplay,   1, 1.5, 2, 0),
(@LightforgedFelcrusherHolyDisplay,   1, 1.5, 2, 0);
