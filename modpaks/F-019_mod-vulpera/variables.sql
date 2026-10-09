-- Race ID
SET @Vulpera                           := @NextRace := @NextRace +1; -- default: 18
SET @VulperaMask                        = 1 << (@Vulpera - 1);       -- race ID 18 → 131072
SET @VulperaHelmetMask                  = 1 << @Vulpera;             -- race ID 18 → 262144

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                          = @HordeMask    | @VulperaMask;
SET @BarrensBros                        = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                   = @AllianceMask | @HordeMask;
SET @BowHunters                         = @BowHunters   | @VulperaMask;
SET @VulperaLanguage                    = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @VulperaAlliance                    = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @VulperaKnowThyEnemy                = @KnowThyEnemyHorde;

-- Miscellaneous
SET @VulperaExplorationSound            = @TaurenExplorationSound;
SET @VulperaCinematicSequence           = @TaurenCinematicSequence;
SET @VulperaBlood                       = 1;
SET @VulperaMaleModelPath               = 'Character\\Vulpera\\male\\VulperaMale.M2';
SET @VulperaFemaleModelPath             = 'Character\\Vulpera\\female\\VulperaFemale.M2';
SET @VulperaMaleFootprint               = @FootprintPaw;
SET @VulperaFemaleFootprint             = @FootprintPaw;

-- Strings
SET @VulperaClientPrefix                = 'Vu';
SET @VulperaClientString                = 'Vulpera';

-- Localization Strings
SET @VulperaenUS                        = 'Vulpera';
SET @VulperakoKR                        = '';
SET @VulperafrFR                        = '';
SET @VulperadeDE                        = '';
SET @VulperazhCN                        = '';
SET @VulperazhTW                        = '';
SET @VulperaesES                        = '';
SET @VulperaesMX                        = '';
SET @VulperaruRU                        = '';
SET @VulperajaJP                        = '';
SET @VulperaptPT                        = '';
SET @VulperaitIT                        = '';

SET @VulperaFemaleenUS                  = '';
SET @VulperaFemalekoKR                  = '';
SET @VulperaFemalefrFR                  = '';
SET @VulperaFemaledeDE                  = '';
SET @VulperaFemalezhCN                  = '';
SET @VulperaFemalezhTW                  = '';
SET @VulperaFemaleesES                  = '';
SET @VulperaFemaleesMX                  = '';
SET @VulperaFemaleruRU                  = '';
SET @VulperaFemalejaJP                  = '';
SET @VulperaFemaleptPT                  = '';
SET @VulperaFemaleitIT                  = '';

SET @VulperaMaleenUS                    = '';
SET @VulperaMalekoKR                    = '';
SET @VulperaMalefrFR                    = '';
SET @VulperaMaledeDE                    = '';
SET @VulperaMalezhCN                    = '';
SET @VulperaMalezhTW                    = '';
SET @VulperaMaleesES                    = '';
SET @VulperaMaleesMX                    = '';
SET @VulperaMaleruRU                    = '';
SET @VulperaMalejaJP                    = '';
SET @VulperaMaleptPT                    = '';
SET @VulperaMaleitIT                    = '';

SET @VulperaRacialNameenUS              = 'Racial - Vulpera';
SET @VulperaRacialNamekoKR              = '';
SET @VulperaRacialNamefrFR              = '';
SET @VulperaRacialNamedeDE              = '';
SET @VulperaRacialNamezhCN              = '';
SET @VulperaRacialNamezhTW              = '';
SET @VulperaRacialNameesES              = '';
SET @VulperaRacialNameesMX              = '';
SET @VulperaRacialNameruRU              = '';
SET @VulperaRacialNamejaJP              = '';
SET @VulperaRacialNameptPT              = '';
SET @VulperaRacialNameitIT              = '';

SET @VulperaPlayerenUS                  = '"PLAYER"," Vulpera"';
SET @VulperaPlayerkoKR                  = '';
SET @VulperaPlayerfrFR                  = '';
SET @VulperaPlayerdeDE                  = '';
SET @VulperaPlayerzhCN                  = '';
SET @VulperaPlayerzhTW                  = '';
SET @VulperaPlayeresES                  = '';
SET @VulperaPlayeresMX                  = '';
SET @VulperaPlayerruRU                  = '';
SET @VulperaPlayerjaJP                  = '';
SET @VulperaPlayerptPT                  = '';
SET @VulperaPlayeritIT                  = '';

SET @VulperaFactionNameenUS             = 'Voldunai';
SET @VulperaFactionNamekoKR             = '';
SET @VulperaFactionNamefrFR             = '';
SET @VulperaFactionNamedeDE             = '';
SET @VulperaFactionNamezhCN             = '';
SET @VulperaFactionNamezhTW             = '';
SET @VulperaFactionNameesES             = '';
SET @VulperaFactionNameesMX             = '';
SET @VulperaFactionNameruRU             = '';
SET @VulperaFactionNamejaJP             = '';
SET @VulperaFactionNameptPT             = '';
SET @VulperaFactionNameitIT             = '';

