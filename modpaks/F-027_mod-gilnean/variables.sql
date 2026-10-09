-- Race ID
SET @Gilnean                           := @NextRace := @NextRace +1; -- default: 23
SET @GilneanMask                       = 1 << (@Gilnean - 1);        -- default: 4194304
SET @GilneanHelmetMask                 = 1 << @Gilnean;              -- default: 8388608

-- Important variable update
SET @AllianceMask                      = @AllianceMask     | @GilneanMask;
SET @PlayableRaceMask                  = @PlayableRaceMask | @GilneanMask;
SET @GunHunters                        = @GunHunters       | @GilneanMask;
SET @GilneanLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @GilneanAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @GilneanExplorationSound           = @HumanExplorationSound;
SET @GilneanCinematicSequence          = @HumanCinematicSequence;
SET @GilneanBlood                      = 1;
SET @GilneanMaleModelPath              = 'Character\\Gilnean\\Male\\GilneanMale.M2'; -- copied from 'Character\\Human\\Male\\HumanMale.mdx'
SET @GilneanFemaleModelPath            = 'Character\\Gilnean\\Female\\GilneanFemale.M2'; -- copied from 'Character\\Human\\Female\\HumanFemale.mdx'
SET @GilneanMaleFootprint              = @FootprintShoe;
SET @GilneanFemaleFootprint            = @FootprintShoe;

-- Strings
SET @GilneanClientPrefix               = 'Hu';
SET @GilneanClientString               = 'Gilnean';

-- Localization Strings
SET @GilneanenUS                       = 'Gilnean';
SET @GilneankoKR                       = '';
SET @GilneanfrFR                       = '';
SET @GilneandeDE                       = '';
SET @GilneanzhCN                       = '';
SET @GilneanzhTW                       = '';
SET @GilneanesES                       = '';
SET @GilneanesMX                       = '';
SET @GilneanruRU                       = '';
SET @GilneanjaJP                       = '';
SET @GilneanptPT                       = '';
SET @GilneanitIT                       = '';

SET @GilneanFemaleenUS                 = '';
SET @GilneanFemalekoKR                 = '';
SET @GilneanFemalefrFR                 = '';
SET @GilneanFemaledeDE                 = '';
SET @GilneanFemalezhCN                 = '';
SET @GilneanFemalezhTW                 = '';
SET @GilneanFemaleesES                 = '';
SET @GilneanFemaleesMX                 = '';
SET @GilneanFemaleruRU                 = '';
SET @GilneanFemalejaJP                 = '';
SET @GilneanFemaleptPT                 = '';
SET @GilneanFemaleitIT                 = '';

SET @GilneanMaleenUS                   = '';
SET @GilneanMalekoKR                   = '';
SET @GilneanMalefrFR                   = '';
SET @GilneanMaledeDE                   = '';
SET @GilneanMalezhCN                   = '';
SET @GilneanMalezhTW                   = '';
SET @GilneanMaleesES                   = '';
SET @GilneanMaleesMX                   = '';
SET @GilneanMaleruRU                   = '';
SET @GilneanMalejaJP                   = '';
SET @GilneanMaleptPT                   = '';
SET @GilneanMaleitIT                   = '';

SET @GilneanRacialNameenUS             = 'Racial - Gilnean';
SET @GilneanRacialNamekoKR             = '';
SET @GilneanRacialNamefrFR             = '';
SET @GilneanRacialNamedeDE             = '';
SET @GilneanRacialNamezhCN             = '';
SET @GilneanRacialNamezhTW             = '';
SET @GilneanRacialNameesES             = '';
SET @GilneanRacialNameesMX             = '';
SET @GilneanRacialNameruRU             = '';
SET @GilneanRacialNamejaJP             = '';
SET @GilneanRacialNameptPT             = '';
SET @GilneanRacialNameitIT             = '';

SET @GilneanPlayerenUS                 = '"PLAYER", " Gilnean"';
SET @GilneanPlayerkoKR                 = '';
SET @GilneanPlayerfrFR                 = '';
SET @GilneanPlayerdeDE                 = '';
SET @GilneanPlayerzhCN                 = '';
SET @GilneanPlayerzhTW                 = '';
SET @GilneanPlayeresES                 = '';
SET @GilneanPlayeresMX                 = '';
SET @GilneanPlayerruRU                 = '';
SET @GilneanPlayerjaJP                 = '';
SET @GilneanPlayerptPT                 = '';
SET @GilneanPlayeritIT                 = '';

SET @GilneanFactionNameenUS            = 'Gilneas';
SET @GilneanFactionNamekoKR            = '';
SET @GilneanFactionNamefrFR            = '';
SET @GilneanFactionNamedeDE            = '';
SET @GilneanFactionNamezhCN            = '';
SET @GilneanFactionNamezhTW            = '';
SET @GilneanFactionNameesES            = '';
SET @GilneanFactionNameesMX            = '';
SET @GilneanFactionNameruRU            = '';
SET @GilneanFactionNamejaJP            = '';
SET @GilneanFactionNameptPT            = '';
SET @GilneanFactionNameitIT            = '';

SET @GilneanFactionDescriptionenUS     = 'The human kingdom of Gilneas';
SET @GilneanFactionDescriptionkoKR     = '';
SET @GilneanFactionDescriptionfrFR     = '';
SET @GilneanFactionDescriptiondeDE     = '';
SET @GilneanFactionDescriptionzhCN     = '';
SET @GilneanFactionDescriptionzhTW     = '';
SET @GilneanFactionDescriptionesES     = '';
SET @GilneanFactionDescriptionesMX     = '';
SET @GilneanFactionDescriptionruRU     = '';
SET @GilneanFactionDescriptionjaJP     = '';
SET @GilneanFactionDescriptionptPT     = '';
SET @GilneanFactionDescriptionitIT     = '';

SET @GilneanAchievementenUS            = 'Realm First! Level 80 Gilnean';
SET @GilneanAchievementkoKR            = '';
SET @GilneanAchievementfrFR            = '';
SET @GilneanAchievementdeDE            = '';
SET @GilneanAchievementzhCN            = '';
SET @GilneanAchievementzhTW            = '';
SET @GilneanAchievementesES            = '';
SET @GilneanAchievementesMX            = '';
SET @GilneanAchievementruRU            = '';
SET @GilneanAchievementjaJP            = '';
SET @GilneanAchievementptPT            = '';
SET @GilneanAchievementitIT            = '';

SET @GilneanAchievementDescriptionenUS = 'First Gilnean on the realm to achieve level 80.';
SET @GilneanAchievementDescriptionkoKR = '';
SET @GilneanAchievementDescriptionfrFR = '';
SET @GilneanAchievementDescriptiondeDE = '';
SET @GilneanAchievementDescriptionzhCN = '';
SET @GilneanAchievementDescriptionzhTW = '';
SET @GilneanAchievementDescriptionesES = '';
SET @GilneanAchievementDescriptionesMX = '';
SET @GilneanAchievementDescriptionruRU = '';
SET @GilneanAchievementDescriptionjaJP = '';
SET @GilneanAchievementDescriptionptPT = '';
SET @GilneanAchievementDescriptionitIT = '';
