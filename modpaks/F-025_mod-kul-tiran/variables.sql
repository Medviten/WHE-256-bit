-- Race ID
SET @KulTiran                          := @NextRace := @NextRace +1; -- default: 21
SET @KulTiranMask                       = 1 << (@KulTiran - 1);      -- race ID 21 → 1048576
SET @KulTiranHelmetMask                 = 1 << @KulTiran;            -- race ID 21 → 2097152

-- Important variable updates (Alliance vs. Horde)
SET @AllianceMask                       = @AllianceMask    | @KulTiranMask;
SET @BarrensBros                        = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                   = @AllianceMask    | @HordeMask;
SET @CrossbowHunters                    = @CrossbowHunters | @KulTiranMask;
SET @KulTiranLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @KulTiranAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @KulTiranKnowThyEnemy               = @KnowThyEnemyAlliance;

-- Miscellaneous
SET @KulTiranExplorationSound           = @HumanExplorationSound;
SET @KulTiranCinematicSequence          = @HumanCinematicSequence;
SET @KulTiranBlood                      = 1;
SET @KulTiranMaleModelPath              = 'Character\\Kultiran\\Male\\KulTiranMale.mdx';
SET @KulTiranFemaleModelPath            = 'Character\\Kultiran\\Female\\KulTiranFemale.mdx';
SET @KulTiranMaleFootprint              = @FootprintShoe;
SET @KulTiranFemaleFootprint            = @FootprintShoe;

-- Strings
SET @KulTiranClientPrefix               = 'Kt';
SET @KulTiranClientString               = 'KulTiran';

-- Localization Strings
SET @KulTiranenUS                       = 'Kul Tiran';
SET @KulTirankoKR                       = '';
SET @KulTiranfrFR                       = '';
SET @KulTirandeDE                       = '';
SET @KulTiranzhCN                       = '';
SET @KulTiranzhTW                       = '';
SET @KulTiranesES                       = '';
SET @KulTiranesMX                       = '';
SET @KulTiranruRU                       = '';
SET @KulTiranjaJP                       = '';
SET @KulTiranptPT                       = '';
SET @KulTiranitIT                       = '';

SET @KulTiranFemaleenUS                 = '';
SET @KulTiranFemalekoKR                 = '';
SET @KulTiranFemalefrFR                 = '';
SET @KulTiranFemaledeDE                 = '';
SET @KulTiranFemalezhCN                 = '';
SET @KulTiranFemalezhTW                 = '';
SET @KulTiranFemaleesES                 = '';
SET @KulTiranFemaleesMX                 = '';
SET @KulTiranFemaleruRU                 = '';
SET @KulTiranFemalejaJP                 = '';
SET @KulTiranFemaleptPT                 = '';
SET @KulTiranFemaleitIT                 = '';

SET @KulTiranMaleenUS                   = '';
SET @KulTiranMalekoKR                   = '';
SET @KulTiranMalefrFR                   = '';
SET @KulTiranMaledeDE                   = '';
SET @KulTiranMalezhCN                   = '';
SET @KulTiranMalezhTW                   = '';
SET @KulTiranMaleesES                   = '';
SET @KulTiranMaleesMX                   = '';
SET @KulTiranMaleruRU                   = '';
SET @KulTiranMalejaJP                   = '';
SET @KulTiranMaleptPT                   = '';
SET @KulTiranMaleitIT                   = '';

SET @KulTiranRacialNameenUS             = 'Racial - Kul Tiran';
SET @KulTiranRacialNamekoKR             = '';
SET @KulTiranRacialNamefrFR             = '';
SET @KulTiranRacialNamedeDE             = '';
SET @KulTiranRacialNamezhCN             = '';
SET @KulTiranRacialNamezhTW             = '';
SET @KulTiranRacialNameesES             = '';
SET @KulTiranRacialNameesMX             = '';
SET @KulTiranRacialNameruRU             = '';
SET @KulTiranRacialNamejaJP             = '';
SET @KulTiranRacialNameptPT             = '';
SET @KulTiranRacialNameitIT             = '';

