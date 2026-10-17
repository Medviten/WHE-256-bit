-- Race ID
SET @AlliancePandaren                          := @NextRace := @NextRace +1;    -- default: 19
SET @AlliancePandarenMask                       = 1 << (@AlliancePandaren - 1); -- race ID 19 → 262144
SET @AlliancePandarenHelmetMask                 = 1 << @AlliancePandaren;       -- race ID 19 → 524288

-- Important variable updates (Alliance vs. Horde)
SET @AllianceMask                               = @AllianceMask    | @AlliancePandarenMask;
SET @BarrensBros                                = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                           = @AllianceMask    | @HordeMask;
SET @CrossbowHunters                            = @CrossbowHunters | @AlliancePandarenMask;
SET @AlliancePandarenLanguage                   = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @AlliancePandarenAlliance                   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @AlliancePandarenKnowThyEnemy               = @KnowThyEnemyAlliance;

-- Miscellaneous
SET @AlliancePandarenExplorationSound           = @TaurenExplorationSound;
SET @AlliancePandarenCinematicSequence          = @HumanCinematicSequence;
SET @AlliancePandarenBlood                      = 1;
SET @AlliancePandarenMaleModelPath              = 'Character\\Pandaren\\Male\\PandarenMale.mdx';
SET @AlliancePandarenFemaleModelPath            = 'Character\\Pandaren\\Female\\PandarenFemale.mdx';
SET @AlliancePandarenMaleFootprint              = @FootprintPaw;
SET @AlliancePandarenFemaleFootprint            = @FootprintPaw;

-- Mounts (IDs are global, see config.sql)
SET @AlliancePandarenMount1                  = @SpellBlueDragonTurtle;
SET @AlliancePandarenMount1Model             = @DragonTurtleModel;
SET @AlliancePandarenMount1Display           = @BlueDragonTurtleDisplay;
SET @AlliancePandarenMount1CreatureID        = @BlueDragonTurtleCreatureID;
SET @AlliancePandarenMount1Item              = @BlueDragonTurtleItem;
SET @AlliancePandarenMount1ItemDisplay       = @BlueDragonTurtleItemDisplay;
SET @AlliancePandarenMount1IconID            = @IconBlueDragonTurtle;

SET @AlliancePandarenMount2                  = @SpellPurpleDragonTurtle;
SET @AlliancePandarenMount2Model             = @DragonTurtleModel;
SET @AlliancePandarenMount2Display           = @PurpleDragonTurtleDisplay;
SET @AlliancePandarenMount2CreatureID        = @PurpleDragonTurtleCreatureID;
SET @AlliancePandarenMount2Item              = @PurpleDragonTurtleItem;
SET @AlliancePandarenMount2ItemDisplay       = @PurpleDragonTurtleItemDisplay;
SET @AlliancePandarenMount2IconID            = @IconPurpleDragonTurtle;

SET @AlliancePandarenMount3                  = @SpellGreenDragonTurtle;
SET @AlliancePandarenMount3Model             = @DragonTurtleModel;
SET @AlliancePandarenMount3Display           = @GreenDragonTurtleDisplay;
SET @AlliancePandarenMount3CreatureID        = @GreenDragonTurtleCreatureID;
SET @AlliancePandarenMount3Item              = @GreenDragonTurtleItem;
SET @AlliancePandarenMount3ItemDisplay       = @GreenDragonTurtleItemDisplay;
SET @AlliancePandarenMount3IconID            = @IconGreenDragonTurtle;

SET @AlliancePandarenMount4                  = @SpellBlackDragonTurtle;
SET @AlliancePandarenMount4Model             = @DragonTurtleModel;
SET @AlliancePandarenMount4Display           = @BlackDragonTurtleDisplay;
SET @AlliancePandarenMount4CreatureID        = @BlackDragonTurtleCreatureID;
SET @AlliancePandarenMount4Item              = @BlackDragonTurtleItem;
SET @AlliancePandarenMount4ItemDisplay       = @BlackDragonTurtleItemDisplay;
SET @AlliancePandarenMount4IconID            = @IconBlackDragonTurtle;

