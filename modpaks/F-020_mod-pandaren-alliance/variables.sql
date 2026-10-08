-- Race ID
SET @AlliancePandaren                          := @NextRace := @NextRace +1;    -- default: 19
SET @AlliancePandarenMask                       = 1 << (@AlliancePandaren - 1); -- race ID 19 → 262144
SET @AlliancePandarenHelmetMask                 = 1 << @AlliancePandaren;       -- race ID 19 → 524288

-- Important variable update
SET @AllianceMask                               = @AllianceMask    | @AlliancePandarenMask;
SET @PlayableRaceMask                           = @AllianceMask    | @HordeMask;
SET @CrossbowHunters                            = @CrossbowHunters | @AlliancePandarenMask;
SET @AlliancePandarenLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @AlliancePandarenAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @AlliancePandarenExplorationSound           = @TaurenExplorationSound;
SET @AlliancePandarenCinematicSequence          = @HumanCinematicSequence;
SET @AlliancePandarenBlood                      = 1;
SET @AlliancePandarenMaleModelPath              = 'Character\\Pandaren\\Male\\PandarenMale.mdx';
SET @AlliancePandarenFemaleModelPath            = 'Character\\Pandaren\\Female\\PandarenFemale.mdx';
SET @AlliancePandarenMaleFootprint              = @FootprintPaw;
SET @AlliancePandarenFemaleFootprint            = @FootprintPaw;

-- Strings
SET @AlliancePandarenClientPrefix               = 'Pa';
SET @AlliancePandarenClientString               = 'AlliancePandaren';

-- Localization Strings
SET @AlliancePandarenenUS                       = 'Pandaren';
SET @AlliancePandarenkoKR                       = '';
SET @AlliancePandarenfrFR                       = '';
SET @AlliancePandarendeDE                       = '';
SET @AlliancePandarenzhCN                       = '';
SET @AlliancePandarenzhTW                       = '';
SET @AlliancePandarenesES                       = '';
SET @AlliancePandarenesMX                       = '';
SET @AlliancePandarenruRU                       = '';
SET @AlliancePandarenjaJP                       = '';
SET @AlliancePandarenptPT                       = '';
SET @AlliancePandarenitIT                       = '';

SET @AlliancePandarenFemaleenUS                 = '';
SET @AlliancePandarenFemalekoKR                 = '';
SET @AlliancePandarenFemalefrFR                 = '';
SET @AlliancePandarenFemaledeDE                 = '';
SET @AlliancePandarenFemalezhCN                 = '';
SET @AlliancePandarenFemalezhTW                 = '';
SET @AlliancePandarenFemaleesES                 = '';
SET @AlliancePandarenFemaleesMX                 = '';
SET @AlliancePandarenFemaleruRU                 = '';
SET @AlliancePandarenFemalejaJP                 = '';
SET @AlliancePandarenFemaleptPT                 = '';
SET @AlliancePandarenFemaleitIT                 = '';

SET @AlliancePandarenMaleenUS                   = '';
SET @AlliancePandarenMalekoKR                   = '';
SET @AlliancePandarenMalefrFR                   = '';
SET @AlliancePandarenMaledeDE                   = '';
SET @AlliancePandarenMalezhCN                   = '';
SET @AlliancePandarenMalezhTW                   = '';
SET @AlliancePandarenMaleesES                   = '';
SET @AlliancePandarenMaleesMX                   = '';
SET @AlliancePandarenMaleruRU                   = '';
SET @AlliancePandarenMalejaJP                   = '';
SET @AlliancePandarenMaleptPT                   = '';
SET @AlliancePandarenMaleitIT                   = '';

SET @AlliancePandarenRacialNameenUS             = 'Racial - Pandaren';
SET @AlliancePandarenRacialNamekoKR             = '';
SET @AlliancePandarenRacialNamefrFR             = '';
SET @AlliancePandarenRacialNamedeDE             = '';
SET @AlliancePandarenRacialNamezhCN             = '';
SET @AlliancePandarenRacialNamezhTW             = '';
SET @AlliancePandarenRacialNameesES             = '';
SET @AlliancePandarenRacialNameesMX             = '';
SET @AlliancePandarenRacialNameruRU             = '';
SET @AlliancePandarenRacialNamejaJP             = '';
SET @AlliancePandarenRacialNameptPT             = '';
SET @AlliancePandarenRacialNameitIT             = '';

