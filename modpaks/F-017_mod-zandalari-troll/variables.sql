-- Race ID
SET @ZandalariTroll                          := @NextRace := @NextRace +1;  -- default: 17
SET @ZandalariTrollMask                       = 1 << (@ZandalariTroll - 1); -- race ID 17 → 65536
SET @ZandalariTrollHelmetMask                 = 1 << @ZandalariTroll;       -- race ID 17 → 131072

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                                = @HordeMask    | @ZandalariTrollMask;
SET @BarrensBros                              = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                         = @AllianceMask | @HordeMask;
SET @BowHunters                               = @BowHunters   | @ZandalariTrollMask;
SET @ZandalariTrollLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @ZandalariTrollAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @ZandalariTrollKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @ZandalariTrollExplorationSound           = @TrollExplorationSound;
SET @ZandalariTrollCinematicSequence          = @TrollCinematicSequence;
SET @ZandalariTrollBlood                      = 1;
SET @ZandalariTrollMaleModelPath              = 'Character\\ZandalariTroll\\male\\ZandalariTrollMale.M2';
SET @ZandalariTrollFemaleModelPath            = 'Character\\ZandalariTroll\\female\\ZandalariTrollFemale.M2';
SET @ZandalariTrollMaleFootprint              = @FootprintShoe;
SET @ZandalariTrollFemaleFootprint            = @FootprintShoe;

-- Mounts (IDs are global, see config.sql)
SET @ZandalariTrollMount1                    = @SpellZandalariDirehorn;
SET @ZandalariTrollMount1Model               = @ZandalariDirehornModel;
SET @ZandalariTrollMount1Display             = @ZandalariDirehornDisplay;
SET @ZandalariTrollMount1CreatureID          = @ZandalariDirehornCreatureID;
SET @ZandalariTrollMount1Item                = @ZandalariDirehornItem;
SET @ZandalariTrollMount1ItemDisplay         = @ZandalariDirehornItemDisplay;
SET @ZandalariTrollMount1IconID              = @IconZandalariDirehorn;
SET @ZandalariTrollMount1IconName            = 'inv_triceratopszandalari';
SET @ZandalariTrollMount1IconPath            = CONCAT('Interface\\Icons\\', @ZandalariTrollMount1IconName);
SET @ZandalariTrollMount1ModelPath           = 'Creature\\triceratops\\triceratopsmount.m2';

-- Strings
SET @ZandalariTrollClientPrefix               = 'Tr';
SET @ZandalariTrollClientString               = 'ZandalariTroll';
SET @ZandalariTrollFacialHairCustomization1   = 'TUSKS';
SET @ZandalariTrollFacialHairCustomization2   = 'TUSKS';
SET @ZandalariTrollHairCustomization          = 'NORMAL';

-- Localization Strings
SET @ZandalariTrollenUS                       = 'Zandalari Troll';
SET @ZandalariTrollkoKR                       = '';
SET @ZandalariTrollfrFR                       = '';
SET @ZandalariTrolldeDE                       = '';
SET @ZandalariTrollzhCN                       = '';
SET @ZandalariTrollzhTW                       = '';
SET @ZandalariTrollesES                       = '';
SET @ZandalariTrollesMX                       = '';
SET @ZandalariTrollruRU                       = '';
SET @ZandalariTrolljaJP                       = '';
SET @ZandalariTrollptPT                       = '';
SET @ZandalariTrollitIT                       = '';
SET @ZandalariTrollUnk1                       = '';
SET @ZandalariTrollUnk2                       = '';
SET @ZandalariTrollUnk3                       = '';
SET @ZandalariTrollUnk4                       = '';

SET @ZandalariTrollFemaleenUS                 = '';
SET @ZandalariTrollFemalekoKR                 = '';
SET @ZandalariTrollFemalefrFR                 = '';
SET @ZandalariTrollFemaledeDE                 = '';
SET @ZandalariTrollFemalezhCN                 = '';
SET @ZandalariTrollFemalezhTW                 = '';
SET @ZandalariTrollFemaleesES                 = '';
SET @ZandalariTrollFemaleesMX                 = '';
SET @ZandalariTrollFemaleruRU                 = '';
SET @ZandalariTrollFemalejaJP                 = '';
SET @ZandalariTrollFemaleptPT                 = '';
SET @ZandalariTrollFemaleitIT                 = '';
SET @ZandalariTrollFemaleUnk1                 = '';
SET @ZandalariTrollFemaleUnk2                 = '';
SET @ZandalariTrollFemaleUnk3                 = '';
SET @ZandalariTrollFemaleUnk4                 = '';