-- Spells
SET @AlliancePandarenRacials                 = @PandarenRacials;
SET @AlliancePandarenRacial1                 = @PandarenRacial1;
SET @AlliancePandarenRacial2                 = @PandarenRacial2;
SET @AlliancePandarenRacial3                 = @PandarenRacial3;
SET @AlliancePandarenRacial4                 = @PandarenRacial4;
SET @AlliancePandarenRacial5                 = @PandarenRacial5;

-- Strings
SET @AlliancePandarenClientPrefix               = 'Pa';
SET @AlliancePandarenClientString               = 'AlliancePandaren';
SET @AlliancePandarenFacialHairCustomization1   = 'NORMAL';
SET @AlliancePandarenFacialHairCustomization2   = 'EARRINGS';
SET @AlliancePandarenHairCustomization          = 'NORMAL';

-- Localization Strings
SET @AlliancePandarenenUS                       = 'Pandaren';
SET @AlliancePandarenkoKR                       = '';
SET @AlliancePandarenfrFR                       = '';
SET @AlliancePandarendeDE                       = '';
SET @AlliancePandarenzhCN                       = '';
SET @AlliancePandarenzhTW                       = '';
SET @AlliancePandarenesES                       = '';
SET @AlliancePandarenesMX                       = '';
SET @AlliancePandarenruRU                       = '';
SET @AlliancePandarenjaJP                       = '';
SET @AlliancePandarenptPT                       = '';
SET @AlliancePandarenitIT                       = '';
SET @AlliancePandarenUnk1                       = '';
SET @AlliancePandarenUnk2                       = '';
SET @AlliancePandarenUnk3                       = '';
SET @AlliancePandarenUnk4                       = '';

SET @AlliancePandarenFemaleenUS                 = '';
SET @AlliancePandarenFemalekoKR                 = '';
SET @AlliancePandarenFemalefrFR                 = '';
SET @AlliancePandarenFemaledeDE                 = '';
SET @AlliancePandarenFemalezhCN                 = '';
SET @AlliancePandarenFemalezhTW                 = '';
SET @AlliancePandarenFemaleesES                 = '';
SET @AlliancePandarenFemaleesMX                 = '';
SET @AlliancePandarenFemaleruRU                 = '';
SET @AlliancePandarenFemalejaJP                 = '';
SET @AlliancePandarenFemaleptPT                 = '';
SET @AlliancePandarenFemaleitIT                 = '';
SET @AlliancePandarenFemaleUnk1                 = '';
SET @AlliancePandarenFemaleUnk2                 = '';
SET @AlliancePandarenFemaleUnk3                 = '';
SET @AlliancePandarenFemaleUnk4                 = '';

SET @AlliancePandarenMaleenUS                   = '';
SET @AlliancePandarenMalekoKR                   = '';
SET @AlliancePandarenMalefrFR                   = '';
SET @AlliancePandarenMaledeDE                   = '';
SET @AlliancePandarenMalezhCN                   = '';
SET @AlliancePandarenMalezhTW                   = '';
SET @AlliancePandarenMaleesES                   = '';
SET @AlliancePandarenMaleesMX                   = '';
SET @AlliancePandarenMaleruRU                   = '';
SET @AlliancePandarenMalejaJP                   = '';
SET @AlliancePandarenMaleptPT                   = '';
SET @AlliancePandarenMaleitIT                   = '';
SET @AlliancePandarenMaleUnk1                   = '';
SET @AlliancePandarenMaleUnk2                   = '';
SET @AlliancePandarenMaleUnk3                   = '';
SET @AlliancePandarenMaleUnk4                   = '';

