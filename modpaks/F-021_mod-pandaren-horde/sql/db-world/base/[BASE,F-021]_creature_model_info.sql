/* Add model info for mounts */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (
    @DragonTurtleBlueDisplay, @DragonTurtlePurpleDisplay, @DragonTurtleGreenDisplay, @DragonTurtleBlackDisplay
);
INSERT INTO `creature_model_info` (`DisplayID`, `BoundingRadius`, `CombatReach`, `Gender`, `DisplayID_Other_Gender`) VALUES
(@DragonTurtleBlueDisplay,   1, 1.5, 2, 0),
(@DragonTurtlePurpleDisplay, 1, 1.5, 2, 0),
(@DragonTurtleGreenDisplay,  1, 1.5, 2, 0),
(@DragonTurtleBlackDisplay,  1, 1.5, 2, 0);
