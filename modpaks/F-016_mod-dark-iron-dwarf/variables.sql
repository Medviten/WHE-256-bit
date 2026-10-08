-- Race ID
SET @DarkIronDwarf                          := @NextRace := @NextRace +1;    -- default: 16
SET @DarkIronDwarfMask                       = 1 << (@DarkIronDwarf - 1); -- race ID 16 → 32768
SET @DarkIronDwarfHelmetMask                 = 1 << @DarkIronDwarf; -- race ID 16 → 65536

-- Important variable update
SET @AllianceMask                            = @AllianceMask | @DarkIronDwarfMask;
SET @PlayableRaceMask                        = @AllianceMask | @HordeMask;
SET @GunHunters                              = @GunHunters   | @DarkIronDwarfMask;
SET @DarkIronDwarfLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @DarkIronDwarfAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @DarkIronDwarfExplorationSound           = @DwarfExplorationSound;
SET @DarkIronDwarfCinematicSequence          = @DwarfCinematicSequence;
SET @DarkIronDwarfBlood                      = 1;
SET @DarkIronDwarfMaleModelPath              = 'Character\\Darkirondwarf\\male\\darkirondwarfMale.M2';
SET @DarkIronDwarfFemaleModelPath            = 'Character\\Darkirondwarf\\female\\darkirondwarfFemale.M2';
SET @DarkIronDwarfMaleFootprint              = @FootprintShoe;
SET @DarkIronDwarfFemaleFootprint            = @FootprintShoe;

-- Strings
SET @DarkIronDwarfClientPrefix               = 'Dw';
SET @DarkIronDwarfClientString               = 'DarkIronDwarf';

-- Localization Strings
SET @DarkIronDwarfenUS                       = 'Dark Iron Dwarf';
SET @DarkIronDwarfkoKR                       = '검은무쇠 드워프';
SET @DarkIronDwarffrFR                       = 'Nain Sombrefer';
SET @DarkIronDwarfdeDE                       = 'Dunkeleisenzwerg';
SET @DarkIronDwarfzhCN                       = '黑铁矮人';
SET @DarkIronDwarfzhTW                       = '黑鐵矮人';
SET @DarkIronDwarfesES                       = 'Enano Hierro Negro';
SET @DarkIronDwarfesMX                       = 'Enano Hierro Negro',
SET @DarkIronDwarfruRU                       = 'Дворф Черного Железа',
SET @DarkIronDwarfjaJP                       = '';
SET @DarkIronDwarfptPT                       = '';
SET @DarkIronDwarfitIT                       = '';

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

SET @DarkIronDwarfRacialNameenUS             = 'Racial - Dark Iron Dwarf';
SET @DarkIronDwarfRacialNamekoKR             = '';
SET @DarkIronDwarfRacialNamefrFR             = 'Racial - Nain sombrefer';
SET @DarkIronDwarfRacialNamedeDE             = 'Volk - Dunkeleisenzwerg';
SET @DarkIronDwarfRacialNamezhCN             = '';
SET @DarkIronDwarfRacialNamezhTW             = '';
SET @DarkIronDwarfRacialNameesES             = 'Racial - Enano Hierro Negro';
SET @DarkIronDwarfRacialNameesMX             = 'Racial - Enano Hierro Negro',
SET @DarkIronDwarfRacialNameruRU             = 'Расовая - дворф Черного Железа',
SET @DarkIronDwarfRacialNamejaJP             = '';
SET @DarkIronDwarfRacialNameptPT             = '';
SET @DarkIronDwarfRacialNameitIT             = '';

