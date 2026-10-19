-- Race masks (race IDs are fixed in config.sql)
SET @NightborneMask                        = 1 << (@Nightborne - 1);       -- race ID 27 → 67108864
SET @NightborneHelmetMask                  = 1 << @Nightborne;             -- race ID 27 → 134217728

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                             = @HordeMask    | @NightborneMask;
SET @BarrensBros                           = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                      = @AllianceMask | @HordeMask;
SET @BowHunters                            = @BowHunters   | @NightborneMask;
SET @NightborneLanguage                    = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @NightborneAlliance                    = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @NightborneKnowThyEnemy                = @KnowThyEnemyHorde;

-- Miscellaneous
SET @NightborneExplorationSound            = @BloodElfExplorationSound;
SET @NightborneCinematicSequence           = @BloodElfCinematicSequence;
SET @NightborneBlood                       = 1;
SET @NightborneMaleModelPath               = 'Character\\Nightborne\\male\\NightborneMale.M2';
SET @NightborneFemaleModelPath             = 'Character\\Nightborne\\female\\NightborneFemale.M2';
SET @NightborneMaleFootprint               = @FootprintShoe;
SET @NightborneFemaleFootprint             = @FootprintShoe;

-- Mounts (IDs are global, see config.sql)
SET @NightborneMount1                        = @SpellNightborneManasaber;
SET @NightborneMount1Model                   = @NightborneManasaberModel;
SET @NightborneMount1Display                 = @NightborneManasaberDisplay;
SET @NightborneMount1CreatureID              = @NightborneManasaberCreatureID;
SET @NightborneMount1Item                    = @NightborneManasaberItem;
SET @NightborneMount1ItemDisplay             = @NightborneManasaberItemDisplay;

-- Strings
SET @NightborneClientPrefix                = 'Be';
SET @NightborneClientString                = 'Nightborne';
SET @NightborneFacialHairCustomization1    = 'NORMAL';
SET @NightborneFacialHairCustomization2    = 'EARRINGS';
SET @NightborneHairCustomization           = 'NORMAL';

-- Localization Strings
SET @NightborneenUS                        = 'Nightborne';
SET @NightbornekoKR                        = '';
SET @NightbornefrFR                        = '';
SET @NightbornedeDE                        = '';
SET @NightbornezhCN                        = '';
SET @NightbornezhTW                        = '';
SET @NightborneesES                        = '';
SET @NightborneesMX                        = '';
SET @NightborneruRU                        = '';
SET @NightbornejaJP                        = '';
SET @NightborneptPT                        = '';
SET @NightborneitIT                        = '';
SET @NightborneUnk1                        = '';
SET @NightborneUnk2                        = '';
SET @NightborneUnk3                        = '';
SET @NightborneUnk4                        = '';

SET @NightborneFemaleenUS                  = '';
SET @NightborneFemalekoKR                  = '';
SET @NightborneFemalefrFR                  = '';
SET @NightborneFemaledeDE                  = '';
SET @NightborneFemalezhCN                  = '';
SET @NightborneFemalezhTW                  = '';
SET @NightborneFemaleesES                  = '';
SET @NightborneFemaleesMX                  = '';
SET @NightborneFemaleruRU                  = '';
SET @NightborneFemalejaJP                  = '';
SET @NightborneFemaleptPT                  = '';
SET @NightborneFemaleitIT                  = '';
SET @NightborneFemaleUnk1                  = '';
SET @NightborneFemaleUnk2                  = '';
SET @NightborneFemaleUnk3                  = '';
SET @NightborneFemaleUnk4                  = '';

SET @NightborneMaleenUS                    = '';
SET @NightborneMalekoKR                    = '';
SET @NightborneMalefrFR                    = '';
SET @NightborneMaledeDE                    = '';
SET @NightborneMalezhCN                    = '';
SET @NightborneMalezhTW                    = '';
SET @NightborneMaleesES                    = '';
SET @NightborneMaleesMX                    = '';
SET @NightborneMaleruRU                    = '';
SET @NightborneMalejaJP                    = '';
SET @NightborneMaleptPT                    = '';
SET @NightborneMaleitIT                    = '';
SET @NightborneMaleUnk1                    = '';
SET @NightborneMaleUnk2                    = '';
SET @NightborneMaleUnk3                    = '';
SET @NightborneMaleUnk4                    = '';

