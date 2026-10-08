-- Race ID
SET @HighElf                          := @NextRace := @NextRace +1; -- default: 13
SET @HighElfMask                       = 1 << (@HighElf - 1);    -- race ID 13 → 4096
SET @HighElfHelmetMask                 = 1 << @HighElf;    -- race ID 13 → 8192

-- Important variable update
SET @AllianceMask                      = @AllianceMask | @HighElfMask;
SET @PlayableRaceMask                  = @AllianceMask | @HordeMask;
SET @BowHunters                        = @BowHunters   | @HighElf;
SET @HighElfLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @HighElfAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @HighElfExplorationSound           = @HumanExplorationSound;
SET @HighElfCinematicSequence          = @HumanCinematicSequence;
SET @HighElfBlood                      = 1;
SET @HighElfMaleModelPath              = 'Character\\HighElf\\Male\\HighElfMale.mdx';
SET @HighElfFemaleModelPath            = 'Character\\HighElf\\Female\\HighElfFemale.mdx';
SET @HighElfMaleFootprint              = @FootprintShoe;
SET @HighElfFemaleFootprint            = @FootprintShoe;

-- Strings
SET @HighElfClientPrefix               = 'Be';
SET @HighElfClientString               = 'HighElf';

-- Localization Strings
SET @HighElfenUS                       = 'High Elf';
SET @HighElfkoKR                       = '하이 엘프';
SET @HighElffrFR                       = 'Haut-elfe';
SET @HighElfdeDE                       = 'Hochelf';
SET @HighElfzhCN                       = '高等精灵';
SET @HighElfzhTW                       = '高等精靈';
SET @HighElfesES                       = 'Alto elfo';
SET @HighElfesMX                       = 'Alto elfo';
SET @HighElfruRU                       = 'Высший эльф';
SET @HighElfjaJP                       = '';
SET @HighElfptPT                       = '';
SET @HighElfitIT                       = '';

SET @HighElfFemaleenUS                 = '';
SET @HighElfFemalekoKR                 = '';
SET @HighElfFemalefrFR                 = '';
SET @HighElfFemaledeDE                 = '';
SET @HighElfFemalezhCN                 = '';
SET @HighElfFemalezhTW                 = '';
SET @HighElfFemaleesES                 = '';
SET @HighElfFemaleesMX                 = '';
SET @HighElfFemaleruRU                 = '';
SET @HighElfFemalejaJP                 = '';
SET @HighElfFemaleptPT                 = '';
SET @HighElfFemaleitIT                 = '';

SET @HighElfMaleenUS                   = '';
SET @HighElfMalekoKR                   = '';
SET @HighElfMalefrFR                   = '';
SET @HighElfMaledeDE                   = '';
SET @HighElfMalezhCN                   = '';
SET @HighElfMalezhTW                   = '';
SET @HighElfMaleesES                   = '';
SET @HighElfMaleesMX                   = '';
SET @HighElfMaleruRU                   = '';
SET @HighElfMalejaJP                   = '';
SET @HighElfMaleptPT                   = '';
SET @HighElfMaleitIT                   = '';

SET @HighElfRacialNameenUS             = 'Racial - High Elf';
SET @HighElfRacialNamekoKR             = '하이 엘프 종족 특성';
SET @HighElfRacialNamefrFR             = 'Raciale haut-elfe';
SET @HighElfRacialNamedeDE             = 'Hochelfenvolk';
SET @HighElfRacialNamezhCN             = '高等精灵种族特长';
SET @HighElfRacialNamezhTW             = '種族特長 - 高等精靈';
SET @HighElfRacialNameesES             = 'Racial alto elfo';
SET @HighElfRacialNameesMX             = 'Racial alto elfo';
SET @HighElfRacialNameruRU             = '';
SET @HighElfRacialNamejaJP             = '';
SET @HighElfRacialNameptPT             = '';
SET @HighElfRacialNameitIT             = '';

SET @HighElfPlayerenUS                 = '"PLAYER"," High Elf"';
SET @HighElfPlayerkoKR                 = '플레이어 - 하이 엘프';
SET @HighElfPlayerfrFR                 = '"JOUEUR"," Haut-elfe"';
SET @HighElfPlayerdeDE                 = '"SPIELER"," Hochelf"';
SET @HighElfPlayerzhCN                 = '高等精灵(玩家)';
SET @HighElfPlayerzhTW                 = '高等精靈(玩家)';
SET @HighElfPlayeresES                 = '"JUGADOR"," alto elfo"';
SET @HighElfPlayeresMX                 = '"JUGADOR"," alto elfo"';
SET @HighElfPlayerruRU                 = 'ИГРОК: высший эльф';
SET @HighElfPlayerjaJP                 = '';
SET @HighElfPlayerptPT                 = '';
SET @HighElfPlayeritIT                 = '';

