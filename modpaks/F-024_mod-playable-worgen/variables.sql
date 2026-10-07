-- Race ID
SET @Worgen                          := 12;
SET @WorgenMask                       = 1 << (@Worgen - 1); -- default: 2048
SET @WorgenHelmetMask                 = 1 << @Worgen; -- default: 4096

-- Important variable update
SET @AllianceMask                     = @AllianceMask     | @WorgenMask;
SET @PlayableRaceMask                 = @PlayableRaceMask | @WorgenMask;
SET @GunHunters                       = @GunHunters       | @WorgenMask;

-- Miscellaneous
SET @WorgenExplorationSound           = @TaurenExplorationSound;
SET @WorgenCinematicSequence          = @NightElfCinematicSequence;
SET @WorgenBlood                      = 1;
SET @WorgenWildBlood                  = @WorgenBlood;
SET @WorgenMaleModelPath              = 'Character\\Worgen\\Male\\WorgenMale.mdx';
SET @WorgenFemaleModelPath            = 'Character\\Worgen\\Female\\WorgenFemale.mdx';
SET @WorgenWildMaleModelPath          = 'Character\\\\WorgenWild\\\\Male\\\\WorgenWildMale.mdx';
SET @WorgenWildFemaleModelPath        = 'Character\\\\WorgenWild\\\\Female\\\\WorgenWildFemale.mdx';
SET @WorgenMaleFootprint              = @FootprintPaw;
SET @WorgenFemaleFootprint            = @FootprintPaw;
SET @WorgenWildMaleFootprint          = @WorgenMaleFootprint;
SET @WorgenWildFemaleFootprint        = @WorgenFemaleFootprint;

-- Strings
SET @WorgenClientPrefix               = 'Wo';
SET @WorgenClientString               = 'Worgen';

-- Localization Strings
SET @WorgenenUS                       = 'Worgen';
SET @WorgenkoKR                       = '늑대인간';
SET @WorgenfrFR                       = 'Worgen';
SET @WorgendeDE                       = 'Worgen';
SET @WorgenzhCN                       = '狼人';
SET @WorgenzhTW                       = '';
SET @WorgenesES                       = 'Huargen';
SET @WorgenesMX                       = 'Huargen';
SET @WorgenruRU                       = 'Ворген';
SET @WorgenjaJP                       = '';
SET @WorgenptPT                       = '';
SET @WorgenitIT                       = '';

SET @WorgenFemaleenUS                 = '';
SET @WorgenFemalekoKR                 = '';
SET @WorgenFemalefrFR                 = 'Worgen';
SET @WorgenFemaledeDE                 = '';
SET @WorgenFemalezhCN                 = '';
SET @WorgenFemalezhTW                 = '';
SET @WorgenFemaleesES                 = 'Huargen';
SET @WorgenFemaleesMX                 = 'Huargen';
SET @WorgenFemaleruRU                 = '';
SET @WorgenFemalejaJP                 = '';
SET @WorgenFemaleptPT                 = '';
SET @WorgenFemaleitIT                 = '';

SET @WorgenMaleenUS                   = '';
SET @WorgenMalekoKR                   = '';
SET @WorgenMalefrFR                   = 'Worgen';
SET @WorgenMaledeDE                   = 'Worgen';
SET @WorgenMalezhCN                   = '';
SET @WorgenMalezhTW                   = '';
SET @WorgenMaleesES                   = 'Huargen';
SET @WorgenMaleesMX                   = 'Huargen';
SET @WorgenMaleruRU                   = 'Ворген';
SET @WorgenMalejaJP                   = '';
SET @WorgenMaleptPT                   = '';
SET @WorgenMaleitIT                   = '';

SET @WorgenRacialNameenUS             = 'Racial - Worgen';
SET @WorgenRacialNamekoKR             = '늑대인간 종족 특성';
SET @WorgenRacialNamefrFR             = 'Raciale worgen';
SET @WorgenRacialNamedeDE             = 'Worgenvolk';
SET @WorgenRacialNamezhCN             = '狼人种族特长';
SET @WorgenRacialNamezhTW             = '';
SET @WorgenRacialNameesES             = 'Racial huargen';
SET @WorgenRacialNameesMX             = 'Racial huargen';
SET @WorgenRacialNameruRU             = '';
SET @WorgenRacialNamejaJP             = '';
SET @WorgenRacialNameptPT             = '';
SET @WorgenRacialNameitIT             = '';

