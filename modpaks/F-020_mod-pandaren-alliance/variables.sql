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

-- Strings
SET @AlliancePandarenClientPrefix               = 'Pa';
SET @AlliancePandarenClientString               = 'AlliancePandaren';

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


-- Racial Mount
SET @DragonTurtleBlueNameenUS                = 'Blue Dragon Turtle';
SET @DragonTurtleBlueNamekoKR                = '';
SET @DragonTurtleBlueNamefrFR                = '';
SET @DragonTurtleBlueNamedeDE                = '';
SET @DragonTurtleBlueNamezhCN                = '';
SET @DragonTurtleBlueNamezhTW                = '';
SET @DragonTurtleBlueNameesES                = '';
SET @DragonTurtleBlueNameesMX                = '';
SET @DragonTurtleBlueNameruRU                = '';
SET @DragonTurtleBlueNamejaJP                = '';
SET @DragonTurtleBlueNameptPT                = '';
SET @DragonTurtleBlueNameitIT                = '';

SET @DragonTurtleBlueSpellDescriptionenUS    = 'Summons and dismisses a rideable Blue Dragon Turtle.';
SET @DragonTurtleBlueSpellDescriptionkoKR    = '';
SET @DragonTurtleBlueSpellDescriptionfrFR    = '';
SET @DragonTurtleBlueSpellDescriptiondeDE    = '';
SET @DragonTurtleBlueSpellDescriptionzhCN    = '';
SET @DragonTurtleBlueSpellDescriptionzhTW    = '';
SET @DragonTurtleBlueSpellDescriptionesES    = '';
SET @DragonTurtleBlueSpellDescriptionesMX    = '';
SET @DragonTurtleBlueSpellDescriptionruRU    = '';
SET @DragonTurtleBlueSpellDescriptionjaJP    = '';
SET @DragonTurtleBlueSpellDescriptionptPT    = '';
SET @DragonTurtleBlueSpellDescriptionitIT    = '';

SET @DragonTurtleBlueItemNameenUS          = 'Reins of the Blue Dragon Turtle';
SET @DragonTurtleBlueItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Blue Dragon Turtle.';

SET @DragonTurtlePurpleNameenUS              = 'Purple Dragon Turtle';
SET @DragonTurtlePurpleNamekoKR              = '';
SET @DragonTurtlePurpleNamefrFR              = '';
SET @DragonTurtlePurpleNamedeDE              = '';
SET @DragonTurtlePurpleNamezhCN              = '';
SET @DragonTurtlePurpleNamezhTW              = '';
SET @DragonTurtlePurpleNameesES              = '';
SET @DragonTurtlePurpleNameesMX              = '';
SET @DragonTurtlePurpleNameruRU              = '';
SET @DragonTurtlePurpleNamejaJP              = '';
SET @DragonTurtlePurpleNameptPT              = '';
SET @DragonTurtlePurpleNameitIT              = '';

SET @DragonTurtlePurpleSpellDescriptionenUS  = 'Summons and dismisses a rideable Purple Dragon Turtle.';
SET @DragonTurtlePurpleSpellDescriptionkoKR  = '';
SET @DragonTurtlePurpleSpellDescriptionfrFR  = '';
SET @DragonTurtlePurpleSpellDescriptiondeDE  = '';
SET @DragonTurtlePurpleSpellDescriptionzhCN  = '';
SET @DragonTurtlePurpleSpellDescriptionzhTW  = '';
SET @DragonTurtlePurpleSpellDescriptionesES  = '';
SET @DragonTurtlePurpleSpellDescriptionesMX  = '';
SET @DragonTurtlePurpleSpellDescriptionruRU  = '';
SET @DragonTurtlePurpleSpellDescriptionjaJP  = '';
SET @DragonTurtlePurpleSpellDescriptionptPT  = '';
SET @DragonTurtlePurpleSpellDescriptionitIT  = '';

