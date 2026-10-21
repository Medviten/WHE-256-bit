-- Race masks (race IDs are fixed in config.sql)
SET @GoblinMask                       = 1 << (@Goblin - 1); -- race ID 9 → 256
SET @GoblinMask_2                     = IF(@Goblin BETWEEN 65 AND 128, 1 << (@Goblin - 65), 0); -- races 65-128
SET @GoblinHelmetMask                 = 1 << @Goblin;       -- race ID 9 → 512

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                        = @HordeMask    | @GoblinMask;
SET @HordeMask_2                      = @HordeMask_2    | @GoblinMask_2; -- races 65-128
SET @BarrensBros                      = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @BarrensBros_2                    = @HordeMask_2    & ~@UndercityMask_2; -- races 65-128
SET @PlayableRaceMask                 = @AllianceMask | @HordeMask;
SET @PlayableRaceMask_2               = @AllianceMask_2 | @HordeMask_2; -- races 65-128
SET @GunHunters                       = @GunHunters   | @GoblinMask;
SET @GunHunters_2                     = @GunHunters_2   | @GoblinMask_2; -- races 65-128
SET @GoblinLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @GoblinAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @GoblinKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @GoblinExplorationSound           = @OrcExplorationSound;
SET @GoblinCinematicSequence          = @OrcCinematicSequence;
SET @GoblinBlood                      = 1;
SET @GoblinMaleModelPath              = 'Character\\GoblinPC\\Male\\GoblinPCMale.mdx';
SET @GoblinFemaleModelPath            = 'Character\\GoblinPC\\Female\\GoblinPCFemale.mdx';
SET @GoblinMaleFootprint              = @FootprintShoe;
SET @GoblinFemaleFootprint            = @FootprintShoe;
SET @GobberCreatureID                                          =    36613; -- Cataclysm ID

-- Mounts (IDs are global, see config.sql)
SET @GoblinMount1                            = @SpellGoblinTrike;
SET @GoblinMount1Model                       = @GoblinTrikeModel;
SET @GoblinMount1Display                     = @GoblinTrikeDisplay;
SET @GoblinMount1CreatureID                  = @GoblinTrikeCreatureID;
SET @GoblinMount1Item                        = @GoblinTrikeItem;
SET @GoblinMount1ItemDisplay                 = @GoblinTrikeItemDisplay;

SET @GoblinMount2                            = @SpellGoblinTurboTrike;
SET @GoblinMount2Model                       = @GoblinTurboTrikeModel;
SET @GoblinMount2Display                     = @GoblinTurboTrikeDisplay;
SET @GoblinMount2CreatureID                  = @GoblinTurboTrikeCreatureID;
SET @GoblinMount2Item                        = @GoblinTurboTrikeItem;
SET @GoblinMount2ItemDisplay                 = @GoblinTurboTrikeItemDisplay;

-- Strings
SET @GoblinClientPrefix               = 'Go';
SET @GoblinClientString               = 'Goblin';
SET @GoblinFacialHairCustomization1   = 'PIERCINGS';
SET @GoblinFacialHairCustomization2   = 'PIERCINGS';
SET @GoblinHairCustomization          = 'NORMAL';

-- Localization Strings
SET @GoblinenUS                       = 'Goblin';
SET @GoblinkoKR                       = '고블린';
SET @GoblinfrFR                       = 'Gobelin';
SET @GoblindeDE                       = 'Goblin';
SET @GoblinzhCN                       = '地精';
SET @GoblinzhTW                       = '哥布林';
SET @GoblinesES                       = 'Goblin';
SET @GoblinesMX                       = 'Goblin';
SET @GoblinruRU                       = 'Гоблин';
SET @GoblinjaJP                       = '';
SET @GoblinptPT                       = '';
SET @GoblinitIT                       = '';
SET @GoblinUnk1                       = '';
SET @GoblinUnk2                       = '';
SET @GoblinUnk3                       = '';
SET @GoblinUnk4                       = '';

