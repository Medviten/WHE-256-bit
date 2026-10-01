/* Add models for racial mounts */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (
    @DragonTurtleBlueCreatureID, @DragonTurtlePurpleCreatureID, @DragonTurtleGreenCreatureID, @DragonTurtleBlackCreatureID
);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
(@DragonTurtleBlueCreatureID,   0, @DragonTurtleBlueDisplay,   1, 1, 12340),
(@DragonTurtlePurpleCreatureID, 0, @DragonTurtlePurpleDisplay, 1, 1, 12340),
(@DragonTurtleGreenCreatureID,  0, @DragonTurtleGreenDisplay,  1, 1, 12340),
(@DragonTurtleBlackCreatureID,  0, @DragonTurtleBlackDisplay,  1, 1, 12340);
