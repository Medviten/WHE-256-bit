-- Race masks (race IDs are fixed in config.sql)
SET @MagharOrcMask                       = 1 << (@MagharOrc - 1);  -- race ID 36 → 34359738368
SET @MagharOrcMask_2                     = IF(@MagharOrc BETWEEN 65 AND 128, 1 << (@MagharOrc - 65), 0); -- races 65-128
SET @MagharOrcHelmetMask                 = 1 << @MagharOrc;  -- race ID 36 → 68719476736

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                           = @HordeMask    |  @MagharOrcMask;
SET @HordeMask_2                         = @HordeMask_2    |  @MagharOrcMask_2; -- races 65-128
SET @BarrensBros                         = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @BarrensBros_2                       = @HordeMask_2    & ~@UndercityMask_2; -- races 65-128
SET @PlayableRaceMask                    = @AllianceMask |  @HordeMask;
SET @PlayableRaceMask_2                  = @AllianceMask_2 |  @HordeMask_2; -- races 65-128
SET @BowHunters                          = @BowHunters   |  @MagharOrcMask;
SET @BowHunters_2                        = @BowHunters_2   |  @MagharOrcMask_2; -- races 65-128
SET @MagharOrcLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MagharOrcAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MagharOrcKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @MagharOrcExplorationSound           = @OrcExplorationSound;
SET @MagharOrcCinematicSequence          = @OrcCinematicSequence;
SET @MagharOrcBlood                      = 1;
SET @MagharOrcMaleModelPath              = 'Character\\Orc\\Male\\OrcMale.mdx';
SET @MagharOrcFemaleModelPath            = 'Character\\Orc\\Female\\OrcFemale.mdx';
SET @MagharOrcMount1ModelPath             = 'Creature\\orcclanworg\\orcclanworg.m2';
SET @MagharOrcMaleFootprint              = @FootprintShoe;
SET @MagharOrcFemaleFootprint            = @FootprintShoe;

-- Mounts (IDs are global, see config.sql)
SET @MagharOrcMount1                         = @SpellMagharDirewolf;
SET @MagharOrcMount1Model                    = @MagharDirewolfModel;
SET @MagharOrcMount1Display                  = @MagharDirewolfDisplay;
SET @MagharOrcMount1CreatureID               = @MagharDirewolfCreatureID;
SET @MagharOrcMount1Item                     = @MagharDirewolfItem;
SET @MagharOrcMount1ItemDisplay              = @MagharDirewolfItemDisplay;
SET @MagharOrcMount1IconID                   = @IconMagharDirewolf;

-- Spells
SET @MagharOrcRacial1                    = @SpellAncestralCall;
SET @MagharOrcRacial2                    = @SpellSavageBlood;
SET @MagharOrcRacial3                    = @SpellSympatheticVigor;
SET @MagharOrcRacial4                    = @SpellOpenSkies;

-- Icons
SET @MagharOrcRacialIcon1                = @IconAncestralCall;
SET @MagharOrcRacialIcon2                = @IconSavageBlood;
SET @MagharOrcRacialIcon3                = @IconSympatheticVigor;
SET @MagharOrcRacialIcon4                = @IconOpenSkies;

-- Icon name
SET @MagharOrcMount1IconName             = 'inv_orcclanworg';
SET @MagharOrcRacialIcon1Name            = 'ability_racial_ancestralcall';
SET @MagharOrcRacialIcon2Name            = 'ability_racial_pureblood';
SET @MagharOrcRacialIcon3Name            = 'ability_racial_sympatheticvigor';
SET @MagharOrcRacialIcon4Name            = 'ability_racial_openskies';

-- Icon paths
SET @MagharOrcMount1IconPath             = 'Interface\\Icons\\inv_orcclanworg';
SET @MagharOrcRacialIcon1Path            = 'Interface\\Icons\\ability_racial_ancestralcall';
SET @MagharOrcRacialIcon2Path            = 'Interface\\Icons\\ability_racial_pureblood';
SET @MagharOrcRacialIcon3Path            = 'Interface\\Icons\\ability_racial_sympatheticvigor';
SET @MagharOrcRacialIcon4Path            = 'Interface\\Icons\\ability_racial_openskies';

