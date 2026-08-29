REPLACE INTO `player_shapeshift_model` (
    `ShapeshiftID`, -- ID from SpellShapeshiftForm.dbc or spellshapeshiftform_dbc
    `RaceID`, -- ID from ChrRaces.dbc or chrraces_dbc
    `CustomizationID`, -- hair colour or skin colour
    `GenderID`, -- 0: male, 1: female, 2: both
    `ModelID` -- ID from CreatureDisplayInfo.dbc or creaturedisplayinfo_dbc (*not* from CreatureModelData.dbc!)
) VALUES

/* Alliance Travel form – high elf */
(
	3, -- ShapeshiftID: Travel form
	13, -- RaceID: High Elf
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
);
