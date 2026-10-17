-- Race ID
SET @Naga                          := @NextRace := @NextRace +1;
SET @NagaMask                       = 1 << (@Naga - 1);
SET @NagaHelmetMask                 = 1 << @Naga;

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                      = @HordeMask | @NagaMask;
SET @BarrensBros                    = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask               = @AllianceMask | @HordeMask;
SET @BowHunters                     = @BowHunters   | @NagaMask;
SET @NagaLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @NagaAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @NagaKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @NagaExplorationSound           = @OrcExplorationSound;
SET @NagaCinematicSequence          = @BloodElfCinematicSequence;
SET @NagaBlood                      = 1;
SET @NagaMaleModelPath              = 'Character\\NagaPC\\male\\NagaPC_male.mdx';
SET @NagaFemaleModelPath            = 'Character\\NagaPC\\female\\NagaPC_Female.mdx';
SET @NagaMaleFootprint              = @FootprintShoe;
SET @NagaFemaleFootprint            = @FootprintShoe;

-- Strings
SET @NagaClientPrefix               = 'Wo'; -- Copying Worgen
SET @NagaClientString               = 'Naga';
SET @NagaFacialHairCustomization1   = 'TENTS';
SET @NagaFacialHairCustomization2   = 'TENTS_PIERCINGS';
SET @NagaHairCustomization          = 'NORMAL';

-- Localization Strings
SET @NagaenUS                       = 'Naga';
SET @NagakoKR                       = '나가';
SET @NagafrFR                       = 'Naga';
SET @NagadeDE                       = 'Naga';
SET @NagazhCN                       = '纳迦';
SET @NagazhTW                       = '納迦';
SET @NagaesES                       = 'Naga';
SET @NagaesMX                       = 'Naga';
SET @NagaruRU                       = 'Нага';
SET @NagajaJP                       = '';
SET @NagaptPT                       = '';
SET @NagaitIT                       = '';
SET @NagaUnk1                       = '';
SET @NagaUnk2                       = '';
SET @NagaUnk3                       = '';
SET @NagaUnk4                       = '';

SET @NagaFemaleenUS                 = '';
SET @NagaFemalekoKR                 = '';
SET @NagaFemalefrFR                 = 'Naga';
SET @NagaFemaledeDE                 = '';
SET @NagaFemalezhCN                 = '';
SET @NagaFemalezhTW                 = '';
SET @NagaFemaleesES                 = 'Naga';
SET @NagaFemaleesMX                 = 'Naga';
SET @NagaFemaleruRU                 = 'Нага';
SET @NagaFemalejaJP                 = '';
SET @NagaFemaleptPT                 = '';
SET @NagaFemaleitIT                 = '';
SET @NagaFemaleUnk1                 = '';
SET @NagaFemaleUnk2                 = '';
SET @NagaFemaleUnk3                 = '';
SET @NagaFemaleUnk4                 = '';

SET @NagaMaleenUS                   = '';
SET @NagaMalekoKR                   = '';
SET @NagaMalefrFR                   = 'Naga';
SET @NagaMaledeDE                   = 'Naga';
SET @NagaMalezhCN                   = '';
SET @NagaMalezhTW                   = '';
SET @NagaMaleesES                   = 'Naga';
SET @NagaMaleesMX                   = 'Naga';
SET @NagaMaleruRU                   = 'Наг';
SET @NagaMalejaJP                   = '';
SET @NagaMaleptPT                   = '';
SET @NagaMaleitIT                   = '';
SET @NagaMaleUnk1                   = '';
SET @NagaMaleUnk2                   = '';
SET @NagaMaleUnk3                   = '';
SET @NagaMaleUnk4                   = '';

SET @NagaRacialNameenUS             = 'Racial - Naga';
SET @NagaRacialNamekoKR             = '';
SET @NagaRacialNamefrFR             = '';
SET @NagaRacialNamedeDE             = '';
SET @NagaRacialNamezhCN             = '';
SET @NagaRacialNamezhTW             = '';
SET @NagaRacialNameesES             = '';
SET @NagaRacialNameesMX             = '';
SET @NagaRacialNameruRU             = '';
SET @NagaRacialNamejaJP             = '';
SET @NagaRacialNameptPT             = '';
SET @NagaRacialNameitIT             = '';
SET @NagaRacialNameUnk1             = '';
SET @NagaRacialNameUnk2             = '';
SET @NagaRacialNameUnk3             = '';
SET @NagaRacialNameUnk4             = '';

