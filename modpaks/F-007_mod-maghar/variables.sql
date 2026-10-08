-- Race ID
SET @MagharOrc := @NextRace             := @NextRace +1; -- default: 14
SET @MagharOrcMask                       = 1 << (@MagharOrc - 1);  -- race ID 14 → 8192
SET @MagharOrcHelmetMask                 = 1 << @MagharOrc;  -- race ID 14 → 16384

-- Important variable update
SET @HordeMask                           = @HordeMask    |  @MagharOrcMask;
SET @BarrensBros                         = @HordeMask    & ~@UndercityMask;
SET @PlayableRaceMask                    = @AllianceMask |  @HordeMask;
SET @BowHunters                          = @BowHunters   |  @MagharOrcMask;

-- Miscellaneous
SET @MagharOrcExplorationSound           = @OrcExplorationSound;
SET @MagharOrcCinematicSequence          = @OrcCinematicSequence;
SET @MagharOrcLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MagharOrcAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @MagharOrcExplorationSound           = @OrcExplorationSound;
SET @MagharOrcCinematicSequence          = @OrcCinematicSequence;
SET @MagharOrcBlood                      = 1;
SET @MagharOrcMaleModelPath              = 'Character\\Orc\\Male\\OrcMale.mdx';
SET @MagharOrcFemaleModelPath            = 'Character\\Orc\\Female\\OrcFemale.mdx';
SET @MagharOrcMaleFootprint              = @FootprintShoe;
SET @MagharOrcFemaleFootprint            = @FootprintShoe;

-- Strings
SET @MagharOrcClientPrefix               = 'Or';
SET @MagharOrcClientString               = 'MagharOrc';

-- Localization Strings
SET @MagharOrcenUS                       = 'MagharOrc';
SET @MagharOrckoKR                       = '';
SET @MagharOrcfrFR                       = '';
SET @MagharOrcdeDE                       = '';
SET @MagharOrczhCN                       = '';
SET @MagharOrczhTW                       = '';
SET @MagharOrcesES                       = '';
SET @MagharOrcesMX                       = '';
SET @MagharOrcruRU                       = '';
SET @MagharOrcjaJP                       = '';
SET @MagharOrcptPT                       = '';
SET @MagharOrcitIT                       = '';

SET @MagharOrcFemaleenUS                 = '';
SET @MagharOrcFemalekoKR                 = '';
SET @MagharOrcFemalefrFR                 = '';
SET @MagharOrcFemaledeDE                 = '';
SET @MagharOrcFemalezhCN                 = '';
SET @MagharOrcFemalezhTW                 = '';
SET @MagharOrcFemaleesES                 = '';
SET @MagharOrcFemaleesMX                 = '';
SET @MagharOrcFemaleruRU                 = '';
SET @MagharOrcFemalejaJP                 = '';
SET @MagharOrcFemaleptPT                 = '';
SET @MagharOrcFemaleitIT                 = '';

SET @MagharOrcMaleenUS                   = '';
SET @MagharOrcMalekoKR                   = '';
SET @MagharOrcMalefrFR                   = '';
SET @MagharOrcMaledeDE                   = '';
SET @MagharOrcMalezhCN                   = '';
SET @MagharOrcMalezhTW                   = '';
SET @MagharOrcMaleesES                   = '';
SET @MagharOrcMaleesMX                   = '';
SET @MagharOrcMaleruRU                   = '';
SET @MagharOrcMalejaJP                   = '';
SET @MagharOrcMaleptPT                   = '';
SET @MagharOrcMaleitIT                   = '';

SET @MagharOrcRacialNameenUS             = 'Racial - Maghar Orc';
SET @MagharOrcRacialNamekoKR             = '';
SET @MagharOrcRacialNamefrFR             = '';
SET @MagharOrcRacialNamedeDE             = '';
SET @MagharOrcRacialNamezhCN             = '';
SET @MagharOrcRacialNamezhTW             = '';
SET @MagharOrcRacialNameesES             = '';
SET @MagharOrcRacialNameesMX             = '';
SET @MagharOrcRacialNameruRU             = '';
SET @MagharOrcRacialNamejaJP             = '';
SET @MagharOrcRacialNameptPT             = '';
SET @MagharOrcRacialNameitIT             = '';

