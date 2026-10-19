-- Race masks (race IDs are fixed in config.sql)
SET @KulTiranMask                       = 1 << (@KulTiran - 1);      -- race ID 32 → 2147483648
SET @KulTiranHelmetMask                 = 1 << @KulTiran;            -- race ID 32 → 4294967296

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

-- Mounts (IDs are global, see config.sql)
SET @KulTiranMount1                          = @SpellKulTiranCharger;
SET @KulTiranMount1Model                     = @KulTiranChargerModel;
SET @KulTiranMount1Display                   = @KulTiranChargerDisplay;
SET @KulTiranMount1CreatureID                = @KulTiranChargerCreatureID;
SET @KulTiranMount1Item                      = @KulTiranChargerItem;
SET @KulTiranMount1ItemDisplay               = @KulTiranChargerItemDisplay;
SET @KulTiranMount1IconID                    = @IconKulTiranCharger;
SET @KulTiranMount1IconName                  = 'inv_horsekultiran';
SET @KulTiranMount1IconPath                  = CONCAT('Interface\\Icons\\', @KulTiranMount1IconName);
SET @KulTiranMount1ModelPath                 = 'Creature\\horsekultiran\\horsekultiran.m2';

-- Strings
SET @KulTiranClientPrefix               = 'Kt';
SET @KulTiranClientString               = 'KulTiran';
SET @KulTiranFacialHairCustomization1   = 'NORMAL';
SET @KulTiranFacialHairCustomization2   = 'EARRINGS';
SET @KulTiranHairCustomization          = 'NORMAL';

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
SET @KulTiranUnk1                       = '';
SET @KulTiranUnk2                       = '';
SET @KulTiranUnk3                       = '';
SET @KulTiranUnk4                       = '';

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
SET @KulTiranFemaleUnk1                 = '';
SET @KulTiranFemaleUnk2                 = '';
SET @KulTiranFemaleUnk3                 = '';
SET @KulTiranFemaleUnk4                 = '';

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
SET @KulTiranMaleUnk1                   = '';
SET @KulTiranMaleUnk2                   = '';
SET @KulTiranMaleUnk3                   = '';
SET @KulTiranMaleUnk4                   = '';

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
SET @KulTiranRacialNameUnk1             = '';
SET @KulTiranRacialNameUnk2             = '';
SET @KulTiranRacialNameUnk3             = '';
SET @KulTiranRacialNameUnk4             = '';

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
SET @KulTiranPlayerUnk1                 = '';
SET @KulTiranPlayerUnk2                 = '';
SET @KulTiranPlayerUnk3                 = '';
SET @KulTiranPlayerUnk4                 = '';

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
SET @KulTiranFactionNameUnk1            = '';
SET @KulTiranFactionNameUnk2            = '';
SET @KulTiranFactionNameUnk3            = '';
SET @KulTiranFactionNameUnk4            = '';

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
SET @KulTiranFactionDescriptionUnk1     = '';
SET @KulTiranFactionDescriptionUnk2     = '';
SET @KulTiranFactionDescriptionUnk3     = '';
SET @KulTiranFactionDescriptionUnk4     = '';

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
SET @KulTiranAchievementUnk1            = '';
SET @KulTiranAchievementUnk2            = '';
SET @KulTiranAchievementUnk3            = '';
SET @KulTiranAchievementUnk4            = '';

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
SET @KulTiranAchievementDescriptionUnk1 = '';
SET @KulTiranAchievementDescriptionUnk2 = '';
SET @KulTiranAchievementDescriptionUnk3 = '';
SET @KulTiranAchievementDescriptionUnk4 = '';

-- Racial Mount Strings
SET @KulTiranMount1NameenUS                          = 'Kul Tiran Charger';
SET @KulTiranMount1NamekoKR                          = '';
SET @KulTiranMount1NamefrFR                          = '';
SET @KulTiranMount1NamedeDE                          = '';
SET @KulTiranMount1NamezhCN                          = '';
SET @KulTiranMount1NamezhTW                          = '';
SET @KulTiranMount1NameesES                          = '';
SET @KulTiranMount1NameesMX                          = '';
SET @KulTiranMount1NameruRU                          = '';
SET @KulTiranMount1NamejaJP                          = '';
SET @KulTiranMount1NameptPT                          = '';
SET @KulTiranMount1NameitIT                          = '';
SET @KulTiranMount1NameUnk1                          = '';
SET @KulTiranMount1NameUnk2                          = '';
SET @KulTiranMount1NameUnk3                          = '';
SET @KulTiranMount1NameUnk4                          = '';

SET @KulTiranMount1SpellDescriptionenUS              = 'Summons and dismisses a rideable Kul Tiran Charger.';
SET @KulTiranMount1SpellDescriptionkoKR              = '';
SET @KulTiranMount1SpellDescriptionfrFR              = '';
SET @KulTiranMount1SpellDescriptiondeDE              = '';
SET @KulTiranMount1SpellDescriptionzhCN              = '';
SET @KulTiranMount1SpellDescriptionzhTW              = '';
SET @KulTiranMount1SpellDescriptionesES              = '';
SET @KulTiranMount1SpellDescriptionesMX              = '';
SET @KulTiranMount1SpellDescriptionruRU              = '';
SET @KulTiranMount1SpellDescriptionjaJP              = '';
SET @KulTiranMount1SpellDescriptionptPT              = '';
SET @KulTiranMount1SpellDescriptionitIT              = '';
SET @KulTiranMount1SpellDescriptionUnk1              = '';
SET @KulTiranMount1SpellDescriptionUnk2              = '';
SET @KulTiranMount1SpellDescriptionUnk3              = '';
SET @KulTiranMount1SpellDescriptionUnk4              = '';

SET @KulTiranMount1ItemNameenUS                      = @KulTiranMount1NameenUS;
SET @KulTiranMount1ItemDescriptionenUS               = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Kul Tiran Charger.';
