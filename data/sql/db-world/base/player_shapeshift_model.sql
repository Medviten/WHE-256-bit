REPLACE INTO `player_shapeshift_model` (
    `ShapeshiftID`, -- ID from SpellShapeshiftForm.dbc or spellshapeshiftform_dbc
    `RaceID`, -- ID from ChrRaces.dbc or chrraces_dbc
    `CustomizationID`, -- hair colour or skin colour
    `GenderID`, -- 0: male, 1: female, 2: both
    `ModelID` -- ID from CreatureDisplayInfo.dbc or creaturedisplayinfo_dbc (*not* from CreatureModelData.dbc!)
) VALUES

/* Troll Druid forms */
(
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    0, -- CustomizationID: pink hair
    2, -- GenderID: both
    33665 -- ModelID: DruidCatTrollSkinBlack
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    1, -- CustomizationID: red hair
    2, -- GenderID: both
    33668 -- ModelID: DruidCatTrollSkinRed
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    2, -- CustomizationID: orange hair
    2, -- GenderID: both
    33668 -- ModelID: DruidCatTrollSkinRed
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    3, -- CustomizationID: yellow hair
    2, -- GenderID: both
    33667 -- ModelID: DruidCatTrollSkinGreen
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    4, -- CustomizationID: green hair
    2, -- GenderID: both
    33666 -- ModelID: DruidCatTrollSkinBlue
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    5, -- CustomizationID: blue-green hair
    2, -- GenderID: both
    33666 -- ModelID: DruidCatTrollSkinBlue
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    6, -- CustomizationID: blue hair
    2, -- GenderID: both
    33666 -- ModelID: DruidCatTrollSkinBlue
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    7, -- CustomizationID: purple hair
    2, -- GenderID: both
    33666 -- ModelID: DruidCatTrollSkinBlue
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    8, -- CustomizationID: gray hair
    2, -- GenderID: both
    33669 -- ModelID: DruidCatTrollSkinWhite
), (
	1, -- ShapeshiftID: Cat Form
    8, -- RaceID: Troll
    9, -- CustomizationID: white hair
    2, -- GenderID: both
    33669 -- ModelID: DruidCatTrollSkinWhite
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    0, -- CustomizationID: pink hair
    2, -- GenderID: both
    33656 -- ModelID: DruidBearTrollPurple
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    1, -- CustomizationID: red hair
    2, -- GenderID: both
    33657 -- ModelID: DruidBearTrollRed
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    2, -- CustomizationID: orange hair
    2, -- GenderID: both
    33657 -- ModelID: DruidBearTrollRed
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    3, -- CustomizationID: yellow hair
    2, -- GenderID: both
    33659 -- ModelID: DruidBearTrollYellow
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    4, -- CustomizationID: green hair
    2, -- GenderID: both
    33655 -- ModelID: DruidBearTrollBlue
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    5, -- CustomizationID: blue-green hair
    2, -- GenderID: both
    33655 -- ModelID: DruidBearTrollBlue
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    6, -- CustomizationID: blue hair
    2, -- GenderID: both
    33655 -- ModelID: DruidBearTrollBlue
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    7, -- CustomizationID: purple hair
    2, -- GenderID: both
    33655 -- ModelID: DruidBearTrollBlue
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    8, -- CustomizationID: gray hair
    2, -- GenderID: both
    33658 -- ModelID: DruidBearTrollWhite
), (
	5, -- ShapeshiftID: Bear Form
    8, -- RaceID: Troll
    9, -- CustomizationID: white hair
    2, -- GenderID: both
    33658 -- ModelID: DruidBearTrollWhite
), (
	31, -- ShapeshiftID: Moonkin Form
    8, -- RaceID: Troll
    255, -- CustomizationID: default
    2, -- GenderID: both
    37174 -- ModelID: DruidOwlBearRedSkin, DruidOwlBearRedSkin2
), (
	2, -- ShapeshiftID: Tree of Life Form
    8, -- RaceID: Troll
    255, -- CustomizationID: default
    2, -- GenderID: both
    37166 -- ModelID: DruidTreeFormOrange
), (
	27, -- ShapeshiftID: Swift Flight Form
    8, -- RaceID: Troll
    255, -- CustomizationID: default
    2, -- GenderID: both
    37730 -- ModelID: EpicDruidFlightTroll1, EpicDruidFlightTroll2
), (
	29, -- ShapeshiftID: Flight Form
    8, -- RaceID: Troll
    255, -- CustomizationID: default
    2, -- GenderID: both
    94216 -- ModelID: DruidFlightTroll1, DruidFlightTroll2
),