SET @KulTiranPlayerenUS                 = '"PLAYER", " Kul Tiran"';
SET @KulTiranPlayerkoKR                 = '';
SET @KulTiranPlayerfrFR                 = '';
SET @KulTiranPlayerdeDE                 = '';
SET @KulTiranPlayerzhCN                 = '';
SET @KulTiranPlayerzhTW                 = '';
SET @KulTiranPlayeresES                 = '';
SET @KulTiranPlayeresMX                 = '';
SET @KulTiranPlayerruRU                 = '';
SET @KulTiranPlayerjaJP                 = '';
SET @KulTiranPlayerptPT                 = '';
SET @KulTiranPlayeritIT                 = '';

SET @KulTiranFactionNameenUS            = 'Kul Tiras';
SET @KulTiranFactionNamekoKR            = '';
SET @KulTiranFactionNamefrFR            = '';
SET @KulTiranFactionNamedeDE            = '';
SET @KulTiranFactionNamezhCN            = '';
SET @KulTiranFactionNamezhTW            = '';
SET @KulTiranFactionNameesES            = '';
SET @KulTiranFactionNameesMX            = '';
SET @KulTiranFactionNameruRU            = '';
SET @KulTiranFactionNamejaJP            = '';
SET @KulTiranFactionNameptPT            = '';
SET @KulTiranFactionNameitIT            = '';

SET @KulTiranFactionDescriptionenUS     = 'The kingdom of Kul Tiras.';
SET @KulTiranFactionDescriptionkoKR     = '쿨 티라스 왕국입니다.';
SET @KulTiranFactionDescriptionfrFR     = 'Le royaume de Kul Tiras.';
SET @KulTiranFactionDescriptiondeDE     = 'Das Königreich Kul Tiras.';
SET @KulTiranFactionDescriptionzhCN     = '库尔提拉斯王国。';
SET @KulTiranFactionDescriptionzhTW     = '庫爾提拉斯王國。';
SET @KulTiranFactionDescriptionesES     = 'El reino de Kul Tiras.';
SET @KulTiranFactionDescriptionesMX     = 'El reino de Kul Tiras.';
SET @KulTiranFactionDescriptionruRU     = '';
SET @KulTiranFactionDescriptionjaJP     = '';
SET @KulTiranFactionDescriptionptPT     = '';
SET @KulTiranFactionDescriptionitIT     = '';

SET @KulTiranAchievementenUS            = 'Realm First! Level 80 Kul Tiran';
SET @KulTiranAchievementkoKR            = '';
SET @KulTiranAchievementfrFR            = '';
SET @KulTiranAchievementdeDE            = '';
SET @KulTiranAchievementzhCN            = '';
SET @KulTiranAchievementzhTW            = '';
SET @KulTiranAchievementesES            = '';
SET @KulTiranAchievementesMX            = '';
SET @KulTiranAchievementruRU            = '';
SET @KulTiranAchievementjaJP            = '';
SET @KulTiranAchievementptPT            = '';
SET @KulTiranAchievementitIT            = '';

SET @KulTiranAchievementDescriptionenUS = 'First Kul Tiran on the realm to achieve level 80.';
SET @KulTiranAchievementDescriptionkoKR = '';
SET @KulTiranAchievementDescriptionfrFR = '';
SET @KulTiranAchievementDescriptiondeDE = '';
SET @KulTiranAchievementDescriptionzhCN = '';
SET @KulTiranAchievementDescriptionzhTW = '';
SET @KulTiranAchievementDescriptionesES = '';
SET @KulTiranAchievementDescriptionesMX = '';
SET @KulTiranAchievementDescriptionruRU = '';
SET @KulTiranAchievementDescriptionjaJP = '';
SET @KulTiranAchievementDescriptionptPT = '';
SET @KulTiranAchievementDescriptionitIT = '';
