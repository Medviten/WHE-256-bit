-- Race ID
SET @HordePandaren                          := @NextRace := @NextRace +1; -- default: 20
SET @HordePandarenMask                       = 1 << (@HordePandaren - 1); -- race ID 20 → 524288
SET @HordePandarenHelmetMask                 = 1 << @HordePandaren;       -- race ID 20 → 1048576

-- Important variable update
SET @HordeMask                               = @HordeMask       |  @HordePandarenMask;
SET @BarrensBros                             = @HordeMask       & ~@UndercityMask;
SET @PlayableRaceMask                        = @AllianceMask    |  @HordeMask;
SET @CrossbowHunters                         = @CrossbowHunters |  @HordePandarenMask;
SET @HordePandarenLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @HordePandarenAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @HordePandarenExplorationSound           = @TaurenExplorationSound;
SET @HordePandarenCinematicSequence          = @TaurenCinematicSequence;

-- Miscellaneous
SET @HordePandarenExplorationSound           = @TaurenExplorationSound;
SET @HordePandarenCinematicSequence          = @TaurenCinematicSequence;
SET @HordePandarenBlood                      = 1;
SET @HordePandarenMaleModelPath              = 'Character\\Pandaren\\Male\\PandarenMale.mdx';
SET @HordePandarenFemaleModelPath            = 'Character\\Pandaren\\Female\\PandarenFemale.mdx';
SET @HordePandarenMaleFootprint              = @FootprintPaw;
SET @HordePandarenFemaleFootprint            = @FootprintPaw;

-- Strings
SET @HordePandarenClientPrefix               = 'Pa';
SET @HordePandarenClientString               = 'HordePandaren';

-- Localization Strings
SET @HordePandarenenUS                       = 'Pandaren';
SET @HordePandarenkoKR                       = '';
SET @HordePandarenfrFR                       = '';
SET @HordePandarendeDE                       = '';
SET @HordePandarenzhCN                       = '';
SET @HordePandarenzhTW                       = '';
SET @HordePandarenesES                       = '';
SET @HordePandarenesMX                       = '';
SET @HordePandarenruRU                       = '';
SET @HordePandarenjaJP                       = '';
SET @HordePandarenptPT                       = '';
SET @HordePandarenitIT                       = '';

SET @HordePandarenFemaleenUS                 = '';
SET @HordePandarenFemalekoKR                 = '';
SET @HordePandarenFemalefrFR                 = '';
SET @HordePandarenFemaledeDE                 = '';
SET @HordePandarenFemalezhCN                 = '';
SET @HordePandarenFemalezhTW                 = '';
SET @HordePandarenFemaleesES                 = '';
SET @HordePandarenFemaleesMX                 = '';
SET @HordePandarenFemaleruRU                 = '';
SET @HordePandarenFemalejaJP                 = '';
SET @HordePandarenFemaleptPT                 = '';
SET @HordePandarenFemaleitIT                 = '';

SET @HordePandarenMaleenUS                   = '';
SET @HordePandarenMalekoKR                   = '';
SET @HordePandarenMalefrFR                   = '';
SET @HordePandarenMaledeDE                   = '';
SET @HordePandarenMalezhCN                   = '';
SET @HordePandarenMalezhTW                   = '';
SET @HordePandarenMaleesES                   = '';
SET @HordePandarenMaleesMX                   = '';
SET @HordePandarenMaleruRU                   = '';
SET @HordePandarenMalejaJP                   = '';
SET @HordePandarenMaleptPT                   = '';
SET @HordePandarenMaleitIT                   = '';

SET @HordePandarenRacialNameenUS             = 'Racial - Pandaren';
SET @HordePandarenRacialNamekoKR             = '';
SET @HordePandarenRacialNamefrFR             = '';
SET @HordePandarenRacialNamedeDE             = '';
SET @HordePandarenRacialNamezhCN             = '';
SET @HordePandarenRacialNamezhTW             = '';
SET @HordePandarenRacialNameesES             = '';
SET @HordePandarenRacialNameesMX             = '';
SET @HordePandarenRacialNameruRU             = '';
SET @HordePandarenRacialNamejaJP             = '';
SET @HordePandarenRacialNameptPT             = '';
SET @HordePandarenRacialNameitIT             = '';