SET @DragonTurtlePurpleItemNameenUS          = 'Reins of the Purple Dragon Turtle';
SET @DragonTurtlePurpleItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Purple Dragon Turtle.';

SET @DragonTurtleGreenNameenUS              = 'Green Dragon Turtle';
SET @DragonTurtleGreenNamekoKR              = '';
SET @DragonTurtleGreenNamefrFR              = '';
SET @DragonTurtleGreenNamedeDE              = '';
SET @DragonTurtleGreenNamezhCN              = '';
SET @DragonTurtleGreenNamezhTW              = '';
SET @DragonTurtleGreenNameesES              = '';
SET @DragonTurtleGreenNameesMX              = '';
SET @DragonTurtleGreenNameruRU              = '';
SET @DragonTurtleGreenNamejaJP              = '';
SET @DragonTurtleGreenNameptPT              = '';
SET @DragonTurtleGreenNameitIT              = '';

SET @DragonTurtleGreenSpellDescriptionenUS  = 'Summons and dismisses a rideable Green Dragon Turtle.';
SET @DragonTurtleGreenSpellDescriptionkoKR  = '';
SET @DragonTurtleGreenSpellDescriptionfrFR  = '';
SET @DragonTurtleGreenSpellDescriptiondeDE  = '';
SET @DragonTurtleGreenSpellDescriptionzhCN  = '';
SET @DragonTurtleGreenSpellDescriptionzhTW  = '';
SET @DragonTurtleGreenSpellDescriptionesES  = '';
SET @DragonTurtleGreenSpellDescriptionesMX  = '';
SET @DragonTurtleGreenSpellDescriptionruRU  = '';
SET @DragonTurtleGreenSpellDescriptionjaJP  = '';
SET @DragonTurtleGreenSpellDescriptionptPT  = '';
SET @DragonTurtleGreenSpellDescriptionitIT  = '';

SET @DragonTurtleGreenItemNameenUS          = 'Reins of the Green Dragon Turtle';
SET @DragonTurtleGreenItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Green Dragon Turtle.';

SET @DragonTurtleBlackNameenUS              = 'Black Dragon Turtle';
SET @DragonTurtleBlackNamekoKR              = '';
SET @DragonTurtleBlackNamefrFR              = '';
SET @DragonTurtleBlackNamedeDE              = '';
SET @DragonTurtleBlackNamezhCN              = '';
SET @DragonTurtleBlackNamezhTW              = '';
SET @DragonTurtleBlackNameesES              = '';
SET @DragonTurtleBlackNameesMX              = '';
SET @DragonTurtleBlackNameruRU              = '';
SET @DragonTurtleBlackNamejaJP              = '';
SET @DragonTurtleBlackNameptPT              = '';
SET @DragonTurtleBlackNameitIT              = '';

SET @DragonTurtleBlackSpellDescriptionenUS  = 'Summons and dismisses a rideable Black Dragon Turtle.';
SET @DragonTurtleBlackSpellDescriptionkoKR  = '';
SET @DragonTurtleBlackSpellDescriptionfrFR  = '';
SET @DragonTurtleBlackSpellDescriptiondeDE  = '';
SET @DragonTurtleBlackSpellDescriptionzhCN  = '';
SET @DragonTurtleBlackSpellDescriptionzhTW  = '';
SET @DragonTurtleBlackSpellDescriptionesES  = '';
SET @DragonTurtleBlackSpellDescriptionesMX  = '';
SET @DragonTurtleBlackSpellDescriptionruRU  = '';
SET @DragonTurtleBlackSpellDescriptionjaJP  = '';
SET @DragonTurtleBlackSpellDescriptionptPT  = '';
SET @DragonTurtleBlackSpellDescriptionitIT  = '';

SET @DragonTurtleBlackItemNameenUS          = 'Reins of the Black Dragon Turtle';
SET @DragonTurtleBlackItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Black Dragon Turtle.';
