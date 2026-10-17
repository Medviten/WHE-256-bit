-- Race ID
SET @DarkIronDwarf                          := @NextRace := @NextRace +1;    -- default: 16
SET @DarkIronDwarfMask                       = 1 << (@DarkIronDwarf - 1); -- race ID 16 → 32768
SET @DarkIronDwarfHelmetMask                 = 1 << @DarkIronDwarf; -- race ID 16 → 65536

-- Important variable updates (Alliance vs. Horde)
SET @AllianceMask                            = @AllianceMask | @DarkIronDwarfMask;
SET @BarrensBros                             = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                        = @AllianceMask | @HordeMask;
SET @GunHunters                              = @GunHunters   | @DarkIronDwarfMask;
SET @DarkIronDwarfLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @DarkIronDwarfAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @DarkIronDwarfKnowThyEnemy               = @KnowThyEnemyAlliance;

-- Miscellaneous
SET @DarkIronDwarfExplorationSound           = @DwarfExplorationSound;
SET @DarkIronDwarfCinematicSequence          = @DwarfCinematicSequence;
SET @DarkIronDwarfBlood                      = 1;
SET @DarkIronDwarfMaleModelPath              = 'Character\\Darkirondwarf\\male\\darkirondwarfMale.M2';
SET @DarkIronDwarfFemaleModelPath            = 'Character\\Darkirondwarf\\female\\darkirondwarfFemale.M2';
SET @DarkIronDwarfMaleFootprint              = @FootprintShoe;
SET @DarkIronDwarfFemaleFootprint            = @FootprintShoe;

-- Mounts (IDs are global, see config.sql)
SET @DarkIronDwarfMount1                     = @SpellDarkIronCoreHound;
SET @DarkIronDwarfMount1Model                = @DarkIronCoreHoundModel;
SET @DarkIronDwarfMount1Display              = @DarkIronCoreHoundDisplay;
SET @DarkIronDwarfMount1CreatureID           = @DarkIronCoreHoundCreatureID;
SET @DarkIronDwarfMount1Item                 = @DarkIronCoreHoundItem;
SET @DarkIronDwarfMount1ItemDisplay          = @DarkIronCoreHoundItemDisplay;
SET @DarkIronDwarfMount1IconID               = @IconDarkIronCoreHound;
SET @DarkIronDwarfMount1IconName             = 'ability_hunter_pet_corehound';
SET @DarkIronDwarfMount1IconPath             = CONCAT('Interface\\Icons\\', @DarkIronDwarfMount1IconName);
SET @DarkIronDwarfMount1ModelPath            = 'Creature\\darkirondwarfcorehound\\darkirondwarfcorehound.m2';

-- Strings
SET @DarkIronDwarfClientPrefix               = 'Dw';
SET @DarkIronDwarfClientString               = 'DarkIronDwarf';
SET @DarkIronDwarfFacialHairCustomization1   = 'NORMAL';
SET @DarkIronDwarfFacialHairCustomization2   = 'PIERCINGS';
SET @DarkIronDwarfHairCustomization          = 'NORMAL';

-- Localization Strings
SET @DarkIronDwarfenUS                       = 'Dark Iron Dwarf';
SET @DarkIronDwarfkoKR                       = '검은무쇠 드워프';
SET @DarkIronDwarffrFR                       = 'Nain Sombrefer';
SET @DarkIronDwarfdeDE                       = 'Dunkeleisenzwerg';
SET @DarkIronDwarfzhCN                       = '黑铁矮人';
SET @DarkIronDwarfzhTW                       = '黑鐵矮人';
SET @DarkIronDwarfesES                       = 'Enano Hierro Negro';
SET @DarkIronDwarfesMX                       = 'Enano Hierro Negro';
SET @DarkIronDwarfruRU                       = 'Дворф Черного Железа';
SET @DarkIronDwarfjaJP                       = '';
SET @DarkIronDwarfptPT                       = '';
SET @DarkIronDwarfitIT                       = '';
SET @DarkIronDwarfUnk1                       = '';
SET @DarkIronDwarfUnk2                       = '';
SET @DarkIronDwarfUnk3                       = '';
SET @DarkIronDwarfUnk4                       = '';