SET @GoblinFemaleenUS                 = '';
SET @GoblinFemalekoKR                 = '';
SET @GoblinFemalefrFR                 = 'Gobeline';
SET @GoblinFemaledeDE                 = '';
SET @GoblinFemalezhCN                 = '';
SET @GoblinFemalezhTW                 = '';
SET @GoblinFemaleesES                 = 'Goblin';
SET @GoblinFemaleesMX                 = 'Goblin';
SET @GoblinFemaleruRU                 = '';
SET @GoblinFemalejaJP                 = '';
SET @GoblinFemaleptPT                 = '';
SET @GoblinFemaleitIT                 = '';
SET @GoblinFemaleUnk1                 = '';
SET @GoblinFemaleUnk2                 = '';
SET @GoblinFemaleUnk3                 = '';
SET @GoblinFemaleUnk4                 = '';

SET @GoblinMaleenUS                   = '';
SET @GoblinMalekoKR                   = '';
SET @GoblinMalefrFR                   = 'Gobelin';
SET @GoblinMaledeDE                   = 'Goblin';
SET @GoblinMalezhCN                   = '';
SET @GoblinMalezhTW                   = '';
SET @GoblinMaleesES                   = 'Goblin';
SET @GoblinMaleesMX                   = 'Goblin';
SET @GoblinMaleruRU                   = 'Гоблин';
SET @GoblinMalejaJP                   = '';
SET @GoblinMaleptPT                   = '';
SET @GoblinMaleitIT                   = '';
SET @GoblinMaleUnk1                   = '';
SET @GoblinMaleUnk2                   = '';
SET @GoblinMaleUnk3                   = '';
SET @GoblinMaleUnk4                   = '';

SET @GoblinRacialNameenUS             = 'Racial - Goblin';
SET @GoblinRacialNamekoKR             = '고블린 종족 특성';
SET @GoblinRacialNamefrFR             = 'Raciale gobelin';
SET @GoblinRacialNamedeDE             = 'Goblinvolk';
SET @GoblinRacialNamezhCN             = '地精种族特长';
SET @GoblinRacialNamezhTW             = '哥布林種族特長';
SET @GoblinRacialNameesES             = 'Racial goblin';
SET @GoblinRacialNameesMX             = 'Racial goblin';
SET @GoblinRacialNameruRU             = 'Расовый навык гоблинов';
SET @GoblinRacialNamejaJP             = '';
SET @GoblinRacialNameptPT             = '';
SET @GoblinRacialNameitIT             = '';
SET @GoblinRacialNameUnk1             = '';
SET @GoblinRacialNameUnk2             = '';
SET @GoblinRacialNameUnk3             = '';
SET @GoblinRacialNameUnk4             = '';

SET @GoblinPlayerenUS                 = '"PLAYER"," Goblin"';
SET @GoblinPlayerkoKR                 = '플레이어 - 고블린';
SET @GoblinPlayerfrFR                 = '"JOUEUR"," Gobelin"';
SET @GoblinPlayerdeDE                 = '"SPIELER"," Goblin"';
SET @GoblinPlayerzhCN                 = '地精(玩家)';
SET @GoblinPlayerzhTW                 = '';
SET @GoblinPlayeresES                 = '"JUGADOR"," goblin"';
SET @GoblinPlayeresMX                 = '"JUGADOR"," goblin"';
SET @GoblinPlayerruRU                 = 'ИГРОК: гоблин';
SET @GoblinPlayerjaJP                 = '';
SET @GoblinPlayerptPT                 = '';
SET @GoblinPlayeritIT                 = '';
SET @GoblinPlayerUnk1                 = '';
SET @GoblinPlayerUnk2                 = '';
SET @GoblinPlayerUnk3                 = '';
SET @GoblinPlayerUnk4                 = '';

SET @GoblinFactionNameenUS            = 'Bilgewater Cartel';
SET @GoblinFactionNamekoKR            = '빌지워터 무역회사';
SET @GoblinFactionNamefrFR            = 'Cartel Baille-Fonds';
SET @GoblinFactionNamedeDE            = 'Bilgewasserkartell';
SET @GoblinFactionNamezhCN            = '锈水财阀';
SET @GoblinFactionNamezhTW            = '污水企業';
SET @GoblinFactionNameesES            = 'Cártel Pantoque';
SET @GoblinFactionNameesMX            = 'Cártel Pantoque';
SET @GoblinFactionNameruRU            = 'Торговая компания Трюмных Вод';
SET @GoblinFactionNamejaJP            = '';
SET @GoblinFactionNameptPT            = '';
SET @GoblinFactionNameitIT            = '';
SET @GoblinFactionNameUnk1            = '';
SET @GoblinFactionNameUnk2            = '';
SET @GoblinFactionNameUnk3            = '';
SET @GoblinFactionNameUnk4            = '';

