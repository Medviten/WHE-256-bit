-- Race ID
SET @HighmountainTauren                          := @NextRace := @NextRace +1;
SET @HighmountainTaurenMask                       = 1 << (@HighmountainTauren - 1);
SET @HighmountainTaurenHelmetMask                 = 1 << @HighmountainTauren;

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

-- Strings
SET @HighmountainTaurenClientPrefix               = 'Ta'; -- Copying Tauren
SET @HighmountainTaurenClientString               = 'HighmountainTauren';

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

-- Racial Mount Strings 
SET @HighmountainThunderhoofNameenUS              = 'Highmountain Thunderhoof';
SET @HighmountainThunderhoofNamekoKR              = '';
SET @HighmountainThunderhoofNamefrFR              = '';
SET @HighmountainThunderhoofNamedeDE              = '';
SET @HighmountainThunderhoofNamezhCN              = '';
SET @HighmountainThunderhoofNamezhTW              = '';
SET @HighmountainThunderhoofNameesES              = '';
SET @HighmountainThunderhoofNameesMX              = '';
SET @HighmountainThunderhoofNameruRU              = '';
SET @HighmountainThunderhoofNamejaJP              = '';
SET @HighmountainThunderhoofNameptPT              = '';
SET @HighmountainThunderhoofNameitIT              = '';

SET @HighmountainThunderhoofSpellDescriptionenUS  = 'Summons and dismisses your Highmountain Thunderhoof.';
SET @HighmountainThunderhoofSpellDescriptionkoKR  = '';
SET @HighmountainThunderhoofSpellDescriptionfrFR  = '';
SET @HighmountainThunderhoofSpellDescriptiondeDE  = '';
SET @HighmountainThunderhoofSpellDescriptionzhCN  = '';
SET @HighmountainThunderhoofSpellDescriptionzhTW  = '';
SET @HighmountainThunderhoofSpellDescriptionesES  = '';
SET @HighmountainThunderhoofSpellDescriptionesMX  = '';
SET @HighmountainThunderhoofSpellDescriptionruRU  = '';
SET @HighmountainThunderhoofSpellDescriptionjaJP  = '';
SET @HighmountainThunderhoofSpellDescriptionptPT  = '';
SET @HighmountainThunderhoofSpellDescriptionitIT  = '';

SET @HighmountainThunderhoofItemNameenUS          = @HighmountainThunderhoofNameenUS;
SET @HighmountainThunderhoofItemDescriptionenUS   = 'Summons and dismisses your Highmountain Thunderhoof.\n\n"A gift from the tauren who trained this sure-footed highland moose to safely traverse the paths and peaks of Highmountain."';