SET @DarkIronDwarfFemaleenUS                 = '';
SET @DarkIronDwarfFemalekoKR                 = '';
SET @DarkIronDwarfFemalefrFR                 = '';
SET @DarkIronDwarfFemaledeDE                 = '';
SET @DarkIronDwarfFemalezhCN                 = '';
SET @DarkIronDwarfFemalezhTW                 = '';
SET @DarkIronDwarfFemaleesES                 = '';
SET @DarkIronDwarfFemaleesMX                 = '';
SET @DarkIronDwarfFemaleruRU                 = '';
SET @DarkIronDwarfFemalejaJP                 = '';
SET @DarkIronDwarfFemaleptPT                 = '';
SET @DarkIronDwarfFemaleitIT                 = '';
SET @DarkIronDwarfFemaleUnk1                 = '';
SET @DarkIronDwarfFemaleUnk2                 = '';
SET @DarkIronDwarfFemaleUnk3                 = '';
SET @DarkIronDwarfFemaleUnk4                 = '';

SET @DarkIronDwarfMaleenUS                   = '';
SET @DarkIronDwarfMalekoKR                   = '';
SET @DarkIronDwarfMalefrFR                   = '';
SET @DarkIronDwarfMaledeDE                   = '';
SET @DarkIronDwarfMalezhCN                   = '';
SET @DarkIronDwarfMalezhTW                   = '';
SET @DarkIronDwarfMaleesES                   = '';
SET @DarkIronDwarfMaleesMX                   = '';
SET @DarkIronDwarfMaleruRU                   = '';
SET @DarkIronDwarfMalejaJP                   = '';
SET @DarkIronDwarfMaleptPT                   = '';
SET @DarkIronDwarfMaleitIT                   = '';
SET @DarkIronDwarfMaleUnk1                   = '';
SET @DarkIronDwarfMaleUnk2                   = '';
SET @DarkIronDwarfMaleUnk3                   = '';
SET @DarkIronDwarfMaleUnk4                   = '';

SET @DarkIronDwarfRacialNameenUS             = 'Racial - Dark Iron Dwarf';
SET @DarkIronDwarfRacialNamekoKR             = '';
SET @DarkIronDwarfRacialNamefrFR             = 'Racial - Nain sombrefer';
SET @DarkIronDwarfRacialNamedeDE             = 'Volk - Dunkeleisenzwerg';
SET @DarkIronDwarfRacialNamezhCN             = '';
SET @DarkIronDwarfRacialNamezhTW             = '';
SET @DarkIronDwarfRacialNameesES             = 'Racial - Enano Hierro Negro';
SET @DarkIronDwarfRacialNameesMX             = 'Racial - Enano Hierro Negro';
SET @DarkIronDwarfRacialNameruRU             = 'Расовая - дворф Черного Железа';
SET @DarkIronDwarfRacialNamejaJP             = '';
SET @DarkIronDwarfRacialNameptPT             = '';
SET @DarkIronDwarfRacialNameitIT             = '';
SET @DarkIronDwarfRacialNameUnk1             = '';
SET @DarkIronDwarfRacialNameUnk2             = '';
SET @DarkIronDwarfRacialNameUnk3             = '';
SET @DarkIronDwarfRacialNameUnk4             = '';

