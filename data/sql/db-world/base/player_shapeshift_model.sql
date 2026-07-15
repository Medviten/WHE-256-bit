REPLACE INTO `player_shapeshift_model` (
    `ShapeshiftID`, -- ID from SpellShapeshiftForm.dbc or spellshapeshiftform_dbc
    `RaceID`, -- ID from ChrRaces.dbc or chrraces_dbc
    `CustomizationID`, -- hair colour or skin colour
    `GenderID`, -- 0: male, 1: female, 2: both
    `ModelID` -- ID from CreatureDisplayInfo.dbc or creaturedisplayinfo_dbc (*not* from CreatureModelData.dbc!)
) VALUES
/* Worgen Racials */
(
    34, -- ShapeshiftID: Two Forms
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    0, -- GenderID: male
    94135 -- ModelID: Gilnean (male)
),
(
    34, -- ShapeshiftID: Two Forms
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    1, -- GenderID: female
    94136 -- ModelID: Gilnean (female)
),
(
    33, -- ShapeshiftID: Running Wild
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    0, -- GenderID: male
    94133 -- ModelID: WorgenWild (male)
),
(
    33, -- ShapeshiftID: Running Wild
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    1, -- GenderID: female
    94134 -- ModelID: WorgenWild (female)
),
/* Undead Druid Forms */
(
	2, -- ShapeshiftID: Tree of Life Form
    5, -- RaceID: Undead
    255, -- CustomizationID: default
    0, -- GenderID: male
    94144 -- ModelID: EntSkinDead
), (
    2, -- ShapeshiftID: Tree of Life Form
    5, -- RaceID: Undead
    255, -- CustomizationID: default
    1, -- GenderID: female
    94141 -- ModelID: EntSkinDiseased
), (
    5, -- ShapeshiftID: Bear Form
    5, -- RaceID: Undead
    255, -- CustomizationID: default
    2, -- GenderID: both
    94139 -- ModelID: BearSkinBrownDiseased
), (
    5, -- ShapeshiftID: Bear Form
    5, -- RaceID: Undead
    0, -- CustomizationID: ?
    2, -- GenderID: both
    94140 -- ModelID: BearSkinWhiteDiseased
), (
    4, -- ShapeshiftID: Aquatic Form
    5, -- RaceID: Undead
    255, -- CustomizationID: default
    2, -- GenderID: both
    94143 -- ModelID: SharkSkinPurple
), (
    29, -- ShapeshiftID: Flight Form
    5, -- RaceID: Undead
    255, -- CustomizationID: default
    2, -- GenderID: both
    10007 -- ModelID: DragonWhelpSkinDiseased
),
/* Gnome Druid Forms */
(
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	1, -- CustomizationID: brown hair
	2, -- GenderID: both
	94146 -- ModelID: LasherOrchidSkinBrown -- ModelID: LasherOrchidSkinBrown
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	2, -- CustomizationID: gray hair
	2, -- GenderID: both
	94146 -- ModelID: LasherOrchidSkinBrown
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	3, -- CustomizationID: white hair
	2, -- GenderID: both
	94146 -- ModelID: LasherOrchidSkinBrown
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	4, -- CustomizationID: gray hair again
	2, -- GenderID: both
	94146 -- ModelID: LasherOrchidSkinBrown
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	5, -- CustomizationID: red hair
	2, -- GenderID: both
	94147 -- ModelID: LasherOrchidSkinPurple
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	8, -- CustomizationID: pink hair
	2, -- GenderID: both
	94147 -- ModelID: LasherOrchidSkinPurple
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	9, -- CustomizationID: black
	2, -- GenderID: both
	94147 -- ModelID: LasherOrchidSkinPurple
), (
	2, -- ShapeshiftID: Tree of Life Form
	7, -- RaceID: Gnome
	255, -- CustomizationID: default
	2, -- GenderID: both
	94145 -- ModelID: LasherOrchidSkinGreen
), (
	5, -- ShapeshiftID: Bear Form
	7, -- RaceID: Gnome
	255, -- CustomizationID: default
	2, -- GenderID: both
	23946 -- ModelID: PolarBearCubSkin
), (
	31, -- ShapeshiftID: Moonkin Form
	7, -- RaceID: Gnome
	255, -- CustomizationID: default
	2, -- GenderID: both
	24978 -- ModelID: NorthrendPenguin01
);