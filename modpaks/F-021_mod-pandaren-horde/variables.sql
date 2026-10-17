-- Race ID
SET @HordePandaren                          := @NextRace := @NextRace +1; -- default: 20
SET @HordePandarenMask                       = 1 << (@HordePandaren - 1); -- race ID 20 → 524288
SET @HordePandarenHelmetMask                 = 1 << @HordePandaren;       -- race ID 20 → 1048576

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                               = @HordeMask       |  @HordePandarenMask;
SET @BarrensBros                             = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                        = @AllianceMask    |  @HordeMask;
SET @CrossbowHunters                         = @CrossbowHunters |  @HordePandarenMask;
SET @HordePandarenLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @HordePandarenAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @HordePandarenKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @HordePandarenExplorationSound           = @TaurenExplorationSound;
SET @HordePandarenCinematicSequence          = @TaurenCinematicSequence;
SET @HordePandarenBlood                      = 1;
SET @HordePandarenMaleModelPath              = 'Character\\Pandaren\\Male\\PandarenMale.mdx';
SET @HordePandarenFemaleModelPath            = 'Character\\Pandaren\\Female\\PandarenFemale.mdx';
SET @HordePandarenMaleFootprint              = @FootprintPaw;
SET @HordePandarenFemaleFootprint            = @FootprintPaw;

-- Mounts (IDs are global, see config.sql)
SET @HordePandarenMount1                     = @SpellBlueDragonTurtle;
SET @HordePandarenMount1Model                = @DragonTurtleModel;
SET @HordePandarenMount1Display              = @BlueDragonTurtleDisplay;
SET @HordePandarenMount1CreatureID           = @BlueDragonTurtleCreatureID;
SET @HordePandarenMount1Item                 = @BlueDragonTurtleItem;
SET @HordePandarenMount1ItemDisplay          = @BlueDragonTurtleItemDisplay;
SET @HordePandarenMount1IconID               = @IconBlueDragonTurtle;

SET @HordePandarenMount2                     = @SpellPurpleDragonTurtle;
SET @HordePandarenMount2Model                = @DragonTurtleModel;
SET @HordePandarenMount2Display              = @PurpleDragonTurtleDisplay;
SET @HordePandarenMount2CreatureID           = @PurpleDragonTurtleCreatureID;
SET @HordePandarenMount2Item                 = @PurpleDragonTurtleItem;
SET @HordePandarenMount2ItemDisplay          = @PurpleDragonTurtleItemDisplay;
SET @HordePandarenMount2IconID               = @IconPurpleDragonTurtle;

SET @HordePandarenMount3                     = @SpellGreenDragonTurtle;
SET @HordePandarenMount3Model                = @DragonTurtleModel;
SET @HordePandarenMount3Display              = @GreenDragonTurtleDisplay;
SET @HordePandarenMount3CreatureID           = @GreenDragonTurtleCreatureID;
SET @HordePandarenMount3Item                 = @GreenDragonTurtleItem;
SET @HordePandarenMount3ItemDisplay          = @GreenDragonTurtleItemDisplay;
SET @HordePandarenMount3IconID               = @IconGreenDragonTurtle;

SET @HordePandarenMount4                     = @SpellBlackDragonTurtle;
SET @HordePandarenMount4Model                = @DragonTurtleModel;
SET @HordePandarenMount4Display              = @BlackDragonTurtleDisplay;
SET @HordePandarenMount4CreatureID           = @BlackDragonTurtleCreatureID;
SET @HordePandarenMount4Item                 = @BlackDragonTurtleItem;
SET @HordePandarenMount4ItemDisplay          = @BlackDragonTurtleItemDisplay;
SET @HordePandarenMount4IconID               = @IconBlackDragonTurtle;

-- Spells
SET @HordePandarenRacials                    = @PandarenRacials;
SET @HordePandarenRacial1                    = @PandarenRacial1;
SET @HordePandarenRacial2                    = @PandarenRacial2;
SET @HordePandarenRacial3                    = @PandarenRacial3;
SET @HordePandarenRacial4                    = @PandarenRacial4;
SET @HordePandarenRacial5                    = @PandarenRacial5;

-- Strings
SET @HordePandarenClientPrefix               = 'Pa';
SET @HordePandarenClientString               = 'HordePandaren';
SET @HordePandarenFacialHairCustomization1   = 'NORMAL';
SET @HordePandarenFacialHairCustomization2   = 'EARRINGS';
SET @HordePandarenHairCustomization          = 'NORMAL';