SET @DarkIronDwarfPlayerenUS                 = '"PLAYER"," Dark Iron Dwarf"';
SET @DarkIronDwarfPlayerkoKR                 = '플레이어 - 검은무쇠 드워프';
SET @DarkIronDwarfPlayerfrFR                 = '"JOUEUR"," Nain Sombrefer"';
SET @DarkIronDwarfPlayerdeDE                 = '"SPIELER"," Dunkeleisenzwerg"';
SET @DarkIronDwarfPlayerzhCN                 = '黑铁矮人(玩家)';
SET @DarkIronDwarfPlayerzhTW                 = '黑鐵矮人(玩家)';
SET @DarkIronDwarfPlayeresES                 = '"JUGADOR"," Enano Hierro Negro"';
SET @DarkIronDwarfPlayeresMX                 = '"JUGADOR"," Enano Hierro Negro"';
SET @DarkIronDwarfPlayerruRU                 = 'ИГРОК: Дворф Черного Железа';
SET @DarkIronDwarfPlayerjaJP                 = '';
SET @DarkIronDwarfPlayerptPT                 = '';
SET @DarkIronDwarfPlayeritIT                 = '';
SET @DarkIronDwarfPlayerUnk1                 = '';
SET @DarkIronDwarfPlayerUnk2                 = '';
SET @DarkIronDwarfPlayerUnk3                 = '';
SET @DarkIronDwarfPlayerUnk4                 = '';

SET @DarkIronDwarfFactionNameenUS            = 'Shadowforge City';
SET @DarkIronDwarfFactionNamekoKR            = '';
SET @DarkIronDwarfFactionNamefrFR            = '';
SET @DarkIronDwarfFactionNamedeDE            = '';
SET @DarkIronDwarfFactionNamezhCN            = '';
SET @DarkIronDwarfFactionNamezhTW            = '';
SET @DarkIronDwarfFactionNameesES            = '';
SET @DarkIronDwarfFactionNameesMX            = '';
SET @DarkIronDwarfFactionNameruRU            = '';
SET @DarkIronDwarfFactionNamejaJP            = '';
SET @DarkIronDwarfFactionNameptPT            = '';
SET @DarkIronDwarfFactionNameitIT            = '';
SET @DarkIronDwarfFactionNameUnk1            = '';
SET @DarkIronDwarfFactionNameUnk2            = '';
SET @DarkIronDwarfFactionNameUnk3            = '';
SET @DarkIronDwarfFactionNameUnk4            = '';

SET @DarkIronDwarfFactionDescriptionenUS     = 'The capital of the Dark Iron Dwarves.';
SET @DarkIronDwarfFactionDescriptionkoKR     = '';
SET @DarkIronDwarfFactionDescriptionfrFR     = '';
SET @DarkIronDwarfFactionDescriptiondeDE     = '';
SET @DarkIronDwarfFactionDescriptionzhCN     = '';
SET @DarkIronDwarfFactionDescriptionzhTW     = '';
SET @DarkIronDwarfFactionDescriptionesES     = '';
SET @DarkIronDwarfFactionDescriptionesMX     = '';
SET @DarkIronDwarfFactionDescriptionruRU     = '';
SET @DarkIronDwarfFactionDescriptionjaJP     = '';
SET @DarkIronDwarfFactionDescriptionptPT     = '';
SET @DarkIronDwarfFactionDescriptionitIT     = '';
SET @DarkIronDwarfFactionDescriptionUnk1     = '';
SET @DarkIronDwarfFactionDescriptionUnk2     = '';
SET @DarkIronDwarfFactionDescriptionUnk3     = '';
SET @DarkIronDwarfFactionDescriptionUnk4     = '';

SET @DarkIronDwarfAchievementenUS            = 'Realm First! Level 80 Dark Iron Dwarf';
SET @DarkIronDwarfAchievementkoKR            = '';
SET @DarkIronDwarfAchievementfrFR            = '';
SET @DarkIronDwarfAchievementdeDE            = '';
SET @DarkIronDwarfAchievementzhCN            = '';
SET @DarkIronDwarfAchievementzhTW            = '';
SET @DarkIronDwarfAchievementesES            = '';
SET @DarkIronDwarfAchievementesMX            = '';
SET @DarkIronDwarfAchievementruRU            = '';
SET @DarkIronDwarfAchievementjaJP            = '';
SET @DarkIronDwarfAchievementptPT            = '';
SET @DarkIronDwarfAchievementitIT            = '';
SET @DarkIronDwarfAchievementUnk1            = '';
SET @DarkIronDwarfAchievementUnk2            = '';
SET @DarkIronDwarfAchievementUnk3            = '';
SET @DarkIronDwarfAchievementUnk4            = '';