SET @AlliancePandarenRacialNameenUS             = 'Racial - Pandaren';
SET @AlliancePandarenRacialNamekoKR             = '';
SET @AlliancePandarenRacialNamefrFR             = '';
SET @AlliancePandarenRacialNamedeDE             = '';
SET @AlliancePandarenRacialNamezhCN             = '';
SET @AlliancePandarenRacialNamezhTW             = '';
SET @AlliancePandarenRacialNameesES             = '';
SET @AlliancePandarenRacialNameesMX             = '';
SET @AlliancePandarenRacialNameruRU             = '';
SET @AlliancePandarenRacialNamejaJP             = '';
SET @AlliancePandarenRacialNameptPT             = '';
SET @AlliancePandarenRacialNameitIT             = '';
SET @AlliancePandarenRacialNameUnk1             = '';
SET @AlliancePandarenRacialNameUnk2             = '';
SET @AlliancePandarenRacialNameUnk3             = '';
SET @AlliancePandarenRacialNameUnk4             = '';

SET @AlliancePandarenPlayerenUS                 = '"PLAYER", " Pandaren (Alliance)"';
SET @AlliancePandarenPlayerkoKR                 = '';
SET @AlliancePandarenPlayerfrFR                 = '';
SET @AlliancePandarenPlayerdeDE                 = '';
SET @AlliancePandarenPlayerzhCN                 = '';
SET @AlliancePandarenPlayerzhTW                 = '';
SET @AlliancePandarenPlayeresES                 = '';
SET @AlliancePandarenPlayeresMX                 = '';
SET @AlliancePandarenPlayerruRU                 = '';
SET @AlliancePandarenPlayerjaJP                 = '';
SET @AlliancePandarenPlayerptPT                 = '';
SET @AlliancePandarenPlayeritIT                 = '';
SET @AlliancePandarenPlayerUnk1                 = '';
SET @AlliancePandarenPlayerUnk2                 = '';
SET @AlliancePandarenPlayerUnk3                 = '';
SET @AlliancePandarenPlayerUnk4                 = '';

SET @AlliancePandarenFactionNameenUS            = 'Tushui Pandaren';
SET @AlliancePandarenFactionNamekoKR            = '';
SET @AlliancePandarenFactionNamefrFR            = '';
SET @AlliancePandarenFactionNamedeDE            = '';
SET @AlliancePandarenFactionNamezhCN            = '';
SET @AlliancePandarenFactionNamezhTW            = '';
SET @AlliancePandarenFactionNameesES            = '';
SET @AlliancePandarenFactionNameesMX            = '';
SET @AlliancePandarenFactionNameruRU            = '';
SET @AlliancePandarenFactionNamejaJP            = '';
SET @AlliancePandarenFactionNameptPT            = '';
SET @AlliancePandarenFactionNameitIT            = '';
SET @AlliancePandarenFactionNameUnk1            = '';
SET @AlliancePandarenFactionNameUnk2            = '';
SET @AlliancePandarenFactionNameUnk3            = '';
SET @AlliancePandarenFactionNameUnk4            = '';

SET @AlliancePandarenFactionDescriptionenUS     = 'Led by the stalwart Aysa Cloudsinger, the Tushui Pandaren believe in contemplation and reasoned action.';
SET @AlliancePandarenFactionDescriptionkoKR     = '';
SET @AlliancePandarenFactionDescriptionfrFR     = '';
SET @AlliancePandarenFactionDescriptiondeDE     = '';
SET @AlliancePandarenFactionDescriptionzhCN     = '';
SET @AlliancePandarenFactionDescriptionzhTW     = '';
SET @AlliancePandarenFactionDescriptionesES     = '';
SET @AlliancePandarenFactionDescriptionesMX     = '';
SET @AlliancePandarenFactionDescriptionruRU     = '';
SET @AlliancePandarenFactionDescriptionjaJP     = '';
SET @AlliancePandarenFactionDescriptionptPT     = '';
SET @AlliancePandarenFactionDescriptionitIT     = '';
SET @AlliancePandarenFactionDescriptionUnk1     = '';
SET @AlliancePandarenFactionDescriptionUnk2     = '';
SET @AlliancePandarenFactionDescriptionUnk3     = '';
SET @AlliancePandarenFactionDescriptionUnk4     = '';

