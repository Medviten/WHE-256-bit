/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @LightforgedFelcrusherHolyCreatureID, @LightforgedFelcrusherPurpleCreatureID,
    @LightforgedFelcrusherBlueCreatureID, @LightforgedFelcrusherDarkCreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@LightforgedFelcrusherHolyCreatureID,    0, @LightforgedFelcrusherHolyDisplay,      1, 1, 12340),
(@LightforgedFelcrusherPurpleCreatureID,  0, @LightforgedFelcrusherPurpleDisplay,    1, 1, 12340),
(@LightforgedFelcrusherBlueCreatureID,    0, @LightforgedFelcrusherBlueDisplay,      1, 1, 12340),
(@LightforgedFelcrusherDarkCreatureID,    0, @LightforgedFelcrusherDarkDisplay,      1, 1, 12340);
