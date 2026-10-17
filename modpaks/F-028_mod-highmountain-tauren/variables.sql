-- Race masks (race IDs are fixed in config.sql)
SET @HighmountainTaurenMask                       = 1 << (@HighmountainTauren - 1); -- race ID 28 → 134217728
SET @HighmountainTaurenHelmetMask                 = 1 << @HighmountainTauren; -- race ID 28 → 268435456

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                                    = @HordeMask | @HighmountainTaurenMask;
SET @BarrensBros                                  = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                             = @AllianceMask | @HordeMask;
SET @HighmountainTaurenLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @HighmountainTaurenAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @HighmountainTaurenKnowThyEnemy               = @KnowThyEnemyHorde;
SET @HighmountainTaurenKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @HighmountainTaurenExplorationSound           = @TaurenExplorationSound;
SET @HighmountainTaurenCinematicSequence          = @TaurenCinematicSequence;
SET @HighmountainTaurenBlood                      = 1;
SET @HighmountainTaurenMaleModelPath              = 'Character\\HighmountainTauren\\male\\HighmountainTaurenMale.M2';
SET @HighmountainTaurenFemaleModelPath            = 'Character\\HighmountainTauren\\female\\HighmountainTaurenFemale.M2';
SET @HighmountainTaurenMaleFootprint              = @FootprintHoof;
SET @HighmountainTaurenFemaleFootprint            = @FootprintHoof;

-- Mounts (IDs are global, see config.sql)
SET @HighmountainTaurenMount1                = @SpellHighmountainThunderhoof;
SET @HighmountainTaurenMount1Model           = @HighmountainThunderhoofModel;
SET @HighmountainTaurenMount1Display         = @HighmountainThunderhoofDisplay;
SET @HighmountainTaurenMount1CreatureID      = @HighmountainThunderhoofCreatureID;
SET @HighmountainTaurenMount1Item            = @HighmountainThunderhoofItem;
SET @HighmountainTaurenMount1ItemDisplay     = @HighmountainThunderhoofItemDisplay;
SET @HighmountainTaurenMount1IconID          = @IconHighmountainThunderhoof;

-- Strings
SET @HighmountainTaurenClientPrefix               = 'Ta'; -- Copying Tauren
SET @HighmountainTaurenClientString               = 'HighmountainTauren';
SET @HighmountainTaurenFacialHairCustomization1   = 'NORMAL';
SET @HighmountainTaurenFacialHairCustomization2   = 'HAIR';
SET @HighmountainTaurenHairCustomization          = 'HORNS';

-- Localization Strings
SET @HighmountainTaurenenUS                       = 'Highmountain Tauren';
SET @HighmountainTaurenkoKR                       = '';
SET @HighmountainTaurenfrFR                       = '';
SET @HighmountainTaurendeDE                       = '';
SET @HighmountainTaurenzhCN                       = '';
SET @HighmountainTaurenzhTW                       = '';
SET @HighmountainTaurenesES                       = '';
SET @HighmountainTaurenesMX                       = '';
SET @HighmountainTaurenruRU                       = '';
SET @HighmountainTaurenjaJP                       = '';
SET @HighmountainTaurenptPT                       = '';
SET @HighmountainTaurenitIT                       = '';
SET @HighmountainTaurenUnk1                       = '';
SET @HighmountainTaurenUnk2                       = '';
SET @HighmountainTaurenUnk3                       = '';
SET @HighmountainTaurenUnk4                       = '';

SET @HighmountainTaurenFemaleenUS                 = '';
SET @HighmountainTaurenFemalekoKR                 = '';
SET @HighmountainTaurenFemalefrFR                 = '';
SET @HighmountainTaurenFemaledeDE                 = '';
SET @HighmountainTaurenFemalezhCN                 = '';
SET @HighmountainTaurenFemalezhTW                 = '';
SET @HighmountainTaurenFemaleesES                 = '';
SET @HighmountainTaurenFemaleesMX                 = '';
SET @HighmountainTaurenFemaleruRU                 = '';
SET @HighmountainTaurenFemalejaJP                 = '';
SET @HighmountainTaurenFemaleptPT                 = '';
SET @HighmountainTaurenFemaleitIT                 = '';
SET @HighmountainTaurenFemaleUnk1                 = '';
SET @HighmountainTaurenFemaleUnk2                 = '';
SET @HighmountainTaurenFemaleUnk3                 = '';
SET @HighmountainTaurenFemaleUnk4                 = '';

SET @HighmountainTaurenMaleenUS                   = '';
SET @HighmountainTaurenMalekoKR                   = '';
SET @HighmountainTaurenMalefrFR                   = '';
SET @HighmountainTaurenMaledeDE                   = '';
SET @HighmountainTaurenMalezhCN                   = '';
SET @HighmountainTaurenMalezhTW                   = '';
SET @HighmountainTaurenMaleesES                   = '';
SET @HighmountainTaurenMaleesMX                   = '';
SET @HighmountainTaurenMaleruRU                   = '';
SET @HighmountainTaurenMalejaJP                   = '';
SET @HighmountainTaurenMaleptPT                   = '';
SET @HighmountainTaurenMaleitIT                   = '';
SET @HighmountainTaurenMaleUnk1                   = '';
SET @HighmountainTaurenMaleUnk2                   = '';
SET @HighmountainTaurenMaleUnk3                   = '';
SET @HighmountainTaurenMaleUnk4                   = '';