SET @NightborneRacialNameenUS              = 'Racial - Nightborne';
SET @NightborneRacialNamekoKR              = '';
SET @NightborneRacialNamefrFR              = '';
SET @NightborneRacialNamedeDE              = '';
SET @NightborneRacialNamezhCN              = '';
SET @NightborneRacialNamezhTW              = '';
SET @NightborneRacialNameesES              = '';
SET @NightborneRacialNameesMX              = '';
SET @NightborneRacialNameruRU              = '';
SET @NightborneRacialNamejaJP              = '';
SET @NightborneRacialNameptPT              = '';
SET @NightborneRacialNameitIT              = '';
SET @NightborneRacialNameUnk1              = '';
SET @NightborneRacialNameUnk2              = '';
SET @NightborneRacialNameUnk3              = '';
SET @NightborneRacialNameUnk4              = '';

SET @NightbornePlayerenUS                  = '"PLAYER"," Nightborne"';
SET @NightbornePlayerkoKR                  = '';
SET @NightbornePlayerfrFR                  = '';
SET @NightbornePlayerdeDE                  = '';
SET @NightbornePlayerzhCN                  = '';
SET @NightbornePlayerzhTW                  = '';
SET @NightbornePlayeresES                  = '';
SET @NightbornePlayeresMX                  = '';
SET @NightbornePlayerruRU                  = '';
SET @NightbornePlayerjaJP                  = '';
SET @NightbornePlayerptPT                  = '';
SET @NightbornePlayeritIT                  = '';
SET @NightbornePlayerUnk1                  = '';
SET @NightbornePlayerUnk2                  = '';
SET @NightbornePlayerUnk3                  = '';
SET @NightbornePlayerUnk4                  = '';

SET @NightborneFactionNameenUS             = 'Suramar';
SET @NightborneFactionNamekoKR             = '';
SET @NightborneFactionNamefrFR             = '';
SET @NightborneFactionNamedeDE             = '';
SET @NightborneFactionNamezhCN             = '';
SET @NightborneFactionNamezhTW             = '';
SET @NightborneFactionNameesES             = '';
SET @NightborneFactionNameesMX             = '';
SET @NightborneFactionNameruRU             = '';
SET @NightborneFactionNamejaJP             = '';
SET @NightborneFactionNameptPT             = '';
SET @NightborneFactionNameitIT             = '';
SET @NightborneFactionNameUnk1             = '';
SET @NightborneFactionNameUnk2             = '';
SET @NightborneFactionNameUnk3             = '';
SET @NightborneFactionNameUnk4             = '';

SET @NightborneFactionDescriptionenUS      = 'Capital of the Nightborne';
SET @NightborneFactionDescriptionkoKR      = '';
SET @NightborneFactionDescriptionfrFR      = '';
SET @NightborneFactionDescriptiondeDE      = '';
SET @NightborneFactionDescriptionzhCN      = '';
SET @NightborneFactionDescriptionzhTW      = '';
SET @NightborneFactionDescriptionesES      = '';
SET @NightborneFactionDescriptionesMX      = '';
SET @NightborneFactionDescriptionruRU      = '';
SET @NightborneFactionDescriptionjaJP      = '';
SET @NightborneFactionDescriptionptPT      = '';
SET @NightborneFactionDescriptionitIT      = '';
SET @NightborneFactionDescriptionUnk1      = '';
SET @NightborneFactionDescriptionUnk2      = '';
SET @NightborneFactionDescriptionUnk3      = '';
SET @NightborneFactionDescriptionUnk4      = '';