-- Localization Strings
SET @HordePandarenenUS                       = 'Pandaren';
SET @HordePandarenkoKR                       = '';
SET @HordePandarenfrFR                       = '';
SET @HordePandarendeDE                       = '';
SET @HordePandarenzhCN                       = '';
SET @HordePandarenzhTW                       = '';
SET @HordePandarenesES                       = '';
SET @HordePandarenesMX                       = '';
SET @HordePandarenruRU                       = '';
SET @HordePandarenjaJP                       = '';
SET @HordePandarenptPT                       = '';
SET @HordePandarenitIT                       = '';
SET @HordePandarenUnk1                       = '';
SET @HordePandarenUnk2                       = '';
SET @HordePandarenUnk3                       = '';
SET @HordePandarenUnk4                       = '';

SET @HordePandarenFemaleenUS                 = '';
SET @HordePandarenFemalekoKR                 = '';
SET @HordePandarenFemalefrFR                 = '';
SET @HordePandarenFemaledeDE                 = '';
SET @HordePandarenFemalezhCN                 = '';
SET @HordePandarenFemalezhTW                 = '';
SET @HordePandarenFemaleesES                 = '';
SET @HordePandarenFemaleesMX                 = '';
SET @HordePandarenFemaleruRU                 = '';
SET @HordePandarenFemalejaJP                 = '';
SET @HordePandarenFemaleptPT                 = '';
SET @HordePandarenFemaleitIT                 = '';
SET @HordePandarenFemaleUnk1                 = '';
SET @HordePandarenFemaleUnk2                 = '';
SET @HordePandarenFemaleUnk3                 = '';
SET @HordePandarenFemaleUnk4                 = '';

SET @HordePandarenMaleenUS                   = '';
SET @HordePandarenMalekoKR                   = '';
SET @HordePandarenMalefrFR                   = '';
SET @HordePandarenMaledeDE                   = '';
SET @HordePandarenMalezhCN                   = '';
SET @HordePandarenMalezhTW                   = '';
SET @HordePandarenMaleesES                   = '';
SET @HordePandarenMaleesMX                   = '';
SET @HordePandarenMaleruRU                   = '';
SET @HordePandarenMalejaJP                   = '';
SET @HordePandarenMaleptPT                   = '';
SET @HordePandarenMaleitIT                   = '';
SET @HordePandarenMaleUnk1                   = '';
SET @HordePandarenMaleUnk2                   = '';
SET @HordePandarenMaleUnk3                   = '';
SET @HordePandarenMaleUnk4                   = '';

SET @HordePandarenRacialNameenUS             = 'Racial - Pandaren';
SET @HordePandarenRacialNamekoKR             = '';
SET @HordePandarenRacialNamefrFR             = '';
SET @HordePandarenRacialNamedeDE             = '';
SET @HordePandarenRacialNamezhCN             = '';
SET @HordePandarenRacialNamezhTW             = '';
SET @HordePandarenRacialNameesES             = '';
SET @HordePandarenRacialNameesMX             = '';
SET @HordePandarenRacialNameruRU             = '';
SET @HordePandarenRacialNamejaJP             = '';
SET @HordePandarenRacialNameptPT             = '';
SET @HordePandarenRacialNameitIT             = '';
SET @HordePandarenRacialNameUnk1             = '';
SET @HordePandarenRacialNameUnk2             = '';
SET @HordePandarenRacialNameUnk3             = '';
SET @HordePandarenRacialNameUnk4             = '';

SET @HordePandarenPlayerenUS                 = '"PLAYER"," Pandaren (Horde)"';
SET @HordePandarenPlayerkoKR                 = '';
SET @HordePandarenPlayerfrFR                 = '';
SET @HordePandarenPlayerdeDE                 = '';
SET @HordePandarenPlayerzhCN                 = '';
SET @HordePandarenPlayerzhTW                 = '';
SET @HordePandarenPlayeresES                 = '';
SET @HordePandarenPlayeresMX                 = '';
SET @HordePandarenPlayerruRU                 = '';
SET @HordePandarenPlayerjaJP                 = '';
SET @HordePandarenPlayerptPT                 = '';
SET @HordePandarenPlayeritIT                 = '';
SET @HordePandarenPlayerUnk1                 = '';
SET @HordePandarenPlayerUnk2                 = '';
SET @HordePandarenPlayerUnk3                 = '';
SET @HordePandarenPlayerUnk4                 = '';