SET @HighmountainTaurenRacialNameenUS             = 'Racial - Highmountain Tauren';
SET @HighmountainTaurenRacialNamekoKR             = '';
SET @HighmountainTaurenRacialNamefrFR             = '';
SET @HighmountainTaurenRacialNamedeDE             = '';
SET @HighmountainTaurenRacialNamezhCN             = '';
SET @HighmountainTaurenRacialNamezhTW             = '';
SET @HighmountainTaurenRacialNameesES             = '';
SET @HighmountainTaurenRacialNameesMX             = '';
SET @HighmountainTaurenRacialNameruRU             = '';
SET @HighmountainTaurenRacialNamejaJP             = '';
SET @HighmountainTaurenRacialNameptPT             = '';
SET @HighmountainTaurenRacialNameitIT             = '';
SET @HighmountainTaurenRacialNameUnk1             = '';
SET @HighmountainTaurenRacialNameUnk2             = '';
SET @HighmountainTaurenRacialNameUnk3             = '';
SET @HighmountainTaurenRacialNameUnk4             = '';

SET @HighmountainTaurenPlayerenUS                 = '"PLAYER", " Highmountain Tauren"';
SET @HighmountainTaurenPlayerkoKR                 = '';
SET @HighmountainTaurenPlayerfrFR                 = '';
SET @HighmountainTaurenPlayerdeDE                 = '';
SET @HighmountainTaurenPlayerzhCN                 = '';
SET @HighmountainTaurenPlayerzhTW                 = '';
SET @HighmountainTaurenPlayeresES                 = '';
SET @HighmountainTaurenPlayeresMX                 = '';
SET @HighmountainTaurenPlayerruRU                 = '';
SET @HighmountainTaurenPlayerjaJP                 = '';
SET @HighmountainTaurenPlayerptPT                 = '';
SET @HighmountainTaurenPlayeritIT                 = '';
SET @HighmountainTaurenPlayerUnk1                 = '';
SET @HighmountainTaurenPlayerUnk2                 = '';
SET @HighmountainTaurenPlayerUnk3                 = '';
SET @HighmountainTaurenPlayerUnk4                 = '';

SET @HighmountainTaurenFactionNameenUS            = 'Highmountain Tribe';
SET @HighmountainTaurenFactionNamekoKR            = '';
SET @HighmountainTaurenFactionNamefrFR            = '';
SET @HighmountainTaurenFactionNamedeDE            = '';
SET @HighmountainTaurenFactionNamezhCN            = '';
SET @HighmountainTaurenFactionNamezhTW            = '';
SET @HighmountainTaurenFactionNameesES            = '';
SET @HighmountainTaurenFactionNameesMX            = '';
SET @HighmountainTaurenFactionNameruRU            = '';
SET @HighmountainTaurenFactionNamejaJP            = '';
SET @HighmountainTaurenFactionNameptPT            = '';
SET @HighmountainTaurenFactionNameitIT            = '';
SET @HighmountainTaurenFactionNameUnk1            = '';
SET @HighmountainTaurenFactionNameUnk2            = '';
SET @HighmountainTaurenFactionNameUnk3            = '';
SET @HighmountainTaurenFactionNameUnk4            = '';

SET @HighmountainTaurenFactionDescriptionenUS     = 'The Highmountain Tribe has dwindled in numbers over the years, and with the drogbar threat looming, seek new allies to save their homeland.';
SET @HighmountainTaurenFactionDescriptionkoKR     = '';
SET @HighmountainTaurenFactionDescriptionfrFR     = '';
SET @HighmountainTaurenFactionDescriptiondeDE     = '';
SET @HighmountainTaurenFactionDescriptionzhCN     = '';
SET @HighmountainTaurenFactionDescriptionzhTW     = '';
SET @HighmountainTaurenFactionDescriptionesES     = '';
SET @HighmountainTaurenFactionDescriptionesMX     = '';
SET @HighmountainTaurenFactionDescriptionruRU     = '';
SET @HighmountainTaurenFactionDescriptionjaJP     = '';
SET @HighmountainTaurenFactionDescriptionptPT     = '';
SET @HighmountainTaurenFactionDescriptionitIT     = '';
SET @HighmountainTaurenFactionDescriptionUnk1     = '';
SET @HighmountainTaurenFactionDescriptionUnk2     = '';
SET @HighmountainTaurenFactionDescriptionUnk3     = '';
SET @HighmountainTaurenFactionDescriptionUnk4     = '';