SET @AlliancePandarenAchievementenUS            = 'Realm First! Level 80 Pandaren (Alliance)';
SET @AlliancePandarenAchievementkoKR            = '';
SET @AlliancePandarenAchievementfrFR            = '';
SET @AlliancePandarenAchievementdeDE            = '';
SET @AlliancePandarenAchievementzhCN            = '';
SET @AlliancePandarenAchievementzhTW            = '';
SET @AlliancePandarenAchievementesES            = '';
SET @AlliancePandarenAchievementesMX            = '';
SET @AlliancePandarenAchievementruRU            = '';
SET @AlliancePandarenAchievementjaJP            = '';
SET @AlliancePandarenAchievementptPT            = '';
SET @AlliancePandarenAchievementitIT            = '';
SET @AlliancePandarenAchievementUnk1            = '';
SET @AlliancePandarenAchievementUnk2            = '';
SET @AlliancePandarenAchievementUnk3            = '';
SET @AlliancePandarenAchievementUnk4            = '';

SET @AlliancePandarenAchievementDescriptionenUS = 'First (Alliance) Pandaren on the realm to achieve level 80.';
SET @AlliancePandarenAchievementDescriptionkoKR = '';
SET @AlliancePandarenAchievementDescriptionfrFR = '';
SET @AlliancePandarenAchievementDescriptiondeDE = '';
SET @AlliancePandarenAchievementDescriptionzhCN = '';
SET @AlliancePandarenAchievementDescriptionzhTW = '';
SET @AlliancePandarenAchievementDescriptionesES = '';
SET @AlliancePandarenAchievementDescriptionesMX = '';
SET @AlliancePandarenAchievementDescriptionruRU = '';
SET @AlliancePandarenAchievementDescriptionjaJP = '';
SET @AlliancePandarenAchievementDescriptionptPT = '';
SET @AlliancePandarenAchievementDescriptionitIT = '';
SET @AlliancePandarenAchievementDescriptionUnk1 = '';
SET @AlliancePandarenAchievementDescriptionUnk2 = '';
SET @AlliancePandarenAchievementDescriptionUnk3 = '';
SET @AlliancePandarenAchievementDescriptionUnk4 = '';


-- Racial Mount
SET @AlliancePandarenMount1NameenUS                = 'Blue Dragon Turtle';
SET @AlliancePandarenMount1NamekoKR                = '';
SET @AlliancePandarenMount1NamefrFR                = '';
SET @AlliancePandarenMount1NamedeDE                = '';
SET @AlliancePandarenMount1NamezhCN                = '';
SET @AlliancePandarenMount1NamezhTW                = '';
SET @AlliancePandarenMount1NameesES                = '';
SET @AlliancePandarenMount1NameesMX                = '';
SET @AlliancePandarenMount1NameruRU                = '';
SET @AlliancePandarenMount1NamejaJP                = '';
SET @AlliancePandarenMount1NameptPT                = '';
SET @AlliancePandarenMount1NameitIT                = '';
SET @AlliancePandarenMount1NameUnk1                = '';
SET @AlliancePandarenMount1NameUnk2                = '';
SET @AlliancePandarenMount1NameUnk3                = '';
SET @AlliancePandarenMount1NameUnk4                = '';

SET @AlliancePandarenMount1SpellDescriptionenUS    = 'Summons and dismisses a rideable Blue Dragon Turtle.';
SET @AlliancePandarenMount1SpellDescriptionkoKR    = '';
SET @AlliancePandarenMount1SpellDescriptionfrFR    = '';
SET @AlliancePandarenMount1SpellDescriptiondeDE    = '';
SET @AlliancePandarenMount1SpellDescriptionzhCN    = '';
SET @AlliancePandarenMount1SpellDescriptionzhTW    = '';
SET @AlliancePandarenMount1SpellDescriptionesES    = '';
SET @AlliancePandarenMount1SpellDescriptionesMX    = '';
SET @AlliancePandarenMount1SpellDescriptionruRU    = '';
SET @AlliancePandarenMount1SpellDescriptionjaJP    = '';
SET @AlliancePandarenMount1SpellDescriptionptPT    = '';
SET @AlliancePandarenMount1SpellDescriptionitIT    = '';
SET @AlliancePandarenMount1SpellDescriptionUnk1    = '';
SET @AlliancePandarenMount1SpellDescriptionUnk2    = '';
SET @AlliancePandarenMount1SpellDescriptionUnk3    = '';
SET @AlliancePandarenMount1SpellDescriptionUnk4    = '';