SET @ZandalariTrollMaleenUS                   = '';
SET @ZandalariTrollMalekoKR                   = '';
SET @ZandalariTrollMalefrFR                   = '';
SET @ZandalariTrollMaledeDE                   = '';
SET @ZandalariTrollMalezhCN                   = '';
SET @ZandalariTrollMalezhTW                   = '';
SET @ZandalariTrollMaleesES                   = '';
SET @ZandalariTrollMaleesMX                   = '';
SET @ZandalariTrollMaleruRU                   = '';
SET @ZandalariTrollMalejaJP                   = '';
SET @ZandalariTrollMaleptPT                   = '';
SET @ZandalariTrollMaleitIT                   = '';
SET @ZandalariTrollMaleUnk1                   = '';
SET @ZandalariTrollMaleUnk2                   = '';
SET @ZandalariTrollMaleUnk3                   = '';
SET @ZandalariTrollMaleUnk4                   = '';

SET @ZandalariTrollRacialNameenUS             = 'Racial - Zandalari Troll';
SET @ZandalariTrollRacialNamekoKR             = '';
SET @ZandalariTrollRacialNamefrFR             = '';
SET @ZandalariTrollRacialNamedeDE             = '';
SET @ZandalariTrollRacialNamezhCN             = '';
SET @ZandalariTrollRacialNamezhTW             = '';
SET @ZandalariTrollRacialNameesES             = '';
SET @ZandalariTrollRacialNameesMX             = '';
SET @ZandalariTrollRacialNameruRU             = '';
SET @ZandalariTrollRacialNamejaJP             = '';
SET @ZandalariTrollRacialNameptPT             = '';
SET @ZandalariTrollRacialNameitIT             = '';
SET @ZandalariTrollRacialNameUnk1             = '';
SET @ZandalariTrollRacialNameUnk2             = '';
SET @ZandalariTrollRacialNameUnk3             = '';
SET @ZandalariTrollRacialNameUnk4             = '';

SET @ZandalariTrollPlayerenUS                 = '"PLAYER"," Zandalari Troll"';
SET @ZandalariTrollPlayerkoKR                 = '';
SET @ZandalariTrollPlayerfrFR                 = '';
SET @ZandalariTrollPlayerdeDE                 = '';
SET @ZandalariTrollPlayerzhCN                 = '';
SET @ZandalariTrollPlayerzhTW                 = '';
SET @ZandalariTrollPlayeresES                 = '';
SET @ZandalariTrollPlayeresMX                 = '';
SET @ZandalariTrollPlayerruRU                 = '';
SET @ZandalariTrollPlayerjaJP                 = '';
SET @ZandalariTrollPlayerptPT                 = '';
SET @ZandalariTrollPlayeritIT                 = '';
SET @ZandalariTrollPlayerUnk1                 = '';
SET @ZandalariTrollPlayerUnk2                 = '';
SET @ZandalariTrollPlayerUnk3                 = '';
SET @ZandalariTrollPlayerUnk4                 = '';

SET @ZandalariTrollFactionNameenUS            = 'Zandalari Empire';
SET @ZandalariTrollFactionNamekoKR            = '';
SET @ZandalariTrollFactionNamefrFR            = '';
SET @ZandalariTrollFactionNamedeDE            = '';
SET @ZandalariTrollFactionNamezhCN            = '';
SET @ZandalariTrollFactionNamezhTW            = '';
SET @ZandalariTrollFactionNameesES            = '';
SET @ZandalariTrollFactionNameesMX            = '';
SET @ZandalariTrollFactionNameruRU            = '';
SET @ZandalariTrollFactionNamejaJP            = '';
SET @ZandalariTrollFactionNameptPT            = '';
SET @ZandalariTrollFactionNameitIT            = '';
SET @ZandalariTrollFactionNameUnk1            = '';
SET @ZandalariTrollFactionNameUnk2            = '';
SET @ZandalariTrollFactionNameUnk3            = '';
SET @ZandalariTrollFactionNameUnk4            = '';

SET @ZandalariTrollFactionDescriptionenUS     = 'The oldest empire of Azeroth, the Zandalari are powerful trolls who bargain with fearsome loa and whose navy is unmatched on the Great Sea.';
SET @ZandalariTrollFactionDescriptionkoKR     = '';
SET @ZandalariTrollFactionDescriptionfrFR     = '';
SET @ZandalariTrollFactionDescriptiondeDE     = '';
SET @ZandalariTrollFactionDescriptionzhCN     = '';
SET @ZandalariTrollFactionDescriptionzhTW     = '';
SET @ZandalariTrollFactionDescriptionesES     = '';
SET @ZandalariTrollFactionDescriptionesMX     = '';
SET @ZandalariTrollFactionDescriptionruRU     = '';
SET @ZandalariTrollFactionDescriptionjaJP     = '';
SET @ZandalariTrollFactionDescriptionptPT     = '';
SET @ZandalariTrollFactionDescriptionitIT     = '';
SET @ZandalariTrollFactionDescriptionUnk1     = '';
SET @ZandalariTrollFactionDescriptionUnk2     = '';
SET @ZandalariTrollFactionDescriptionUnk3     = '';
SET @ZandalariTrollFactionDescriptionUnk4     = '';

