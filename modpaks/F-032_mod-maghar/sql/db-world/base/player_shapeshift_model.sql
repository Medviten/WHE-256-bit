REPLACE INTO `player_shapeshift_model` (
    `ShapeshiftID`, -- ID from SpellShapeshiftForm.dbc or spellshapeshiftform_dbc
    `RaceID`, -- ID from ChrRaces.dbc or chrraces_dbc
    `CustomizationID`, -- hair colour or skin colour
    `GenderID`, -- 0: male, 1: female, 2: both
    `ModelID` -- ID from CreatureDisplayInfo.dbc or creaturedisplayinfo_dbc (*not* from CreatureModelData.dbc!)
) VALUES
/* Horde Travel forms – Mag'har Orc */
(
	3, -- ShapeshiftID: Travel form
	14, -- RaceID: Mag'har Orc
	255, -- CustomizationID: default
	2, -- GenderID: both
	45339 -- ModelID: DruidTravelHorde
);