SET @HordePandarenFactionNameenUS            = 'Huojin Pandaren';
SET @HordePandarenFactionNamekoKR            = '';
SET @HordePandarenFactionNamefrFR            = '';
SET @HordePandarenFactionNamedeDE            = '';
SET @HordePandarenFactionNamezhCN            = '';
SET @HordePandarenFactionNamezhTW            = '';
SET @HordePandarenFactionNameesES            = '';
SET @HordePandarenFactionNameesMX            = '';
SET @HordePandarenFactionNameruRU            = '';
SET @HordePandarenFactionNamejaJP            = '';
SET @HordePandarenFactionNameptPT            = '';
SET @HordePandarenFactionNameitIT            = '';
SET @HordePandarenFactionNameUnk1            = '';
SET @HordePandarenFactionNameUnk2            = '';
SET @HordePandarenFactionNameUnk3            = '';
SET @HordePandarenFactionNameUnk4            = '';

SET @HordePandarenFactionDescriptionenUS     = 'Led by the intrepid Ji Firepaw, the Huojin Pandaren are quick to act and quicker to fight for what they believe in.';
SET @HordePandarenFactionDescriptionkoKR     = '';
SET @HordePandarenFactionDescriptionfrFR     = '';
SET @HordePandarenFactionDescriptiondeDE     = '';
SET @HordePandarenFactionDescriptionzhCN     = '';
SET @HordePandarenFactionDescriptionzhTW     = '';
SET @HordePandarenFactionDescriptionesES     = '';
SET @HordePandarenFactionDescriptionesMX     = '';
SET @HordePandarenFactionDescriptionruRU     = '';
SET @HordePandarenFactionDescriptionjaJP     = '';
SET @HordePandarenFactionDescriptionptPT     = '';
SET @HordePandarenFactionDescriptionitIT     = '';
SET @HordePandarenFactionDescriptionUnk1     = '';
SET @HordePandarenFactionDescriptionUnk2     = '';
SET @HordePandarenFactionDescriptionUnk3     = '';
SET @HordePandarenFactionDescriptionUnk4     = '';

SET @HordePandarenAchievementenUS            = 'Realm First! Level 80 Pandaren (Horde)';
SET @HordePandarenAchievementkoKR            = '';
SET @HordePandarenAchievementfrFR            = '';
SET @HordePandarenAchievementdeDE            = '';
SET @HordePandarenAchievementzhCN            = '';
SET @HordePandarenAchievementzhTW            = '';
SET @HordePandarenAchievementesES            = '';
SET @HordePandarenAchievementesMX            = '';
SET @HordePandarenAchievementruRU            = '';
SET @HordePandarenAchievementjaJP            = '';
SET @HordePandarenAchievementptPT            = '';
SET @HordePandarenAchievementitIT            = '';
SET @HordePandarenAchievementUnk1            = '';
SET @HordePandarenAchievementUnk2            = '';
SET @HordePandarenAchievementUnk3            = '';
SET @HordePandarenAchievementUnk4            = '';

SET @HordePandarenAchievementDescriptionenUS = 'First (Horde) Pandaren on the realm to achieve level 80.';
SET @HordePandarenAchievementDescriptionkoKR = '';
SET @HordePandarenAchievementDescriptionfrFR = '';
SET @HordePandarenAchievementDescriptiondeDE = '';
SET @HordePandarenAchievementDescriptionzhCN = '';
SET @HordePandarenAchievementDescriptionzhTW = '';
SET @HordePandarenAchievementDescriptionesES = '';
SET @HordePandarenAchievementDescriptionesMX = '';
SET @HordePandarenAchievementDescriptionruRU = '';
SET @HordePandarenAchievementDescriptionjaJP = '';
SET @HordePandarenAchievementDescriptionptPT = '';
SET @HordePandarenAchievementDescriptionitIT = '';
SET @HordePandarenAchievementDescriptionUnk1 = '';
SET @HordePandarenAchievementDescriptionUnk2 = '';
SET @HordePandarenAchievementDescriptionUnk3 = '';
SET @HordePandarenAchievementDescriptionUnk4 = '';