SET @DarkIronDwarfPlayerenUS                 = '"PLAYER"," Dark Iron Dwarf"';
SET @DarkIronDwarfPlayerkoKR                 = '플레이어 - 검은무쇠 드워프';
SET @DarkIronDwarfPlayerfrFR                 = '"JOUEUR"," Nain Sombrefer"';
SET @DarkIronDwarfPlayerdeDE                 = '"SPIELER"," Dunkeleisenzwerg"';
SET @DarkIronDwarfPlayerzhCN                 = '黑铁矮人(玩家)';
SET @DarkIronDwarfPlayerzhTW                 = '黑鐵矮人(玩家)';
SET @DarkIronDwarfPlayeresES                 = '"JUGADOR"," Enano Hierro Negro"';
SET @DarkIronDwarfPlayeresMX                 = '"JUGADOR"," Enano Hierro Negro"',
SET @DarkIronDwarfPlayerruRU                 = 'ИГРОК: Дворф Черного Железа',
SET @DarkIronDwarfPlayerjaJP                 = '';
SET @DarkIronDwarfPlayerptPT                 = '';
SET @DarkIronDwarfPlayeritIT                 = '';

SET @DarkIronDwarfFactionNameenUS            = 'Shadowforge City';
SET @DarkIronDwarfFactionNamekoKR            = '';
SET @DarkIronDwarfFactionNamefrFR            = '';
SET @DarkIronDwarfFactionNamedeDE            = '';
SET @DarkIronDwarfFactionNamezhCN            = '';
SET @DarkIronDwarfFactionNamezhTW            = '';
SET @DarkIronDwarfFactionNameesES            = '';
SET @DarkIronDwarfFactionNameesMX            = '',
SET @DarkIronDwarfFactionNameruRU            = '',
SET @DarkIronDwarfFactionNamejaJP            = '';
SET @DarkIronDwarfFactionNameptPT            = '';
SET @DarkIronDwarfFactionNameitIT            = '';

SET @DarkIronDwarfFactionDescriptionenUS     = 'The capital of the Dark Iron Dwarves.';
SET @DarkIronDwarfFactionDescriptionkoKR     = '';
SET @DarkIronDwarfFactionDescriptionfrFR     = '';
SET @DarkIronDwarfFactionDescriptiondeDE     = '';
SET @DarkIronDwarfFactionDescriptionzhCN     = '';
SET @DarkIronDwarfFactionDescriptionzhTW     = '';
SET @DarkIronDwarfFactionDescriptionesES     = '';
SET @DarkIronDwarfFactionDescriptionesMX     = '',
SET @DarkIronDwarfFactionDescriptionruRU     = '',
SET @DarkIronDwarfFactionDescriptionjaJP     = '';
SET @DarkIronDwarfFactionDescriptionptPT     = '';
SET @DarkIronDwarfFactionDescriptionitIT     = '';

SET @DarkIronDwarfAchievementenUS            = 'Realm First! Level 80 Dark Iron Dwarf';
SET @DarkIronDwarfAchievementkoKR            = '';
SET @DarkIronDwarfAchievementfrFR            = '';
SET @DarkIronDwarfAchievementdeDE            = '';
SET @DarkIronDwarfAchievementzhCN            = '';
SET @DarkIronDwarfAchievementzhTW            = '';
SET @DarkIronDwarfAchievementesES            = '';
SET @DarkIronDwarfAchievementesMX            = '',
SET @DarkIronDwarfAchievementruRU            = '',
SET @DarkIronDwarfAchievementjaJP            = '';
SET @DarkIronDwarfAchievementptPT            = '';
SET @DarkIronDwarfAchievementitIT            = '';

SET @DarkIronDwarfAchievementDescriptionenUS = 'First Dark Iron Dwarf on the realm to achieve level 80.';
SET @DarkIronDwarfAchievementDescriptionkoKR = '';
SET @DarkIronDwarfAchievementDescriptionfrFR = '';
SET @DarkIronDwarfAchievementDescriptiondeDE = '';
SET @DarkIronDwarfAchievementDescriptionzhCN = '';
SET @DarkIronDwarfAchievementDescriptionzhTW = '';
SET @DarkIronDwarfAchievementDescriptionesES = '';
SET @DarkIronDwarfAchievementDescriptionesMX = '',
SET @DarkIronDwarfAchievementDescriptionruRU = '',
SET @DarkIronDwarfAchievementDescriptionjaJP = '';
SET @DarkIronDwarfAchievementDescriptionptPT = '';
SET @DarkIronDwarfAchievementDescriptionitIT = '';