SET @AlliancePandarenPlayerenUS                 = '"PLAYER", " Pandaren (Alliance)"';
SET @AlliancePandarenPlayerkoKR                 = '';
SET @AlliancePandarenPlayerfrFR                 = '';
SET @AlliancePandarenPlayerdeDE                 = '';
SET @AlliancePandarenPlayerzhCN                 = '';
SET @AlliancePandarenPlayerzhTW                 = '';
SET @AlliancePandarenPlayeresES                 = '';
SET @AlliancePandarenPlayeresMX                 = '';
SET @AlliancePandarenPlayerruRU                 = '';
SET @AlliancePandarenPlayerjaJP                 = '';
SET @AlliancePandarenPlayerptPT                 = '';
SET @AlliancePandarenPlayeritIT                 = '';

SET @AlliancePandarenFactionNameenUS            = 'Tushui Pandaren';
SET @AlliancePandarenFactionNamekoKR            = '';
SET @AlliancePandarenFactionNamefrFR            = '';
SET @AlliancePandarenFactionNamedeDE            = '';
SET @AlliancePandarenFactionNamezhCN            = '';
SET @AlliancePandarenFactionNamezhTW            = '';
SET @AlliancePandarenFactionNameesES            = '';
SET @AlliancePandarenFactionNameesMX            = '';
SET @AlliancePandarenFactionNameruRU            = '';
SET @AlliancePandarenFactionNamejaJP            = '';
SET @AlliancePandarenFactionNameptPT            = '';
SET @AlliancePandarenFactionNameitIT            = '';

SET @AlliancePandarenFactionDescriptionenUS     = 'Led by the stalwart Aysa Cloudsinger, the Tushui Pandaren believe in contemplation and reasoned action.';
SET @AlliancePandarenFactionDescriptionkoKR     = '';
SET @AlliancePandarenFactionDescriptionfrFR     = '';
SET @AlliancePandarenFactionDescriptiondeDE     = '';
SET @AlliancePandarenFactionDescriptionzhCN     = '';
SET @AlliancePandarenFactionDescriptionzhTW     = '';
SET @AlliancePandarenFactionDescriptionesES     = '';
SET @AlliancePandarenFactionDescriptionesMX     = '';
SET @AlliancePandarenFactionDescriptionruRU     = '';
SET @AlliancePandarenFactionDescriptionjaJP     = '';
SET @AlliancePandarenFactionDescriptionptPT     = '';
SET @AlliancePandarenFactionDescriptionitIT     = '';

SET @AlliancePandarenAchievementenUS            = 'Realm First! Level 80 Pandaren (Alliance)';
SET @AlliancePandarenAchievementkoKR            = '';
SET @AlliancePandarenAchievementfrFR            = '';
SET @AlliancePandarenAchievementdeDE            = '';
SET @AlliancePandarenAchievementzhCN            = '';
SET @AlliancePandarenAchievementzhTW            = '';
SET @AlliancePandarenAchievementesES            = '';
SET @AlliancePandarenAchievementesMX            = '';
SET @AlliancePandarenAchievementruRU            = '';
SET @AlliancePandarenAchievementjaJP            = '';
SET @AlliancePandarenAchievementptPT            = '';
SET @AlliancePandarenAchievementitIT            = '';

SET @AlliancePandarenAchievementDescriptionenUS = 'First (Alliance) Pandaren on the realm to achieve level 80.';
SET @AlliancePandarenAchievementDescriptionkoKR = '';
SET @AlliancePandarenAchievementDescriptionfrFR = '';
SET @AlliancePandarenAchievementDescriptiondeDE = '';
SET @AlliancePandarenAchievementDescriptionzhCN = '';
SET @AlliancePandarenAchievementDescriptionzhTW = '';
SET @AlliancePandarenAchievementDescriptionesES = '';
SET @AlliancePandarenAchievementDescriptionesMX = '';
SET @AlliancePandarenAchievementDescriptionruRU = '';
SET @AlliancePandarenAchievementDescriptionjaJP = '';
SET @AlliancePandarenAchievementDescriptionptPT = '';
SET @AlliancePandarenAchievementDescriptionitIT = '';