/* Worgen Druid forms */
(
	1, -- ShapeshiftID: Cat Form
    12, -- RaceID: Worgen
    0, -- CustomizationID: black hair
    2, -- GenderID: both
    33661 -- ModelID: DruidCatSkinWorgenBlack
), (
	1, -- ShapeshiftID: Cat Form
    12, -- RaceID: Worgen
    1, -- CustomizationID: light brown hair
    2, -- GenderID: both
    33660 -- ModelID: DruidCatSkinWorgen
), (
	1, -- ShapeshiftID: Cat Form
    12, -- RaceID: Worgen
    2, -- CustomizationID: brown hair
    2, -- GenderID: both
    33662 -- ModelID: DruidCatSkinWorgenBrown
), (
	1, -- ShapeshiftID: Cat Form
    12, -- RaceID: Worgen
    3, -- CustomizationID: red hair
    2, -- GenderID: both
    33663 -- ModelID: DruidCatSkinWorgenWhite
), (
	1, -- ShapeshiftID: Cat Form
    12, -- RaceID: Worgen
    4, -- CustomizationID: dark blonde hair
    2, -- GenderID: both
    33664 -- ModelID: DruidCatSkinWorgenYellow
), (
	5, -- ShapeshiftID: Bear Form
    12, -- RaceID: Worgen
    0, -- CustomizationID: black hair
    2, -- GenderID: both
    33651 -- ModelID: DruidBearWorgenBlack
), (
	5, -- ShapeshiftID: Bear Form
    12, -- RaceID: Worgen
    1, -- CustomizationID: light brown hair
    2, -- GenderID: both
    33650 -- ModelID: DruidBearWorgen
), (
	5, -- ShapeshiftID: Bear Form
    12, -- RaceID: Worgen
    2, -- CustomizationID: brown hair
    2, -- GenderID: both
    33652 -- ModelID: DruidBearWorgenBrown
), (
	5, -- ShapeshiftID: Bear Form
    12, -- RaceID: Worgen
    3, -- CustomizationID: red hair
    2, -- GenderID: both
    33654 -- ModelID: DruidBearWorgenWhite
), (
	5, -- ShapeshiftID: Bear Form
    12, -- RaceID: Worgen
    4, -- CustomizationID: dark blonde hair
    2, -- GenderID: both
    33653 -- ModelID: DruidBearWorgenTan
), (
	8, -- ShapeshiftID: Dire Bear Form
    12, -- RaceID: Worgen
    0, -- CustomizationID: black hair
    2, -- GenderID: both
    33651 -- ModelID: DruidBearWorgenBlack
), (
	8, -- ShapeshiftID: Dire Bear Form
    12, -- RaceID: Worgen
    1, -- CustomizationID: light brown hair
    2, -- GenderID: both
    33650 -- ModelID: DruidBearWorgen
), (
	8, -- ShapeshiftID: Dire Bear Form
    12, -- RaceID: Worgen
    2, -- CustomizationID: brown hair
    2, -- GenderID: both
    33652 -- ModelID: DruidBearWorgenBrown
), (
	8, -- ShapeshiftID: Dire Bear Form
    12, -- RaceID: Worgen
    3, -- CustomizationID: red hair
    2, -- GenderID: both
    33654 -- ModelID: DruidBearWorgenWhite
), (
	8, -- ShapeshiftID: Dire Bear Form
    12, -- RaceID: Worgen
    4, -- CustomizationID: dark blonde hair
    2, -- GenderID: both
    33653 -- ModelID: DruidBearWorgenTan
), (
	31, -- ShapeshiftID: Moonkin Form
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    2, -- GenderID: both
    37173 -- ModelID: DruidOwlBearBlackSkin, DruidOwlBearBlackSkin2
), (
	2, -- ShapeshiftID: Tree of Life Form
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    2, -- GenderID: both
    37164 -- ModelID: DruidTreeFormRed
), (
	27, -- ShapeshiftID: Swift Flight Form
    12, -- RaceID: Worgen
    255, -- CustomizationID: default
    2, -- GenderID: both
    37729 -- ModelID: StormCrowDruidSkin
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
	9, -- CustomizationID: black hair
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
),

/* Alliance Travel form */
(
	3, -- ShapeshiftID: Travel form
	1, -- RaceID: Human
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
), (
	3, -- ShapeshiftID: Travel form
	3, -- RaceID: Dwarf
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
), (
	3, -- ShapeshiftID: Travel form
	7, -- RaceID: Gnome
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
), (
	3, -- ShapeshiftID: Travel form
	11, -- RaceID: Draenei
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
), (
	3, -- ShapeshiftID: Travel form
	12, -- RaceID: Worgen
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
), (
	3, -- ShapeshiftID: Travel form
	13, -- RaceID: High Elf
	255, -- CustomizationID: default
	2, -- GenderID: both
	40816 -- ModelID: DruidTravelAlliance
),

/* Horde Travel forms */
(
	3, -- ShapeshiftID: Travel form
	2, -- RaceID: Orc
	255, -- CustomizationID: default
	2, -- GenderID: both
	45339 -- ModelID: DruidTravelHorde
), (
	3, -- ShapeshiftID: Travel form
	8, -- RaceID: Troll
	255, -- CustomizationID: default
	2, -- GenderID: both
	45339 -- ModelID: DruidTravelHorde
), (
	3, -- ShapeshiftID: Travel form
	9, -- RaceID: Goblin
	255, -- CustomizationID: default
	2, -- GenderID: both
	45339 -- ModelID: DruidTravelHorde
), (
	3, -- ShapeshiftID: Travel form
	10, -- RaceID: Blood Elf
	255, -- CustomizationID: default
	2, -- GenderID: both
	45339 -- ModelID: DruidTravelHorde
), (
	3, -- ShapeshiftID: Travel form
	14, -- RaceID: Mag'har Orc
	255, -- CustomizationID: default
	2, -- GenderID: both
	45339 -- ModelID: DruidTravelHorde
);