SET @VulperaFactionDescriptionenUS      = 'Comprised of exiles and scavengers, the Voldunai use their knowledge of the sands to thrive where others would wither and die.';
SET @VulperaFactionDescriptionkoKR      = '';
SET @VulperaFactionDescriptionfrFR      = '';
SET @VulperaFactionDescriptiondeDE      = '';
SET @VulperaFactionDescriptionzhCN      = '';
SET @VulperaFactionDescriptionzhTW      = '';
SET @VulperaFactionDescriptionesES      = '';
SET @VulperaFactionDescriptionesMX      = '';
SET @VulperaFactionDescriptionruRU      = '';
SET @VulperaFactionDescriptionjaJP      = '';
SET @VulperaFactionDescriptionptPT      = '';
SET @VulperaFactionDescriptionitIT      = '';

SET @VulperaAchievementenUS             = 'Realm First! Level 80 Vulpera';
SET @VulperaAchievementkoKR             = '';
SET @VulperaAchievementfrFR             = '';
SET @VulperaAchievementdeDE             = '';
SET @VulperaAchievementzhCN             = '';
SET @VulperaAchievementzhTW             = '';
SET @VulperaAchievementesES             = '';
SET @VulperaAchievementesMX             = '';
SET @VulperaAchievementruRU             = '';
SET @VulperaAchievementjaJP             = '';
SET @VulperaAchievementptPT             = '';
SET @VulperaAchievementitIT             = '';

SET @VulperaAchievementDescriptionenUS  = 'First Vulpera on the realm to achieve level 80.';
SET @VulperaAchievementDescriptionkoKR  = '';
SET @VulperaAchievementDescriptionfrFR  = '';
SET @VulperaAchievementDescriptiondeDE  = '';
SET @VulperaAchievementDescriptionzhCN  = '';
SET @VulperaAchievementDescriptionzhTW  = '';
SET @VulperaAchievementDescriptionesES  = '';
SET @VulperaAchievementDescriptionesMX  = '';
SET @VulperaAchievementDescriptionruRU  = '';
SET @VulperaAchievementDescriptionjaJP  = '';
SET @VulperaAchievementDescriptionptPT  = '';
SET @VulperaAchievementDescriptionitIT  = '';

-- Racial Mount Strings 
SET @CaravanHyena1NameenUS              = 'Caravan Hyena with Canopy';
SET @CaravanHyena1NamekoKR              = '';
SET @CaravanHyena1NamefrFR              = '';
SET @CaravanHyena1NamedeDE              = '';
SET @CaravanHyena1NamezhCN              = '';
SET @CaravanHyena1NamezhTW              = '';
SET @CaravanHyena1NameesES              = '';
SET @CaravanHyena1NameesMX              = '';
SET @CaravanHyena1NameruRU              = '';
SET @CaravanHyena1NamejaJP              = '';
SET @CaravanHyena1NameptPT              = '';
SET @CaravanHyena1NameitIT              = '';

SET @CaravanHyena1SpellDescriptionenUS  = 'Summons and dismisses a rideable Caravan Hyena with a canopy.';
SET @CaravanHyena1SpellDescriptionkoKR  = '';
SET @CaravanHyena1SpellDescriptionfrFR  = '';
SET @CaravanHyena1SpellDescriptiondeDE  = '';
SET @CaravanHyena1SpellDescriptionzhCN  = '';
SET @CaravanHyena1SpellDescriptionzhTW  = '';
SET @CaravanHyena1SpellDescriptionesES  = '';
SET @CaravanHyena1SpellDescriptionesMX  = '';
SET @CaravanHyena1SpellDescriptionruRU  = '';
SET @CaravanHyena1SpellDescriptionjaJP  = '';
SET @CaravanHyena1SpellDescriptionptPT  = '';
SET @CaravanHyena1SpellDescriptionitIT  = '';

SET @CaravanHyena1ItemNameenUS          = @CaravanHyena1NameenUS;
SET @CaravanHyena1ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Caravan Hyena with a canopy.';

SET @CaravanHyena2NameenUS              = 'Caravan Hyena without Canopy';
SET @CaravanHyena2NamekoKR              = '';
SET @CaravanHyena2NamefrFR              = '';
SET @CaravanHyena2NamedeDE              = '';
SET @CaravanHyena2NamezhCN              = '';
SET @CaravanHyena2NamezhTW              = '';
SET @CaravanHyena2NameesES              = '';
SET @CaravanHyena2NameesMX              = '';
SET @CaravanHyena2NameruRU              = '';
SET @CaravanHyena2NamejaJP              = '';
SET @CaravanHyena2NameptPT              = '';
SET @CaravanHyena2NameitIT              = '';

SET @CaravanHyena2SpellDescriptionenUS  = 'Summons and dismisses a rideable Caravan Hyena without a canopy.';
SET @CaravanHyena2SpellDescriptionkoKR  = '';
SET @CaravanHyena2SpellDescriptionfrFR  = '';
SET @CaravanHyena2SpellDescriptiondeDE  = '';
SET @CaravanHyena2SpellDescriptionzhCN  = '';
SET @CaravanHyena2SpellDescriptionzhTW  = '';
SET @CaravanHyena2SpellDescriptionesES  = '';
SET @CaravanHyena2SpellDescriptionesMX  = '';
SET @CaravanHyena2SpellDescriptionruRU  = '';
SET @CaravanHyena2SpellDescriptionjaJP  = '';
SET @CaravanHyena2SpellDescriptionptPT  = '';
SET @CaravanHyena2SpellDescriptionitIT  = '';

SET @CaravanHyena2ItemNameenUS          = @CaravanHyena2NameenUS;
SET @CaravanHyena2ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Caravan Hyena without a canopy.';