SET @HordePandarenPlayerenUS                 = '"PLAYER"," Pandaren (Horde)"';
SET @HordePandarenPlayerkoKR                 = '';
SET @HordePandarenPlayerfrFR                 = '';
SET @HordePandarenPlayerdeDE                 = '';
SET @HordePandarenPlayerzhCN                 = '';
SET @HordePandarenPlayerzhTW                 = '';
SET @HordePandarenPlayeresES                 = '';
SET @HordePandarenPlayeresMX                 = '';
SET @HordePandarenPlayerruRU                 = '';
SET @HordePandarenPlayerjaJP                 = '';
SET @HordePandarenPlayerptPT                 = '';
SET @HordePandarenPlayeritIT                 = '';

SET @HordePandarenFactionNameenUS            = 'Huojin Pandaren';
SET @HordePandarenFactionNamekoKR            = '';
SET @HordePandarenFactionNamefrFR            = '';
SET @HordePandarenFactionNamedeDE            = '';
SET @HordePandarenFactionNamezhCN            = '';
SET @HordePandarenFactionNamezhTW            = '';
SET @HordePandarenFactionNameesES            = '';
SET @HordePandarenFactionNameesMX            = '';
SET @HordePandarenFactionNameruRU            = '';
SET @HordePandarenFactionNamejaJP            = '';
SET @HordePandarenFactionNameptPT            = '';
SET @HordePandarenFactionNameitIT            = '';

SET @HordePandarenFactionDescriptionenUS     = 'Led by the intrepid Ji Firepaw, the Huojin Pandaren are quick to act and quicker to fight for what they believe in.';
SET @HordePandarenFactionDescriptionkoKR     = '';
SET @HordePandarenFactionDescriptionfrFR     = '';
SET @HordePandarenFactionDescriptiondeDE     = '';
SET @HordePandarenFactionDescriptionzhCN     = '';
SET @HordePandarenFactionDescriptionzhTW     = '';
SET @HordePandarenFactionDescriptionesES     = '';
SET @HordePandarenFactionDescriptionesMX     = '';
SET @HordePandarenFactionDescriptionruRU     = '';
SET @HordePandarenFactionDescriptionjaJP     = '';
SET @HordePandarenFactionDescriptionptPT     = '';
SET @HordePandarenFactionDescriptionitIT     = '';

SET @HordePandarenAchievementenUS            = 'Realm First! Level 80 Pandaren (Horde)';
SET @HordePandarenAchievementkoKR            = '';
SET @HordePandarenAchievementfrFR            = '';
SET @HordePandarenAchievementdeDE            = '';
SET @HordePandarenAchievementzhCN            = '';
SET @HordePandarenAchievementzhTW            = '';
SET @HordePandarenAchievementesES            = '';
SET @HordePandarenAchievementesMX            = '';
SET @HordePandarenAchievementruRU            = '';
SET @HordePandarenAchievementjaJP            = '';
SET @HordePandarenAchievementptPT            = '';
SET @HordePandarenAchievementitIT            = '';

SET @HordePandarenAchievementDescriptionenUS = 'First (Horde) Pandaren on the realm to achieve level 80.';
SET @HordePandarenAchievementDescriptionkoKR = '';
SET @HordePandarenAchievementDescriptionfrFR = '';
SET @HordePandarenAchievementDescriptiondeDE = '';
SET @HordePandarenAchievementDescriptionzhCN = '';
SET @HordePandarenAchievementDescriptionzhTW = '';
SET @HordePandarenAchievementDescriptionesES = '';
SET @HordePandarenAchievementDescriptionesMX = '';
SET @HordePandarenAchievementDescriptionruRU = '';
SET @HordePandarenAchievementDescriptionjaJP = '';
SET @HordePandarenAchievementDescriptionptPT = '';
SET @HordePandarenAchievementDescriptionitIT = '';
