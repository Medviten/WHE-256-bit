-- Race masks (race IDs are fixed in config.sql)
SET @VulperaMask                        = 1 << (@Vulpera - 1);       -- race ID 35 → 17179869184
SET @VulperaHelmetMask                  = 1 << @Vulpera;             -- race ID 35 → 34359738368

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

-- Mounts (IDs are global, see config.sql)
SET @VulperaMount1                           = @SpellCaravanHyena;
SET @VulperaMount1Model                      = @CaravanHyenaModel;
SET @VulperaMount1Display                    = @CaravanHyenaDisplay;
SET @VulperaMount1CreatureID                 = @CaravanHyenaCreatureID;
SET @VulperaMount1Item                       = @CaravanHyenaItem;
SET @VulperaMount1ItemDisplay                = @CaravanHyenaItemDisplay;
SET @VulperaMount1IconID                     = @IconCaravanHyena;

SET @VulperaMount2                           = @SpellCaravanHyenaNoCanopy;
SET @VulperaMount2Model                      = @CaravanHyenaNoCanopyModel;
SET @VulperaMount2Display                    = @CaravanHyenaNoCanopyDisplay;
SET @VulperaMount2CreatureID                 = @CaravanHyenaNoCanopyCreatureID;
SET @VulperaMount2Item                       = @CaravanHyenaNoCanopyItem;
SET @VulperaMount2ItemDisplay                = @CaravanHyenaNoCanopyItemDisplay;
SET @VulperaMount2IconID                     = @IconCaravanHyena;

-- Strings
SET @VulperaClientPrefix                = 'Vu';
SET @VulperaClientString                = 'Vulpera';
SET @VulperaFacialHairCustomization1    = 'NORMAL';
SET @VulperaFacialHairCustomization2    = 'EARRINGS';
SET @VulperaHairCustomization           = 'NORMAL';

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
SET @VulperaUnk1                        = '';
SET @VulperaUnk2                        = '';
SET @VulperaUnk3                        = '';
SET @VulperaUnk4                        = '';

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
SET @VulperaFemaleUnk1                  = '';
SET @VulperaFemaleUnk2                  = '';
SET @VulperaFemaleUnk3                  = '';
SET @VulperaFemaleUnk4                  = '';

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
SET @VulperaMaleUnk1                    = '';
SET @VulperaMaleUnk2                    = '';
SET @VulperaMaleUnk3                    = '';
SET @VulperaMaleUnk4                    = '';

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
SET @VulperaRacialNameUnk1              = '';
SET @VulperaRacialNameUnk2              = '';
SET @VulperaRacialNameUnk3              = '';
SET @VulperaRacialNameUnk4              = '';

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
SET @VulperaPlayerUnk1                  = '';
SET @VulperaPlayerUnk2                  = '';
SET @VulperaPlayerUnk3                  = '';
SET @VulperaPlayerUnk4                  = '';

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
SET @VulperaFactionNameUnk1             = '';
SET @VulperaFactionNameUnk2             = '';
SET @VulperaFactionNameUnk3             = '';
SET @VulperaFactionNameUnk4             = '';

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
SET @VulperaFactionDescriptionUnk1      = '';
SET @VulperaFactionDescriptionUnk2      = '';
SET @VulperaFactionDescriptionUnk3      = '';
SET @VulperaFactionDescriptionUnk4      = '';

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
SET @VulperaAchievementUnk1             = '';
SET @VulperaAchievementUnk2             = '';
SET @VulperaAchievementUnk3             = '';
SET @VulperaAchievementUnk4             = '';

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
SET @VulperaAchievementDescriptionUnk1  = '';
SET @VulperaAchievementDescriptionUnk2  = '';
SET @VulperaAchievementDescriptionUnk3  = '';
SET @VulperaAchievementDescriptionUnk4  = '';

