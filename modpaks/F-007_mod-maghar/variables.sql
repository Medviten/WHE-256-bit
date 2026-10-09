-- Race ID
SET @MagharOrc := @NextRace             := @NextRace +1; -- default: 14
SET @MagharOrcMask                       = 1 << (@MagharOrc - 1);  -- race ID 14 → 8192
SET @MagharOrcHelmetMask                 = 1 << @MagharOrc;  -- race ID 14 → 16384

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                           = @HordeMask    |  @MagharOrcMask;
SET @BarrensBros                         = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                    = @AllianceMask |  @HordeMask;
SET @BowHunters                          = @BowHunters   |  @MagharOrcMask;
SET @MagharOrcLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MagharOrcAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MagharOrcKnowThyEnemy               = @KnowThyEnemyHorde;

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
SET @MagharOrcClientString               = 'Maghar';

-- Localization Strings
SET @MagharOrcenUS                       = 'Mag\'har';
SET @MagharOrckoKR                       = '마그하르 오크';
SET @MagharOrcfrFR                       = 'Orc Mag\'har';
SET @MagharOrcdeDE                       = 'Mag\'har-Orc';
SET @MagharOrczhCN                       = '玛格汉兽人';
SET @MagharOrczhTW                       = '瑪格哈獸人';
SET @MagharOrcesES                       = 'Orco Mag\'har';
SET @MagharOrcesMX                       = 'Tábido';
SET @MagharOrcruRU                       = 'Орк Маг\'хар';
SET @MagharOrcjaJP                       = '';
SET @MagharOrcptPT                       = '';
SET @MagharOrcitIT                       = '';

SET @MagharOrcFemaleenUS                 = '';
SET @MagharOrcFemalekoKR                 = '';
SET @MagharOrcFemalefrFR                 = 'Orque Mag\'hare';
SET @MagharOrcFemaledeDE                 = '';
SET @MagharOrcFemalezhCN                 = '';
SET @MagharOrcFemalezhTW                 = '';
SET @MagharOrcFemaleesES                 = 'Orco Mag\'har';
SET @MagharOrcFemaleesMX                 = 'Orco Mag\'har';
SET @MagharOrcFemaleruRU                 = '';
SET @MagharOrcFemalejaJP                 = '';
SET @MagharOrcFemaleptPT                 = '';
SET @MagharOrcFemaleitIT                 = '';

SET @MagharOrcMaleenUS                   = '';
SET @MagharOrcMalekoKR                   = '';
SET @MagharOrcMalefrFR                   = 'Orc Mag\'har';
SET @MagharOrcMaledeDE                   = 'Mag\'har-Orc';
SET @MagharOrcMalezhCN                   = '';
SET @MagharOrcMalezhTW                   = '';
SET @MagharOrcMaleesES                   = 'Orco Mag\'har';
SET @MagharOrcMaleesMX                   = 'Orco Mag\'har';
SET @MagharOrcMaleruRU                   = 'Орк Маг\'хар';
SET @MagharOrcMalejaJP                   = '';
SET @MagharOrcMaleptPT                   = '';
SET @MagharOrcMaleitIT                   = '';

SET @MagharOrcRacialNameenUS             = 'Racial - Mag\'har Orc';
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

SET @MagharOrcFactionNameenUS            = 'Mag\'har of the Horde';
SET @MagharOrcFactionNamekoKR            = '호드의 마가르';
SET @MagharOrcFactionNamefrFR            = 'Mag’har de la Horde';
SET @MagharOrcFactionNamedeDE            = 'Mag\'har der Horde';
SET @MagharOrcFactionNamezhCN            = '部落玛格汉';
SET @MagharOrcFactionNamezhTW            = '部落瑪格哈';
SET @MagharOrcFactionNameesES            = 'Mag\'har de la Horda';
SET @MagharOrcFactionNameesMX            = 'Mag\'har de la Horda';
SET @MagharOrcFactionNameruRU            = 'Магхары Орды';
SET @MagharOrcFactionNamejaJP            = '';
SET @MagharOrcFactionNameptPT            = '';
SET @MagharOrcFactionNameitIT            = '';