SET @NightborneAchievementenUS             = 'Realm First! Level 80 Nightborne';
SET @NightborneAchievementkoKR             = '';
SET @NightborneAchievementfrFR             = '';
SET @NightborneAchievementdeDE             = '';
SET @NightborneAchievementzhCN             = '';
SET @NightborneAchievementzhTW             = '';
SET @NightborneAchievementesES             = '';
SET @NightborneAchievementesMX             = '';
SET @NightborneAchievementruRU             = '';
SET @NightborneAchievementjaJP             = '';
SET @NightborneAchievementptPT             = '';
SET @NightborneAchievementitIT             = '';
SET @NightborneAchievementUnk1             = '';
SET @NightborneAchievementUnk2             = '';
SET @NightborneAchievementUnk3             = '';
SET @NightborneAchievementUnk4             = '';

SET @NightborneAchievementDescriptionenUS  = 'First Nightborne on the realm to achieve level 80.';
SET @NightborneAchievementDescriptionkoKR  = '';
SET @NightborneAchievementDescriptionfrFR  = '';
SET @NightborneAchievementDescriptiondeDE  = '';
SET @NightborneAchievementDescriptionzhCN  = '';
SET @NightborneAchievementDescriptionzhTW  = '';
SET @NightborneAchievementDescriptionesES  = '';
SET @NightborneAchievementDescriptionesMX  = '';
SET @NightborneAchievementDescriptionruRU  = '';
SET @NightborneAchievementDescriptionjaJP  = '';
SET @NightborneAchievementDescriptionptPT  = '';
SET @NightborneAchievementDescriptionitIT  = '';
SET @NightborneAchievementDescriptionUnk1  = '';
SET @NightborneAchievementDescriptionUnk2  = '';
SET @NightborneAchievementDescriptionUnk3  = '';
SET @NightborneAchievementDescriptionUnk4  = '';

-- Racial Mount Strings 
SET @NightborneMount1NameenUS              = 'Nightborne Manasaber';
SET @NightborneMount1NamekoKR              = '';
SET @NightborneMount1NamefrFR              = '';
SET @NightborneMount1NamedeDE              = '';
SET @NightborneMount1NamezhCN              = '';
SET @NightborneMount1NamezhTW              = '';
SET @NightborneMount1NameesES              = '';
SET @NightborneMount1NameesMX              = '';
SET @NightborneMount1NameruRU              = '';
SET @NightborneMount1NamejaJP              = '';
SET @NightborneMount1NameptPT              = '';
SET @NightborneMount1NameitIT              = '';
SET @NightborneMount1NameUnk1              = '';
SET @NightborneMount1NameUnk2              = '';
SET @NightborneMount1NameUnk3              = '';
SET @NightborneMount1NameUnk4              = '';

SET @NightborneMount1SpellDescriptionenUS  = 'Summons and dismisses a rideable Nightborne Manasaber.';
SET @NightborneMount1SpellDescriptionkoKR  = '';
SET @NightborneMount1SpellDescriptionfrFR  = '';
SET @NightborneMount1SpellDescriptiondeDE  = '';
SET @NightborneMount1SpellDescriptionzhCN  = '';
SET @NightborneMount1SpellDescriptionzhTW  = '';
SET @NightborneMount1SpellDescriptionesES  = '';
SET @NightborneMount1SpellDescriptionesMX  = '';
SET @NightborneMount1SpellDescriptionruRU  = '';
SET @NightborneMount1SpellDescriptionjaJP  = '';
SET @NightborneMount1SpellDescriptionptPT  = '';
SET @NightborneMount1SpellDescriptionitIT  = '';
SET @NightborneMount1SpellDescriptionUnk1  = '';
SET @NightborneMount1SpellDescriptionUnk2  = '';
SET @NightborneMount1SpellDescriptionUnk3  = '';
SET @NightborneMount1SpellDescriptionUnk4  = '';

SET @NightborneMount1ItemNameenUS          = @NightborneMount1NameenUS;
SET @NightborneMount1ItemDescriptionenUS   = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Nightborne Manasaber.\n\n"Born capable of sniffing out concentrations of arcane energy, this noble cat was presented with thanks to a proven ally of the nightborne."';