SET @AlliancePandarenMount1ItemNameenUS          = 'Reins of the Blue Dragon Turtle';
SET @AlliancePandarenMount1ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Blue Dragon Turtle.';

SET @AlliancePandarenMount2NameenUS              = 'Purple Dragon Turtle';
SET @AlliancePandarenMount2NamekoKR              = '';
SET @AlliancePandarenMount2NamefrFR              = '';
SET @AlliancePandarenMount2NamedeDE              = '';
SET @AlliancePandarenMount2NamezhCN              = '';
SET @AlliancePandarenMount2NamezhTW              = '';
SET @AlliancePandarenMount2NameesES              = '';
SET @AlliancePandarenMount2NameesMX              = '';
SET @AlliancePandarenMount2NameruRU              = '';
SET @AlliancePandarenMount2NamejaJP              = '';
SET @AlliancePandarenMount2NameptPT              = '';
SET @AlliancePandarenMount2NameitIT              = '';
SET @AlliancePandarenMount2NameUnk1              = '';
SET @AlliancePandarenMount2NameUnk2              = '';
SET @AlliancePandarenMount2NameUnk3              = '';
SET @AlliancePandarenMount2NameUnk4              = '';

SET @AlliancePandarenMount2SpellDescriptionenUS  = 'Summons and dismisses a rideable Purple Dragon Turtle.';
SET @AlliancePandarenMount2SpellDescriptionkoKR  = '';
SET @AlliancePandarenMount2SpellDescriptionfrFR  = '';
SET @AlliancePandarenMount2SpellDescriptiondeDE  = '';
SET @AlliancePandarenMount2SpellDescriptionzhCN  = '';
SET @AlliancePandarenMount2SpellDescriptionzhTW  = '';
SET @AlliancePandarenMount2SpellDescriptionesES  = '';
SET @AlliancePandarenMount2SpellDescriptionesMX  = '';
SET @AlliancePandarenMount2SpellDescriptionruRU  = '';
SET @AlliancePandarenMount2SpellDescriptionjaJP  = '';
SET @AlliancePandarenMount2SpellDescriptionptPT  = '';
SET @AlliancePandarenMount2SpellDescriptionitIT  = '';
SET @AlliancePandarenMount2SpellDescriptionUnk1  = '';
SET @AlliancePandarenMount2SpellDescriptionUnk2  = '';
SET @AlliancePandarenMount2SpellDescriptionUnk3  = '';
SET @AlliancePandarenMount2SpellDescriptionUnk4  = '';

SET @AlliancePandarenMount2ItemNameenUS          = 'Reins of the Purple Dragon Turtle';
SET @AlliancePandarenMount2ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Purple Dragon Turtle.';

SET @AlliancePandarenMount3NameenUS              = 'Green Dragon Turtle';
SET @AlliancePandarenMount3NamekoKR              = '';
SET @AlliancePandarenMount3NamefrFR              = '';
SET @AlliancePandarenMount3NamedeDE              = '';
SET @AlliancePandarenMount3NamezhCN              = '';
SET @AlliancePandarenMount3NamezhTW              = '';
SET @AlliancePandarenMount3NameesES              = '';
SET @AlliancePandarenMount3NameesMX              = '';
SET @AlliancePandarenMount3NameruRU              = '';
SET @AlliancePandarenMount3NamejaJP              = '';
SET @AlliancePandarenMount3NameptPT              = '';
SET @AlliancePandarenMount3NameitIT              = '';
SET @AlliancePandarenMount3NameUnk1              = '';
SET @AlliancePandarenMount3NameUnk2              = '';
SET @AlliancePandarenMount3NameUnk3              = '';
SET @AlliancePandarenMount3NameUnk4              = '';