-- Racial Mount Strings 
SET @VulperaMount1NameenUS              = 'Caravan Hyena with Canopy';
SET @VulperaMount1NamekoKR              = '';
SET @VulperaMount1NamefrFR              = '';
SET @VulperaMount1NamedeDE              = '';
SET @VulperaMount1NamezhCN              = '';
SET @VulperaMount1NamezhTW              = '';
SET @VulperaMount1NameesES              = '';
SET @VulperaMount1NameesMX              = '';
SET @VulperaMount1NameruRU              = '';
SET @VulperaMount1NamejaJP              = '';
SET @VulperaMount1NameptPT              = '';
SET @VulperaMount1NameitIT              = '';
SET @VulperaMount1NameUnk1              = '';
SET @VulperaMount1NameUnk2              = '';
SET @VulperaMount1NameUnk3              = '';
SET @VulperaMount1NameUnk4              = '';

SET @VulperaMount1SpellDescriptionenUS  = 'Summons and dismisses a rideable Caravan Hyena with a canopy.';
SET @VulperaMount1SpellDescriptionkoKR  = '';
SET @VulperaMount1SpellDescriptionfrFR  = '';
SET @VulperaMount1SpellDescriptiondeDE  = '';
SET @VulperaMount1SpellDescriptionzhCN  = '';
SET @VulperaMount1SpellDescriptionzhTW  = '';
SET @VulperaMount1SpellDescriptionesES  = '';
SET @VulperaMount1SpellDescriptionesMX  = '';
SET @VulperaMount1SpellDescriptionruRU  = '';
SET @VulperaMount1SpellDescriptionjaJP  = '';
SET @VulperaMount1SpellDescriptionptPT  = '';
SET @VulperaMount1SpellDescriptionitIT  = '';
SET @VulperaMount1SpellDescriptionUnk1  = '';
SET @VulperaMount1SpellDescriptionUnk2  = '';
SET @VulperaMount1SpellDescriptionUnk3  = '';
SET @VulperaMount1SpellDescriptionUnk4  = '';

SET @VulperaMount1ItemNameenUS          = @VulperaMount1NameenUS;
SET @VulperaMount1ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Caravan Hyena with a canopy.';

SET @VulperaMount2NameenUS              = 'Caravan Hyena without Canopy';
SET @VulperaMount2NamekoKR              = '';
SET @VulperaMount2NamefrFR              = '';
SET @VulperaMount2NamedeDE              = '';
SET @VulperaMount2NamezhCN              = '';
SET @VulperaMount2NamezhTW              = '';
SET @VulperaMount2NameesES              = '';
SET @VulperaMount2NameesMX              = '';
SET @VulperaMount2NameruRU              = '';
SET @VulperaMount2NamejaJP              = '';
SET @VulperaMount2NameptPT              = '';
SET @VulperaMount2NameitIT              = '';
SET @VulperaMount2NameUnk1              = '';
SET @VulperaMount2NameUnk2              = '';
SET @VulperaMount2NameUnk3              = '';
SET @VulperaMount2NameUnk4              = '';

SET @VulperaMount2SpellDescriptionenUS  = 'Summons and dismisses a rideable Caravan Hyena without a canopy.';
SET @VulperaMount2SpellDescriptionkoKR  = '';
SET @VulperaMount2SpellDescriptionfrFR  = '';
SET @VulperaMount2SpellDescriptiondeDE  = '';
SET @VulperaMount2SpellDescriptionzhCN  = '';
SET @VulperaMount2SpellDescriptionzhTW  = '';
SET @VulperaMount2SpellDescriptionesES  = '';
SET @VulperaMount2SpellDescriptionesMX  = '';
SET @VulperaMount2SpellDescriptionruRU  = '';
SET @VulperaMount2SpellDescriptionjaJP  = '';
SET @VulperaMount2SpellDescriptionptPT  = '';
SET @VulperaMount2SpellDescriptionitIT  = '';
SET @VulperaMount2SpellDescriptionUnk1  = '';
SET @VulperaMount2SpellDescriptionUnk2  = '';
SET @VulperaMount2SpellDescriptionUnk3  = '';
SET @VulperaMount2SpellDescriptionUnk4  = '';

SET @VulperaMount2ItemNameenUS          = @VulperaMount2NameenUS;
SET @VulperaMount2ItemDescriptionenUS   = 'Teaches you how to summon this mount. Summons and dismisses a rideable Caravan Hyena without a canopy.';