SET @DarkIronDwarfAchievementDescriptionenUS = 'First Dark Iron Dwarf on the realm to achieve level 80.';
SET @DarkIronDwarfAchievementDescriptionkoKR = '';
SET @DarkIronDwarfAchievementDescriptionfrFR = '';
SET @DarkIronDwarfAchievementDescriptiondeDE = '';
SET @DarkIronDwarfAchievementDescriptionzhCN = '';
SET @DarkIronDwarfAchievementDescriptionzhTW = '';
SET @DarkIronDwarfAchievementDescriptionesES = '';
SET @DarkIronDwarfAchievementDescriptionesMX = '';
SET @DarkIronDwarfAchievementDescriptionruRU = '';
SET @DarkIronDwarfAchievementDescriptionjaJP = '';
SET @DarkIronDwarfAchievementDescriptionptPT = '';
SET @DarkIronDwarfAchievementDescriptionitIT = '';
SET @DarkIronDwarfAchievementDescriptionUnk1 = '';
SET @DarkIronDwarfAchievementDescriptionUnk2 = '';
SET @DarkIronDwarfAchievementDescriptionUnk3 = '';
SET @DarkIronDwarfAchievementDescriptionUnk4 = '';

-- Racial Mount Strings
SET @DarkIronDwarfMount1NameenUS                     = 'Dark Iron Core Hound';
SET @DarkIronDwarfMount1NamekoKR                     = '';
SET @DarkIronDwarfMount1NamefrFR                     = '';
SET @DarkIronDwarfMount1NamedeDE                     = '';
SET @DarkIronDwarfMount1NamezhCN                     = '';
SET @DarkIronDwarfMount1NamezhTW                     = '';
SET @DarkIronDwarfMount1NameesES                     = '';
SET @DarkIronDwarfMount1NameesMX                     = '';
SET @DarkIronDwarfMount1NameruRU                     = '';
SET @DarkIronDwarfMount1NamejaJP                     = '';
SET @DarkIronDwarfMount1NameptPT                     = '';
SET @DarkIronDwarfMount1NameitIT                     = '';
SET @DarkIronDwarfMount1NameUnk1                     = '';
SET @DarkIronDwarfMount1NameUnk2                     = '';
SET @DarkIronDwarfMount1NameUnk3                     = '';
SET @DarkIronDwarfMount1NameUnk4                     = '';

SET @DarkIronDwarfMount1SpellDescriptionenUS         = 'Summons and dismisses a rideable Dark Iron Core Hound.';
SET @DarkIronDwarfMount1SpellDescriptionkoKR         = '';
SET @DarkIronDwarfMount1SpellDescriptionfrFR         = '';
SET @DarkIronDwarfMount1SpellDescriptiondeDE         = '';
SET @DarkIronDwarfMount1SpellDescriptionzhCN         = '';
SET @DarkIronDwarfMount1SpellDescriptionzhTW         = '';
SET @DarkIronDwarfMount1SpellDescriptionesES         = '';
SET @DarkIronDwarfMount1SpellDescriptionesMX         = '';
SET @DarkIronDwarfMount1SpellDescriptionruRU         = '';
SET @DarkIronDwarfMount1SpellDescriptionjaJP         = '';
SET @DarkIronDwarfMount1SpellDescriptionptPT         = '';
SET @DarkIronDwarfMount1SpellDescriptionitIT         = '';
SET @DarkIronDwarfMount1SpellDescriptionUnk1         = '';
SET @DarkIronDwarfMount1SpellDescriptionUnk2         = '';
SET @DarkIronDwarfMount1SpellDescriptionUnk3         = '';
SET @DarkIronDwarfMount1SpellDescriptionUnk4         = '';

SET @DarkIronDwarfMount1ItemNameenUS                 = @DarkIronDwarfMount1NameenUS;
SET @DarkIronDwarfMount1ItemDescriptionenUS          = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Dark Iron Core Hound.';