SET @HighmountainTaurenAchievementenUS            = 'Realm First! Level 80 Highmountain Tauren';
SET @HighmountainTaurenAchievementkoKR            = '';
SET @HighmountainTaurenAchievementfrFR            = '';
SET @HighmountainTaurenAchievementdeDE            = '';
SET @HighmountainTaurenAchievementzhCN            = '';
SET @HighmountainTaurenAchievementzhTW            = '';
SET @HighmountainTaurenAchievementesES            = '';
SET @HighmountainTaurenAchievementesMX            = '';
SET @HighmountainTaurenAchievementruRU            = '';
SET @HighmountainTaurenAchievementjaJP            = '';
SET @HighmountainTaurenAchievementptPT            = '';
SET @HighmountainTaurenAchievementitIT            = '';
SET @HighmountainTaurenAchievementUnk1            = '';
SET @HighmountainTaurenAchievementUnk2            = '';
SET @HighmountainTaurenAchievementUnk3            = '';
SET @HighmountainTaurenAchievementUnk4            = '';

SET @HighmountainTaurenAchievementDescriptionenUS = 'First Highmountain Tauren on the realm to achieve level 80.';
SET @HighmountainTaurenAchievementDescriptionkoKR = '';
SET @HighmountainTaurenAchievementDescriptionfrFR = '';
SET @HighmountainTaurenAchievementDescriptiondeDE = '';
SET @HighmountainTaurenAchievementDescriptionzhCN = '';
SET @HighmountainTaurenAchievementDescriptionzhTW = '';
SET @HighmountainTaurenAchievementDescriptionesES = '';
SET @HighmountainTaurenAchievementDescriptionesMX = '';
SET @HighmountainTaurenAchievementDescriptionruRU = '';
SET @HighmountainTaurenAchievementDescriptionjaJP = '';
SET @HighmountainTaurenAchievementDescriptionptPT = '';
SET @HighmountainTaurenAchievementDescriptionitIT = '';
SET @HighmountainTaurenAchievementDescriptionUnk1 = '';
SET @HighmountainTaurenAchievementDescriptionUnk2 = '';
SET @HighmountainTaurenAchievementDescriptionUnk3 = '';
SET @HighmountainTaurenAchievementDescriptionUnk4 = '';

-- Racial Mount Strings 
SET @HighmountainTaurenMount1NameenUS              = 'Highmountain Thunderhoof';
SET @HighmountainTaurenMount1NamekoKR              = '';
SET @HighmountainTaurenMount1NamefrFR              = '';
SET @HighmountainTaurenMount1NamedeDE              = '';
SET @HighmountainTaurenMount1NamezhCN              = '';
SET @HighmountainTaurenMount1NamezhTW              = '';
SET @HighmountainTaurenMount1NameesES              = '';
SET @HighmountainTaurenMount1NameesMX              = '';
SET @HighmountainTaurenMount1NameruRU              = '';
SET @HighmountainTaurenMount1NamejaJP              = '';
SET @HighmountainTaurenMount1NameptPT              = '';
SET @HighmountainTaurenMount1NameitIT              = '';
SET @HighmountainTaurenMount1NameUnk1              = '';
SET @HighmountainTaurenMount1NameUnk2              = '';
SET @HighmountainTaurenMount1NameUnk3              = '';
SET @HighmountainTaurenMount1NameUnk4              = '';

SET @HighmountainTaurenMount1SpellDescriptionenUS  = 'Summons and dismisses your Highmountain Thunderhoof.';
SET @HighmountainTaurenMount1SpellDescriptionkoKR  = '';
SET @HighmountainTaurenMount1SpellDescriptionfrFR  = '';
SET @HighmountainTaurenMount1SpellDescriptiondeDE  = '';
SET @HighmountainTaurenMount1SpellDescriptionzhCN  = '';
SET @HighmountainTaurenMount1SpellDescriptionzhTW  = '';
SET @HighmountainTaurenMount1SpellDescriptionesES  = '';
SET @HighmountainTaurenMount1SpellDescriptionesMX  = '';
SET @HighmountainTaurenMount1SpellDescriptionruRU  = '';
SET @HighmountainTaurenMount1SpellDescriptionjaJP  = '';
SET @HighmountainTaurenMount1SpellDescriptionptPT  = '';
SET @HighmountainTaurenMount1SpellDescriptionitIT  = '';
SET @HighmountainTaurenMount1SpellDescriptionUnk1  = '';
SET @HighmountainTaurenMount1SpellDescriptionUnk2  = '';
SET @HighmountainTaurenMount1SpellDescriptionUnk3  = '';
SET @HighmountainTaurenMount1SpellDescriptionUnk4  = '';

SET @HighmountainTaurenMount1ItemNameenUS          = @HighmountainTaurenMount1NameenUS;
SET @HighmountainTaurenMount1ItemDescriptionenUS   = 'Teaches you how to summon this mount.\n\nSummons and dismisses your Highmountain Thunderhoof.\n\n"A gift from the tauren who trained this sure-footed highland moose to safely traverse the paths and peaks of Highmountain."';