-- Racial Mount
SET @HordePandarenMount1NameenUS                = 'Blue Dragon Turtle';
SET @HordePandarenMount1NamekoKR                = '';
SET @HordePandarenMount1NamefrFR                = '';
SET @HordePandarenMount1NamedeDE                = '';
SET @HordePandarenMount1NamezhCN                = '';
SET @HordePandarenMount1NamezhTW                = '';
SET @HordePandarenMount1NameesES                = '';
SET @HordePandarenMount1NameesMX                = '';
SET @HordePandarenMount1NameruRU                = '';
SET @HordePandarenMount1NamejaJP                = '';
SET @HordePandarenMount1NameptPT                = '';
SET @HordePandarenMount1NameitIT                = '';
SET @HordePandarenMount1NameUnk1                = '';
SET @HordePandarenMount1NameUnk2                = '';
SET @HordePandarenMount1NameUnk3                = '';
SET @HordePandarenMount1NameUnk4                = '';

SET @HordePandarenMount1SpellDescriptionenUS    = 'Summons and dismisses a rideable Blue Dragon Turtle.';
SET @HordePandarenMount1SpellDescriptionkoKR    = '';
SET @HordePandarenMount1SpellDescriptionfrFR    = '';
SET @HordePandarenMount1SpellDescriptiondeDE    = '';
SET @HordePandarenMount1SpellDescriptionzhCN    = '';
SET @HordePandarenMount1SpellDescriptionzhTW    = '';
SET @HordePandarenMount1SpellDescriptionesES    = '';
SET @HordePandarenMount1SpellDescriptionesMX    = '';
SET @HordePandarenMount1SpellDescriptionruRU    = '';
SET @HordePandarenMount1SpellDescriptionjaJP    = '';
SET @HordePandarenMount1SpellDescriptionptPT    = '';
SET @HordePandarenMount1SpellDescriptionitIT    = '';
SET @HordePandarenMount1SpellDescriptionUnk1    = '';
SET @HordePandarenMount1SpellDescriptionUnk2    = '';
SET @HordePandarenMount1SpellDescriptionUnk3    = '';
SET @HordePandarenMount1SpellDescriptionUnk4    = '';

SET @HordePandarenMount1ItemNameenUS          = 'Reins of the Blue Dragon Turtle';
SET @HordePandarenMount1ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Blue Dragon Turtle.';

SET @HordePandarenMount2NameenUS              = 'Purple Dragon Turtle';
SET @HordePandarenMount2NamekoKR              = '';
SET @HordePandarenMount2NamefrFR              = '';
SET @HordePandarenMount2NamedeDE              = '';
SET @HordePandarenMount2NamezhCN              = '';
SET @HordePandarenMount2NamezhTW              = '';
SET @HordePandarenMount2NameesES              = '';
SET @HordePandarenMount2NameesMX              = '';
SET @HordePandarenMount2NameruRU              = '';
SET @HordePandarenMount2NamejaJP              = '';
SET @HordePandarenMount2NameptPT              = '';
SET @HordePandarenMount2NameitIT              = '';
SET @HordePandarenMount2NameUnk1              = '';
SET @HordePandarenMount2NameUnk2              = '';
SET @HordePandarenMount2NameUnk3              = '';
SET @HordePandarenMount2NameUnk4              = '';

SET @HordePandarenMount2SpellDescriptionenUS  = 'Summons and dismisses a rideable Purple Dragon Turtle.';
SET @HordePandarenMount2SpellDescriptionkoKR  = '';
SET @HordePandarenMount2SpellDescriptionfrFR  = '';
SET @HordePandarenMount2SpellDescriptiondeDE  = '';
SET @HordePandarenMount2SpellDescriptionzhCN  = '';
SET @HordePandarenMount2SpellDescriptionzhTW  = '';
SET @HordePandarenMount2SpellDescriptionesES  = '';
SET @HordePandarenMount2SpellDescriptionesMX  = '';
SET @HordePandarenMount2SpellDescriptionruRU  = '';
SET @HordePandarenMount2SpellDescriptionjaJP  = '';
SET @HordePandarenMount2SpellDescriptionptPT  = '';
SET @HordePandarenMount2SpellDescriptionitIT  = '';
SET @HordePandarenMount2SpellDescriptionUnk1  = '';
SET @HordePandarenMount2SpellDescriptionUnk2  = '';
SET @HordePandarenMount2SpellDescriptionUnk3  = '';
SET @HordePandarenMount2SpellDescriptionUnk4  = '';

SET @HordePandarenMount2ItemNameenUS          = 'Reins of the Purple Dragon Turtle';
SET @HordePandarenMount2ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Purple Dragon Turtle.';