SET @GoblinFactionDescriptionenUS     = 'Goblins sworn to the Horde.';
SET @GoblinFactionDescriptionkoKR     = '호드에 충성을 맹세한 고블린들입니다.';
SET @GoblinFactionDescriptionfrFR     = 'Des gobelins ayant juré fidélité à la Horde.';
SET @GoblinFactionDescriptiondeDE     = 'Goblins, die der Horde die Treue geschworen haben.';
SET @GoblinFactionDescriptionzhCN     = '效忠于部落的地精。';
SET @GoblinFactionDescriptionzhTW     = '效忠部落的哥布林。';
SET @GoblinFactionDescriptionesES     = 'Goblins que juraron lealtad a la Horda.';
SET @GoblinFactionDescriptionesMX     = 'Goblins que juraron lealtad a la Horda.';
SET @GoblinFactionDescriptionruRU     = 'Гоблины, присягнувшие Орде.';
SET @GoblinFactionDescriptionjaJP     = '';
SET @GoblinFactionDescriptionptPT     = '';
SET @GoblinFactionDescriptionitIT     = '';
SET @GoblinFactionDescriptionUnk1     = '';
SET @GoblinFactionDescriptionUnk2     = '';
SET @GoblinFactionDescriptionUnk3     = '';
SET @GoblinFactionDescriptionUnk4     = '';

SET @GoblinAchievementenUS            = 'Realm First! Level 80 Goblin';
SET @GoblinAchievementkoKR            = '서버 최초 80 레벨 고블린';
SET @GoblinAchievementfrFR            = 'Gobelin « Prem\'s » au niveau 80 sur le royaume';
SET @GoblinAchievementdeDE            = 'Erster Stufe-80-Goblin des Realms!';
SET @GoblinAchievementzhCN            = '服务器第一！80级地精';
SET @GoblinAchievementzhTW            = '伺服器首位!80級哥布林';
SET @GoblinAchievementesES            = '¡Primero del reino! Goblin nivel 80';
SET @GoblinAchievementesMX            = '¡Primero del reino! Goblin nivel 80';
SET @GoblinAchievementruRU            = '1-й на сервере! Гоблин 80-го уровня';
SET @GoblinAchievementjaJP            = '';
SET @GoblinAchievementptPT            = '';
SET @GoblinAchievementitIT            = '';
SET @GoblinAchievementUnk1            = '';
SET @GoblinAchievementUnk2            = '';
SET @GoblinAchievementUnk3            = '';
SET @GoblinAchievementUnk4            = '';

SET @GoblinAchievementDescriptionenUS = 'Realm First! Level 80 Goblin';
SET @GoblinAchievementDescriptionkoKR = '서버 최초 80 레벨 고블린';
SET @GoblinAchievementDescriptionfrFR = 'Gobelin « Prem\'s » au niveau 80 sur le royaume';
SET @GoblinAchievementDescriptiondeDE = 'Erster Stufe-80-Goblin des Realms!';
SET @GoblinAchievementDescriptionzhCN = '服务器第一！80级地精';
SET @GoblinAchievementDescriptionzhTW = '伺服器首位!80級哥布林';
SET @GoblinAchievementDescriptionesES = '¡Primero del reino! Goblin nivel 80';
SET @GoblinAchievementDescriptionesMX = '¡Primero del reino! Goblin nivel 80';
SET @GoblinAchievementDescriptionruRU = '1-й на сервере! Гоблин 80-го уровня';
SET @GoblinAchievementDescriptionjaJP = '';
SET @GoblinAchievementDescriptionptPT = '';
SET @GoblinAchievementDescriptionitIT = '';
SET @GoblinAchievementDescriptionUnk1 = '';
SET @GoblinAchievementDescriptionUnk2 = '';
SET @GoblinAchievementDescriptionUnk3 = '';
SET @GoblinAchievementDescriptionUnk4 = '';