SET @ZandalariTrollAchievementenUS            = 'Realm First! Level 80 Zandalari Troll';
SET @ZandalariTrollAchievementkoKR            = '';
SET @ZandalariTrollAchievementfrFR            = '';
SET @ZandalariTrollAchievementdeDE            = '';
SET @ZandalariTrollAchievementzhCN            = '';
SET @ZandalariTrollAchievementzhTW            = '';
SET @ZandalariTrollAchievementesES            = '';
SET @ZandalariTrollAchievementesMX            = '';
SET @ZandalariTrollAchievementruRU            = '';
SET @ZandalariTrollAchievementjaJP            = '';
SET @ZandalariTrollAchievementptPT            = '';
SET @ZandalariTrollAchievementitIT            = '';
SET @ZandalariTrollAchievementUnk1            = '';
SET @ZandalariTrollAchievementUnk2            = '';
SET @ZandalariTrollAchievementUnk3            = '';
SET @ZandalariTrollAchievementUnk4            = '';

SET @ZandalariTrollAchievementDescriptionenUS = 'First Zandalari Troll on the realm to achieve level 80.';
SET @ZandalariTrollAchievementDescriptionkoKR = '';
SET @ZandalariTrollAchievementDescriptionfrFR = '';
SET @ZandalariTrollAchievementDescriptiondeDE = '';
SET @ZandalariTrollAchievementDescriptionzhCN = '';
SET @ZandalariTrollAchievementDescriptionzhTW = '';
SET @ZandalariTrollAchievementDescriptionesES = '';
SET @ZandalariTrollAchievementDescriptionesMX = '';
SET @ZandalariTrollAchievementDescriptionruRU = '';
SET @ZandalariTrollAchievementDescriptionjaJP = '';
SET @ZandalariTrollAchievementDescriptionptPT = '';
SET @ZandalariTrollAchievementDescriptionitIT = '';
SET @ZandalariTrollAchievementDescriptionUnk1 = '';
SET @ZandalariTrollAchievementDescriptionUnk2 = '';
SET @ZandalariTrollAchievementDescriptionUnk3 = '';
SET @ZandalariTrollAchievementDescriptionUnk4 = '';

-- Racial Mount Strings
SET @ZandalariTrollMount1NameenUS                    = 'Zandalari Direhorn';
SET @ZandalariTrollMount1NamekoKR                    = '';
SET @ZandalariTrollMount1NamefrFR                    = '';
SET @ZandalariTrollMount1NamedeDE                    = '';
SET @ZandalariTrollMount1NamezhCN                    = '';
SET @ZandalariTrollMount1NamezhTW                    = '';
SET @ZandalariTrollMount1NameesES                    = '';
SET @ZandalariTrollMount1NameesMX                    = '';
SET @ZandalariTrollMount1NameruRU                    = '';
SET @ZandalariTrollMount1NamejaJP                    = '';
SET @ZandalariTrollMount1NameptPT                    = '';
SET @ZandalariTrollMount1NameitIT                    = '';
SET @ZandalariTrollMount1NameUnk1                    = '';
SET @ZandalariTrollMount1NameUnk2                    = '';
SET @ZandalariTrollMount1NameUnk3                    = '';
SET @ZandalariTrollMount1NameUnk4                    = '';

SET @ZandalariTrollMount1SpellDescriptionenUS        = 'Summons and dismisses a rideable Zandalari Direhorn.';
SET @ZandalariTrollMount1SpellDescriptionkoKR        = '';
SET @ZandalariTrollMount1SpellDescriptionfrFR        = '';
SET @ZandalariTrollMount1SpellDescriptiondeDE        = '';
SET @ZandalariTrollMount1SpellDescriptionzhCN        = '';
SET @ZandalariTrollMount1SpellDescriptionzhTW        = '';
SET @ZandalariTrollMount1SpellDescriptionesES        = '';
SET @ZandalariTrollMount1SpellDescriptionesMX        = '';
SET @ZandalariTrollMount1SpellDescriptionruRU        = '';
SET @ZandalariTrollMount1SpellDescriptionjaJP        = '';
SET @ZandalariTrollMount1SpellDescriptionptPT        = '';
SET @ZandalariTrollMount1SpellDescriptionitIT        = '';
SET @ZandalariTrollMount1SpellDescriptionUnk1        = '';
SET @ZandalariTrollMount1SpellDescriptionUnk2        = '';
SET @ZandalariTrollMount1SpellDescriptionUnk3        = '';
SET @ZandalariTrollMount1SpellDescriptionUnk4        = '';

SET @ZandalariTrollMount1ItemNameenUS                = @ZandalariTrollMount1NameenUS;
SET @ZandalariTrollMount1ItemDescriptionenUS         = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Zandalari Direhorn.';