SET @HordePandarenMount3NameenUS              = 'Green Dragon Turtle';
SET @HordePandarenMount3NamekoKR              = '';
SET @HordePandarenMount3NamefrFR              = '';
SET @HordePandarenMount3NamedeDE              = '';
SET @HordePandarenMount3NamezhCN              = '';
SET @HordePandarenMount3NamezhTW              = '';
SET @HordePandarenMount3NameesES              = '';
SET @HordePandarenMount3NameesMX              = '';
SET @HordePandarenMount3NameruRU              = '';
SET @HordePandarenMount3NamejaJP              = '';
SET @HordePandarenMount3NameptPT              = '';
SET @HordePandarenMount3NameitIT              = '';
SET @HordePandarenMount3NameUnk1              = '';
SET @HordePandarenMount3NameUnk2              = '';
SET @HordePandarenMount3NameUnk3              = '';
SET @HordePandarenMount3NameUnk4              = '';

SET @HordePandarenMount3SpellDescriptionenUS  = 'Summons and dismisses a rideable Green Dragon Turtle.';
SET @HordePandarenMount3SpellDescriptionkoKR  = '';
SET @HordePandarenMount3SpellDescriptionfrFR  = '';
SET @HordePandarenMount3SpellDescriptiondeDE  = '';
SET @HordePandarenMount3SpellDescriptionzhCN  = '';
SET @HordePandarenMount3SpellDescriptionzhTW  = '';
SET @HordePandarenMount3SpellDescriptionesES  = '';
SET @HordePandarenMount3SpellDescriptionesMX  = '';
SET @HordePandarenMount3SpellDescriptionruRU  = '';
SET @HordePandarenMount3SpellDescriptionjaJP  = '';
SET @HordePandarenMount3SpellDescriptionptPT  = '';
SET @HordePandarenMount3SpellDescriptionitIT  = '';
SET @HordePandarenMount3SpellDescriptionUnk1  = '';
SET @HordePandarenMount3SpellDescriptionUnk2  = '';
SET @HordePandarenMount3SpellDescriptionUnk3  = '';
SET @HordePandarenMount3SpellDescriptionUnk4  = '';

SET @HordePandarenMount3ItemNameenUS          = 'Reins of the Green Dragon Turtle';
SET @HordePandarenMount3ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Green Dragon Turtle.';

SET @HordePandarenMount4NameenUS              = 'Black Dragon Turtle';
SET @HordePandarenMount4NamekoKR              = '';
SET @HordePandarenMount4NamefrFR              = '';
SET @HordePandarenMount4NamedeDE              = '';
SET @HordePandarenMount4NamezhCN              = '';
SET @HordePandarenMount4NamezhTW              = '';
SET @HordePandarenMount4NameesES              = '';
SET @HordePandarenMount4NameesMX              = '';
SET @HordePandarenMount4NameruRU              = '';
SET @HordePandarenMount4NamejaJP              = '';
SET @HordePandarenMount4NameptPT              = '';
SET @HordePandarenMount4NameitIT              = '';
SET @HordePandarenMount4NameUnk1              = '';
SET @HordePandarenMount4NameUnk2              = '';
SET @HordePandarenMount4NameUnk3              = '';
SET @HordePandarenMount4NameUnk4              = '';

SET @HordePandarenMount4SpellDescriptionenUS  = 'Summons and dismisses a rideable Black Dragon Turtle.';
SET @HordePandarenMount4SpellDescriptionkoKR  = '';
SET @HordePandarenMount4SpellDescriptionfrFR  = '';
SET @HordePandarenMount4SpellDescriptiondeDE  = '';
SET @HordePandarenMount4SpellDescriptionzhCN  = '';
SET @HordePandarenMount4SpellDescriptionzhTW  = '';
SET @HordePandarenMount4SpellDescriptionesES  = '';
SET @HordePandarenMount4SpellDescriptionesMX  = '';
SET @HordePandarenMount4SpellDescriptionruRU  = '';
SET @HordePandarenMount4SpellDescriptionjaJP  = '';
SET @HordePandarenMount4SpellDescriptionptPT  = '';
SET @HordePandarenMount4SpellDescriptionitIT  = '';
SET @HordePandarenMount4SpellDescriptionUnk1  = '';
SET @HordePandarenMount4SpellDescriptionUnk2  = '';
SET @HordePandarenMount4SpellDescriptionUnk3  = '';
SET @HordePandarenMount4SpellDescriptionUnk4  = '';

SET @HordePandarenMount4ItemNameenUS          = 'Reins of the Black Dragon Turtle';
SET @HordePandarenMount4ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Black Dragon Turtle.';