-- Strings
SET @MagharOrcClientPrefix               = 'Or';
SET @MagharOrcClientString               = 'Maghar';
SET @MagharOrcFacialHairCustomization1   = 'NORMAL';
SET @MagharOrcFacialHairCustomization2   = 'PIERCINGS';
SET @MagharOrcHairCustomization          = 'NORMAL';

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
SET @MagharOrcUnk1                       = '';
SET @MagharOrcUnk2                       = '';
SET @MagharOrcUnk3                       = '';
SET @MagharOrcUnk4                       = '';

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
SET @MagharOrcFemaleUnk1                 = '';
SET @MagharOrcFemaleUnk2                 = '';
SET @MagharOrcFemaleUnk3                 = '';
SET @MagharOrcFemaleUnk4                 = '';

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
SET @MagharOrcMaleUnk1                   = '';
SET @MagharOrcMaleUnk2                   = '';
SET @MagharOrcMaleUnk3                   = '';
SET @MagharOrcMaleUnk4                   = '';

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
SET @MagharOrcRacialNameUnk1             = '';
SET @MagharOrcRacialNameUnk2             = '';
SET @MagharOrcRacialNameUnk3             = '';
SET @MagharOrcRacialNameUnk4             = '';

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
SET @MagharOrcPlayerUnk1                 = '';
SET @MagharOrcPlayerUnk2                 = '';
SET @MagharOrcPlayerUnk3                 = '';
SET @MagharOrcPlayerUnk4                 = '';

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
SET @MagharOrcFactionNameUnk1            = '';
SET @MagharOrcFactionNameUnk2            = '';
SET @MagharOrcFactionNameUnk3            = '';
SET @MagharOrcFactionNameUnk4            = '';

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
SET @MagharOrcFactionDescriptionUnk1     = '';
SET @MagharOrcFactionDescriptionUnk2     = '';
SET @MagharOrcFactionDescriptionUnk3     = '';
SET @MagharOrcFactionDescriptionUnk4     = '';

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
SET @MagharOrcAchievementUnk1            = '';
SET @MagharOrcAchievementUnk2            = '';
SET @MagharOrcAchievementUnk3            = '';
SET @MagharOrcAchievementUnk4            = '';

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
SET @MagharOrcAchievementDescriptionUnk1 = '';
SET @MagharOrcAchievementDescriptionUnk2 = '';
SET @MagharOrcAchievementDescriptionUnk3 = '';
SET @MagharOrcAchievementDescriptionUnk4 = '';

-- Racial Mount Strings 
SET @MagharOrcMount1NameenUS              = 'Mag\'har Direwolf';
SET @MagharOrcMount1NamekoKR              = '';
SET @MagharOrcMount1NamefrFR              = '';
SET @MagharOrcMount1NamedeDE              = '';
SET @MagharOrcMount1NamezhCN              = '';
SET @MagharOrcMount1NamezhTW              = '';
SET @MagharOrcMount1NameesES              = '';
SET @MagharOrcMount1NameesMX              = '';
SET @MagharOrcMount1NameruRU              = '';
SET @MagharOrcMount1NamejaJP              = '';
SET @MagharOrcMount1NameptPT              = '';
SET @MagharOrcMount1NameitIT              = '';
SET @MagharOrcMount1NameUnk1              = '';
SET @MagharOrcMount1NameUnk2              = '';
SET @MagharOrcMount1NameUnk3              = '';
SET @MagharOrcMount1NameUnk4              = '';

SET @MagharOrcMount1SpellDescriptionenUS  = 'Summons and dismisses a rideable Mag\'har Direwolf.\n\n"Native to Draenor, these wolves are preferred by the Mag\'har for their ferocity, loyalty, and for something to snuggle on those cool winter nights."';
SET @MagharOrcMount1SpellDescriptionkoKR  = '';
SET @MagharOrcMount1SpellDescriptionfrFR  = '';
SET @MagharOrcMount1SpellDescriptiondeDE  = '';
SET @MagharOrcMount1SpellDescriptionzhCN  = '';
SET @MagharOrcMount1SpellDescriptionzhTW  = '';
SET @MagharOrcMount1SpellDescriptionesES  = '';
SET @MagharOrcMount1SpellDescriptionesMX  = '';
SET @MagharOrcMount1SpellDescriptionruRU  = '';
SET @MagharOrcMount1SpellDescriptionjaJP  = '';
SET @MagharOrcMount1SpellDescriptionptPT  = '';
SET @MagharOrcMount1SpellDescriptionitIT  = '';
SET @MagharOrcMount1SpellDescriptionUnk1  = '';
SET @MagharOrcMount1SpellDescriptionUnk2  = '';
SET @MagharOrcMount1SpellDescriptionUnk3  = '';
SET @MagharOrcMount1SpellDescriptionUnk4  = '';

SET @MagharOrcMount1ItemNameenUS          = @MagharOrcMount1NameenUS;
SET @MagharOrcMount1ItemDescriptionenUS   = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Mag\'har Direwolf.\n\n"Native to Draenor, these wolves are preferred by the Mag\'har for their ferocity, loyalty, and for something to snuggle on those cool winter nights."';