SET @HighElfFactionNameenUS            = 'High Elven Loyalists';
SET @HighElfFactionNamekoKR            = '하이 엘프 충성파';
SET @HighElfFactionNamefrFR            = 'Loyalistes hauts-elfes';
SET @HighElfFactionNamedeDE            = 'Hochelfen-Loyalisten';
SET @HighElfFactionNamezhCN            = '高等精灵效忠者';
SET @HighElfFactionNamezhTW            = '高等精靈效忠者';
SET @HighElfFactionNameesES            = 'Leales altos elfos';
SET @HighElfFactionNameesMX            = 'Leales altos elfos';
SET @HighElfFactionNameruRU            = 'Верные высшие эльфы';
SET @HighElfFactionNamejaJP            = '';
SET @HighElfFactionNameptPT            = '';
SET @HighElfFactionNameitIT            = '';

SET @HighElfFactionDescriptionenUS     = 'High elves who remained loyal to the Alliance.';
SET @HighElfFactionDescriptionkoKR     = '얼라이언스에 충성을 지킨 하이 엘프들.';
SET @HighElfFactionDescriptionfrFR     = 'Hauts-elfes restés fidèles à l’Alliance.';
SET @HighElfFactionDescriptiondeDE     = 'Hochelfen, die der Allianz treu geblieben sind.';
SET @HighElfFactionDescriptionzhCN     = '仍效忠联盟的高等精灵。';
SET @HighElfFactionDescriptionzhTW     = '仍效忠聯盟的高等精靈。';
SET @HighElfFactionDescriptionesES     = 'Altos elfos que permanecieron leales a la Alianza.';
SET @HighElfFactionDescriptionesMX     = 'Altos elfos que permanecieron leales a la Alianza.';
SET @HighElfFactionDescriptionruRU     = 'Высшие эльфы, сохранившие верность Альянсу.';
SET @HighElfFactionDescriptionjaJP     = '';
SET @HighElfFactionDescriptionptPT     = '';
SET @HighElfFactionDescriptionitIT     = '';

SET @HighElfAchievementenUS            = 'Realm First! Level 80 High Elf',
SET @HighElfAchievementkoKR            = '서버 최초 80 레벨 하이 엘프',
SET @HighElfAchievementfrFR            = 'Haut-elfe « Prem\'s » au niveau 80 sur le royaume',
SET @HighElfAchievementdeDE            = 'Erster Stufe-80-Hochelf des Realms!',
SET @HighElfAchievementzhCN            = '服务器第一！80级高等精灵',
SET @HighElfAchievementzhTW            = '伺服器首位!80級高等精靈',
SET @HighElfAchievementesES            = '¡Primero del reino! Alto elfo nivel 80',
SET @HighElfAchievementesMX            = '¡Primero del reino! Alto elfo nivel 80',
SET @HighElfAchievementruRU            = '1-й на сервере! Высший эльф 80 уровня',
SET @HighElfAchievementjaJP            = '';
SET @HighElfAchievementptPT            = '';
SET @HighElfAchievementitIT            = '';

SET @HighElfAchievementDescriptionenUS = 'First high elf on the realm to achieve level 80.',
SET @HighElfAchievementDescriptionkoKR = '서버 최초로 80 레벨 하이 엘프 달성',
SET @HighElfAchievementDescriptionfrFR = 'Premier haut-elfe du royaume à atteindre le niveau 80.',
SET @HighElfAchievementDescriptiondeDE = 'Erster Hochelf des Realms, der Stufe 80 erreicht hat.',
SET @HighElfAchievementDescriptionzhCN = '本服务器第一个达到80级的高等精灵。',
SET @HighElfAchievementDescriptionzhTW = '伺服器首位達到80級的高等精靈。',
SET @HighElfAchievementDescriptionesES = 'Primer alto elfo del reino en alcanzar el nivel 80.',
SET @HighElfAchievementDescriptionesMX = 'Primer alto elfo del reino en alcanzar el nivel 80.',
SET @HighElfAchievementDescriptionruRU = 'Первый высший эльф на сервере, достигший 80-го уровня.',
SET @HighElfAchievementDescriptionjaJP = '';
SET @HighElfAchievementDescriptionptPT = '';
SET @HighElfAchievementDescriptionitIT = '';