SET @AlliancePandarenMount3SpellDescriptionenUS  = 'Summons and dismisses a rideable Green Dragon Turtle.';
SET @AlliancePandarenMount3SpellDescriptionkoKR  = '';
SET @AlliancePandarenMount3SpellDescriptionfrFR  = '';
SET @AlliancePandarenMount3SpellDescriptiondeDE  = '';
SET @AlliancePandarenMount3SpellDescriptionzhCN  = '';
SET @AlliancePandarenMount3SpellDescriptionzhTW  = '';
SET @AlliancePandarenMount3SpellDescriptionesES  = '';
SET @AlliancePandarenMount3SpellDescriptionesMX  = '';
SET @AlliancePandarenMount3SpellDescriptionruRU  = '';
SET @AlliancePandarenMount3SpellDescriptionjaJP  = '';
SET @AlliancePandarenMount3SpellDescriptionptPT  = '';
SET @AlliancePandarenMount3SpellDescriptionitIT  = '';
SET @AlliancePandarenMount3SpellDescriptionUnk1  = '';
SET @AlliancePandarenMount3SpellDescriptionUnk2  = '';
SET @AlliancePandarenMount3SpellDescriptionUnk3  = '';
SET @AlliancePandarenMount3SpellDescriptionUnk4  = '';

SET @AlliancePandarenMount3ItemNameenUS          = 'Reins of the Green Dragon Turtle';
SET @AlliancePandarenMount3ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Green Dragon Turtle.';

SET @AlliancePandarenMount4NameenUS              = 'Black Dragon Turtle';
SET @AlliancePandarenMount4NamekoKR              = '';
SET @AlliancePandarenMount4NamefrFR              = '';
SET @AlliancePandarenMount4NamedeDE              = '';
SET @AlliancePandarenMount4NamezhCN              = '';
SET @AlliancePandarenMount4NamezhTW              = '';
SET @AlliancePandarenMount4NameesES              = '';
SET @AlliancePandarenMount4NameesMX              = '';
SET @AlliancePandarenMount4NameruRU              = '';
SET @AlliancePandarenMount4NamejaJP              = '';
SET @AlliancePandarenMount4NameptPT              = '';
SET @AlliancePandarenMount4NameitIT              = '';
SET @AlliancePandarenMount4NameUnk1              = '';
SET @AlliancePandarenMount4NameUnk2              = '';
SET @AlliancePandarenMount4NameUnk3              = '';
SET @AlliancePandarenMount4NameUnk4              = '';

SET @AlliancePandarenMount4SpellDescriptionenUS  = 'Summons and dismisses a rideable Black Dragon Turtle.';
SET @AlliancePandarenMount4SpellDescriptionkoKR  = '';
SET @AlliancePandarenMount4SpellDescriptionfrFR  = '';
SET @AlliancePandarenMount4SpellDescriptiondeDE  = '';
SET @AlliancePandarenMount4SpellDescriptionzhCN  = '';
SET @AlliancePandarenMount4SpellDescriptionzhTW  = '';
SET @AlliancePandarenMount4SpellDescriptionesES  = '';
SET @AlliancePandarenMount4SpellDescriptionesMX  = '';
SET @AlliancePandarenMount4SpellDescriptionruRU  = '';
SET @AlliancePandarenMount4SpellDescriptionjaJP  = '';
SET @AlliancePandarenMount4SpellDescriptionptPT  = '';
SET @AlliancePandarenMount4SpellDescriptionitIT  = '';
SET @AlliancePandarenMount4SpellDescriptionUnk1  = '';
SET @AlliancePandarenMount4SpellDescriptionUnk2  = '';
SET @AlliancePandarenMount4SpellDescriptionUnk3  = '';
SET @AlliancePandarenMount4SpellDescriptionUnk4  = '';

SET @AlliancePandarenMount4ItemNameenUS          = 'Reins of the Black Dragon Turtle';
SET @AlliancePandarenMount4ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Black Dragon Turtle.';
