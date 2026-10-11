-- Race ID
SET @Nightborne                           := @NextRace := @NextRace +1; -- default: 18
SET @NightborneMask                        = 1 << (@Nightborne - 1);       -- race ID 18 → 131072
SET @NightborneHelmetMask                  = 1 << @Nightborne;             -- race ID 18 → 262144

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

-- Racial Mount Strings 
SET @NightborneManasaberNameenUS              = 'Nightborne Manasaber';
SET @NightborneManasaberNamekoKR              = '';
SET @NightborneManasaberNamefrFR              = '';
SET @NightborneManasaberNamedeDE              = '';
SET @NightborneManasaberNamezhCN              = '';
SET @NightborneManasaberNamezhTW              = '';
SET @NightborneManasaberNameesES              = '';
SET @NightborneManasaberNameesMX              = '';
SET @NightborneManasaberNameruRU              = '';
SET @NightborneManasaberNamejaJP              = '';
SET @NightborneManasaberNameptPT              = '';
SET @NightborneManasaberNameitIT              = '';

SET @NightborneManasaberSpellDescriptionenUS  = 'Summons and dismisses a rideable Nightborne Manasaber.';
SET @NightborneManasaberSpellDescriptionkoKR  = '';
SET @NightborneManasaberSpellDescriptionfrFR  = '';
SET @NightborneManasaberSpellDescriptiondeDE  = '';
SET @NightborneManasaberSpellDescriptionzhCN  = '';
SET @NightborneManasaberSpellDescriptionzhTW  = '';
SET @NightborneManasaberSpellDescriptionesES  = '';
SET @NightborneManasaberSpellDescriptionesMX  = '';
SET @NightborneManasaberSpellDescriptionruRU  = '';
SET @NightborneManasaberSpellDescriptionjaJP  = '';
SET @NightborneManasaberSpellDescriptionptPT  = '';
SET @NightborneManasaberSpellDescriptionitIT  = '';

SET @NightborneManasaberItemNameenUS          = @NightborneManasaberNameenUS;
SET @NightborneManasaberItemDescriptionenUS   = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Nightborne Manasaber.\n\n"Born capable of sniffing out concentrations of arcane energy, this noble cat was presented with thanks to a proven ally of the nightborne."';