SET @NagaPlayerenUS                 = '"PLAYER", " Naga"';
SET @NagaPlayerkoKR                 = '';
SET @NagaPlayerfrFR                 = '';
SET @NagaPlayerdeDE                 = '';
SET @NagaPlayerzhCN                 = '';
SET @NagaPlayerzhTW                 = '';
SET @NagaPlayeresES                 = '';
SET @NagaPlayeresMX                 = '';
SET @NagaPlayerruRU                 = '';
SET @NagaPlayerjaJP                 = '';
SET @NagaPlayerptPT                 = '';
SET @NagaPlayeritIT                 = '';
SET @NagaPlayerUnk1                 = '';
SET @NagaPlayerUnk2                 = '';
SET @NagaPlayerUnk3                 = '';
SET @NagaPlayerUnk4                 = '';

SET @NagaFactionNameenUS            = 'Naga of the Horde';
SET @NagaFactionNamekoKR            = '';
SET @NagaFactionNamefrFR            = '';
SET @NagaFactionNamedeDE            = '';
SET @NagaFactionNamezhCN            = '';
SET @NagaFactionNamezhTW            = '';
SET @NagaFactionNameesES            = '';
SET @NagaFactionNameesMX            = '';
SET @NagaFactionNameruRU            = '';
SET @NagaFactionNamejaJP            = '';
SET @NagaFactionNameptPT            = '';
SET @NagaFactionNameitIT            = '';
SET @NagaFactionNameUnk1            = '';
SET @NagaFactionNameUnk2            = '';
SET @NagaFactionNameUnk3            = '';
SET @NagaFactionNameUnk4            = '';

SET @NagaFactionDescriptionenUS     = 'The naga of the Shimmering Expanse, chased from their native waters, have joined the Horde to survive.';
SET @NagaFactionDescriptionkoKR     = '';
SET @NagaFactionDescriptionfrFR     = '';
SET @NagaFactionDescriptiondeDE     = '';
SET @NagaFactionDescriptionzhCN     = '';
SET @NagaFactionDescriptionzhTW     = '';
SET @NagaFactionDescriptionesES     = '';
SET @NagaFactionDescriptionesMX     = '';
SET @NagaFactionDescriptionruRU     = '';
SET @NagaFactionDescriptionjaJP     = '';
SET @NagaFactionDescriptionptPT     = '';
SET @NagaFactionDescriptionitIT     = '';
SET @NagaFactionDescriptionUnk1     = '';
SET @NagaFactionDescriptionUnk2     = '';
SET @NagaFactionDescriptionUnk3     = '';
SET @NagaFactionDescriptionUnk4     = '';

SET @NagaAchievementenUS            = 'Realm First! Level 80 Naga';
SET @NagaAchievementkoKR            = '';
SET @NagaAchievementfrFR            = '';
SET @NagaAchievementdeDE            = '';
SET @NagaAchievementzhCN            = '';
SET @NagaAchievementzhTW            = '';
SET @NagaAchievementesES            = '';
SET @NagaAchievementesMX            = '';
SET @NagaAchievementruRU            = '';
SET @NagaAchievementjaJP            = '';
SET @NagaAchievementptPT            = '';
SET @NagaAchievementitIT            = '';
SET @NagaAchievementUnk1            = '';
SET @NagaAchievementUnk2            = '';
SET @NagaAchievementUnk3            = '';
SET @NagaAchievementUnk4            = '';

SET @NagaAchievementDescriptionenUS = 'First Naga on the realm to achieve level 80.';
SET @NagaAchievementDescriptionkoKR = '';
SET @NagaAchievementDescriptionfrFR = '';
SET @NagaAchievementDescriptiondeDE = '';
SET @NagaAchievementDescriptionzhCN = '';
SET @NagaAchievementDescriptionzhTW = '';
SET @NagaAchievementDescriptionesES = '';
SET @NagaAchievementDescriptionesMX = '';
SET @NagaAchievementDescriptionruRU = '';
SET @NagaAchievementDescriptionjaJP = '';
SET @NagaAchievementDescriptionptPT = '';
SET @NagaAchievementDescriptionitIT = '';
SET @NagaAchievementDescriptionUnk1 = '';
SET @NagaAchievementDescriptionUnk2 = '';
SET @NagaAchievementDescriptionUnk3 = '';
SET @NagaAchievementDescriptionUnk4 = '';