SET @WorgenPlayerenUS                 = '"PLAYER", " Worgen"';
SET @WorgenPlayerkoKR                 = '플레이어 - 늑대인간';
SET @WorgenPlayerfrFR                 = '"JOUEUR"," Worgen"';
SET @WorgenPlayerdeDE                 = '"SPIELER"," Worgen"';
SET @WorgenPlayerzhCN                 = '狼人(玩家)';
SET @WorgenPlayerzhTW                 = '';
SET @WorgenPlayeresES                 = '"JUGADOR"," Huargen"';
SET @WorgenPlayeresMX                 = '"JUGADOR"," Huargen"';
SET @WorgenPlayerruRU                 = 'ИГРОК: ворген';
SET @WorgenPlayerjaJP                 = '';
SET @WorgenPlayerptPT                 = '';
SET @WorgenPlayeritIT                 = '';

SET @WorgenFactionNameenUS            = 'Gilneas';
SET @WorgenFactionNamekoKR            = '길니아스';
SET @WorgenFactionNamefrFR            = 'Gilnéas';
SET @WorgenFactionNamedeDE            = 'Gilneas';
SET @WorgenFactionNamezhCN            = '吉尔尼斯';
SET @WorgenFactionNamezhTW            = '吉爾尼斯';
SET @WorgenFactionNameesES            = 'Gilneas';
SET @WorgenFactionNameesMX            = 'Gilneas';
SET @WorgenFactionNameruRU            = 'Гилнеас';
SET @WorgenFactionNamejaJP            = '';
SET @WorgenFactionNameptPT            = '';
SET @WorgenFactionNameitIT            = '';

SET @WorgenFactionDescriptionenUS     = 'The kingdom of Gilneas.';
SET @WorgenFactionDescriptionkoKR     = '길니아스 왕국입니다.';
SET @WorgenFactionDescriptionfrFR     = 'Le royaume de Gilnéas.';
SET @WorgenFactionDescriptiondeDE     = 'Das Königreich Gilneas.';
SET @WorgenFactionDescriptionzhCN     = '吉尔尼斯王国。';
SET @WorgenFactionDescriptionzhTW     = '吉爾尼斯王國。';
SET @WorgenFactionDescriptionesES     = 'El reino de Gilneas.';
SET @WorgenFactionDescriptionesMX     = 'El reino de Gilneas.';
SET @WorgenFactionDescriptionruRU     = 'Королевство Гилнеас.';
SET @WorgenFactionDescriptionjaJP     = '';
SET @WorgenFactionDescriptionptPT     = '';
SET @WorgenFactionDescriptionitIT     = '';

SET @WorgenAchievementenUS            = 'Realm First! Level 80 Worgen';
SET @WorgenAchievementkoKR            = '서버 최초 80 레벨 늑대인간';
SET @WorgenAchievementfrFR            = 'Worgen  « Prem\'s » au niveau 80 sur le royaume';
SET @WorgenAchievementdeDE            = 'Erster Stufe-80-Worgen des Realms!';
SET @WorgenAchievementzhCN            = '服务器第一！80级狼人';
SET @WorgenAchievementzhTW            = '';
SET @WorgenAchievementesES            = '¡Primero del reino! Worgen nivel 80';
SET @WorgenAchievementesMX            = '¡Primero del reino! Worgen nivel 80';
SET @WorgenAchievementruRU            = '1-й на сервере! Ворген 80-го уровня';
SET @WorgenAchievementjaJP            = '';
SET @WorgenAchievementptPT            = '';
SET @WorgenAchievementitIT            = '';

SET @WorgenAchievementDescriptionenUS = 'First worgen on the realm to achieve level 80.';
SET @WorgenAchievementDescriptionkoKR = '서버 최초로 80 레벨 늑대인간 달성';
SET @WorgenAchievementDescriptionfrFR = 'Premier worgen du royaume à atteindre le niveau 80.';
SET @WorgenAchievementDescriptiondeDE = 'Erster Worgen des Realms, der Stufe 80 erreicht hat.';
SET @WorgenAchievementDescriptionzhCN = '本服务器第一个达到80级的狼人。';
SET @WorgenAchievementDescriptionzhTW = '';
SET @WorgenAchievementDescriptionesES = 'Primer huargen del reino en alcanzar el nivel 80.';
SET @WorgenAchievementDescriptionesMX = 'Primer huargen del reino en alcanzar el nivel 80.';
SET @WorgenAchievementDescriptionruRU = 'Первый ворген на сервере, достигший 80-го уровня.';
SET @WorgenAchievementDescriptionjaJP = '';
SET @WorgenAchievementDescriptionptPT = '';
SET @WorgenAchievementDescriptionitIT = '';