SET @MagharOrcFactionDescriptionenUS     = 'Horde-aligned Mag\'har orcs.';
SET @MagharOrcFactionDescriptionkoKR     = '호드에 합류한 마가르 오크입니다.';
SET @MagharOrcFactionDescriptionfrFR     = 'Orcs mag’har alliés à la Horde.';
SET @MagharOrcFactionDescriptiondeDE     = 'Mag\'har-Orcs, die sich der Horde angeschlossen haben.';
SET @MagharOrcFactionDescriptionzhCN     = '加入部落的玛格汉兽人。';
SET @MagharOrcFactionDescriptionzhTW     = '加入部落的瑪格哈獸人。';
SET @MagharOrcFactionDescriptionesES     = 'Orcos Mag\'har aliados con la Horda.';
SET @MagharOrcFactionDescriptionesMX     = 'Orcos Mag\'har aliados con la Horda.';
SET @MagharOrcFactionDescriptionruRU     = 'Орки-магхары, присоединившиеся к Орде.';
SET @MagharOrcFactionDescriptionjaJP     = '';
SET @MagharOrcFactionDescriptionptPT     = '';
SET @MagharOrcFactionDescriptionitIT     = '';

SET @MagharOrcAchievementenUS            = 'Realm First! Level 80 Mag\'har';
SET @MagharOrcAchievementkoKR            = '서버 최초 80 레벨 마그하르 오크';
SET @MagharOrcAchievementfrFR            = 'Orc Mag\'har « Prem\'s » au niveau 80 sur le royaume';
SET @MagharOrcAchievementdeDE            = 'Erster Stufe-80-Mag\'har-Orc des Realms!';
SET @MagharOrcAchievementzhCN            = '服务器第一！80级玛格汉兽人';
SET @MagharOrcAchievementzhTW            = '伺服器首位!80級瑪格哈獸人';
SET @MagharOrcAchievementesES            = '¡Primero del reino! Orco Mag\'har nivel 80';
SET @MagharOrcAchievementesMX            = '¡Primero del reino! Orco Mag\'har nivel 80';
SET @MagharOrcAchievementruRU            = '1-й на сервере! Орк Маг\'хар 80-го уровня';
SET @MagharOrcAchievementjaJP            = '';
SET @MagharOrcAchievementptPT            = '';
SET @MagharOrcAchievementitIT            = '';

SET @MagharOrcAchievementDescriptionenUS = 'First mag\'har orc on the realm to achieve level 80.';
SET @MagharOrcAchievementDescriptionkoKR = '서버 최초로 80 레벨 마그하르 오크 달성';
SET @MagharOrcAchievementDescriptionfrFR = 'Premier orc Mag\'har du royaume à atteindre le niveau 80.';
SET @MagharOrcAchievementDescriptiondeDE = 'Erster Mag\'har-Orc des Realms, der Stufe 80 erreicht hat.';
SET @MagharOrcAchievementDescriptionzhCN = '本服务器第一个达到80级的玛格汉兽人。';
SET @MagharOrcAchievementDescriptionzhTW = '伺服器首位達到80級的瑪格哈獸人。';
SET @MagharOrcAchievementDescriptionesES = 'Primer orco Mag\'har del reino en alcanzar el nivel 80.';
SET @MagharOrcAchievementDescriptionesMX = 'Primer orco Mag\'har del reino en alcanzar el nivel 80.';
SET @MagharOrcAchievementDescriptionruRU = 'Первый орк Маг\'хар на сервере, достигший 80-го уровня.';
SET @MagharOrcAchievementDescriptionjaJP = '';
SET @MagharOrcAchievementDescriptionptPT = '';
SET @MagharOrcAchievementDescriptionitIT = '';