SET @MagharOrcPlayerenUS                 = '"PLAYER"," Maghar Orc"';
SET @MagharOrcPlayerkoKR                 = '';
SET @MagharOrcPlayerfrFR                 = '';
SET @MagharOrcPlayerdeDE                 = '';
SET @MagharOrcPlayerzhCN                 = '';
SET @MagharOrcPlayerzhTW                 = '';
SET @MagharOrcPlayeresES                 = '';
SET @MagharOrcPlayeresMX                 = '';
SET @MagharOrcPlayerruRU                 = '';
SET @MagharOrcPlayerjaJP                 = '';
SET @MagharOrcPlayerptPT                 = '';
SET @MagharOrcPlayeritIT                 = '';

SET @MagharOrcFactionNameenUS            = '';
SET @MagharOrcFactionNamekoKR            = '';
SET @MagharOrcFactionNamefrFR            = '';
SET @MagharOrcFactionNamedeDE            = '';
SET @MagharOrcFactionNamezhCN            = '';
SET @MagharOrcFactionNamezhTW            = '';
SET @MagharOrcFactionNameesES            = '';
SET @MagharOrcFactionNameesMX            = '';
SET @MagharOrcFactionNameruRU            = '';
SET @MagharOrcFactionNamejaJP            = '';
SET @MagharOrcFactionNameptPT            = '';
SET @MagharOrcFactionNameitIT            = '';

SET @MagharOrcFactionDescriptionenUS     = '';
SET @MagharOrcFactionDescriptionkoKR     = '';
SET @MagharOrcFactionDescriptionfrFR     = '';
SET @MagharOrcFactionDescriptiondeDE     = '';
SET @MagharOrcFactionDescriptionzhCN     = '';
SET @MagharOrcFactionDescriptionzhTW     = '';
SET @MagharOrcFactionDescriptionesES     = '';
SET @MagharOrcFactionDescriptionesMX     = '';
SET @MagharOrcFactionDescriptionruRU     = '';
SET @MagharOrcFactionDescriptionjaJP     = '';
SET @MagharOrcFactionDescriptionptPT     = '';
SET @MagharOrcFactionDescriptionitIT     = '';

SET @MagharOrcAchievementenUS            = '';
SET @MagharOrcAchievementkoKR            = '';
SET @MagharOrcAchievementfrFR            = '';
SET @MagharOrcAchievementdeDE            = '';
SET @MagharOrcAchievementzhCN            = '';
SET @MagharOrcAchievementzhTW            = '';
SET @MagharOrcAchievementesES            = '';
SET @MagharOrcAchievementesMX            = '';
SET @MagharOrcAchievementruRU            = '';
SET @MagharOrcAchievementjaJP            = '';
SET @MagharOrcAchievementptPT            = '';
SET @MagharOrcAchievementitIT            = '';

SET @MagharOrcAchievementDescriptionenUS = '';
SET @MagharOrcAchievementDescriptionkoKR = '';
SET @MagharOrcAchievementDescriptionfrFR = '';
SET @MagharOrcAchievementDescriptiondeDE = '';
SET @MagharOrcAchievementDescriptionzhCN = '';
SET @MagharOrcAchievementDescriptionzhTW = '';
SET @MagharOrcAchievementDescriptionesES = '';
SET @MagharOrcAchievementDescriptionesMX = '';
SET @MagharOrcAchievementDescriptionruRU = '';
SET @MagharOrcAchievementDescriptionjaJP = '';
SET @MagharOrcAchievementDescriptionptPT = '';
SET @MagharOrcAchievementDescriptionitIT = '';
