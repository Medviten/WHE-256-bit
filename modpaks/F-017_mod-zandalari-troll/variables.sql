-- Race ID
SET @ZandalariTroll                          := @NextRace := @NextRace +1;  -- default: 17
SET @ZandalariTrollMask                       = 1 << (@ZandalariTroll - 1); -- race ID 17 → 65536
SET @ZandalariTrollHelmetMask                 = 1 << @ZandalariTroll;       -- race ID 17 → 131072

-- Important variable update
SET @HordeMask                                = @HordeMask | @ZandalariTrollMask;
SET @BarrensBros                              = @HordeMask & ~@UndercityMask;
SET @PlayableRaceMask                         = @AllianceMask | @HordeMask;
SET @BowHunters                               = @BowHunters   | @ZandalariTrollMask;
SET @ZandalariTrollLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @ZandalariTrollAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @ZandalariTrollExplorationSound           = @TrollExplorationSound;
SET @ZandalariTrollCinematicSequence          = @TrollCinematicSequence;
SET @ZandalariTrollBlood                      = 1;
SET @ZandalariTrollMaleModelPath              = 'Character\\ZandalariTroll\\male\\ZandalariTrollMale.M2';
SET @ZandalariTrollFemaleModelPath            = 'Character\\ZandalariTroll\\female\\ZandalariTrollFemale.M2';
SET @ZandalariTrollMaleFootprint              = @FootprintShoe;
SET @ZandalariTrollFemaleFootprint            = @FootprintShoe;

-- Strings
SET @ZandalariTrollClientPrefix               = 'Tr';
SET @ZandalariTrollClientString               = 'ZandalariTroll';

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
