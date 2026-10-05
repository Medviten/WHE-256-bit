-- Race ID
SET @Naga := @NextRace := @NextRace +1;
SET @NagaMask = 1 << (@Naga - 1);
SET @NagaHelmetMask = 1 << @Naga;

-- Important variable update
SET @HordeMask = @HordeMask | @NagaMask;
SET @BarrensBros = @HordeMask & ~@UndercityMask;
SET @PlayableRaceMask = @AllianceMask | @HordeMask;

-- Miscellaneous
SET @NagaExplorationSound = @OrcExplorationSound;
SET @NagaCinematicSequence = @BloodElfCinematicSequence;

-- Strings
SET @NagaClientPrefix = 'Wo'; -- Copying Worgen
SET @NagaClientString = 'Naga';

-- Localization Strings
SET @NagaenUS                   = 'Naga';
SET @NagakoKR                   = '나가';
SET @NagafrFR                   = 'Naga';
SET @NagadeDE                   = 'Naga';
SET @NagazhCN                   = '纳迦';
SET @NagazhTW                   = '納迦';
SET @NagaesES                   = 'Naga';
SET @NagaesMX                   = 'Naga';
SET @NagaruRU                   = 'Нага';
SET @NagajaJP                   = '';
SET @NagaptPT                   = '';
SET @NagaitIT                   = '';

SET @NagaFemaleenUS             = '';
SET @NagaFemalekoKR             = '';
SET @NagaFemalefrFR             = 'Naga';
SET @NagaFemaledeDE             = '';
SET @NagaFemalezhCN             = '';
SET @NagaFemalezhTW             = '';
SET @NagaFemaleesES             = 'Naga';
SET @NagaFemaleesMX             = 'Naga';
SET @NagaFemaleruRU             = 'Нага';
SET @NagaFemalejaJP             = '';
SET @NagaFemaleptPT             = '';
SET @NagaFemaleitIT             = '';

SET @NagaMaleenUS               = '';
SET @NagaMalekoKR               = '';
SET @NagaMalefrFR               = 'Naga';
SET @NagaMaledeDE               = 'Naga';
SET @NagaMalezhCN               = '';
SET @NagaMalezhTW               = '';
SET @NagaMaleesES               = 'Naga';
SET @NagaMaleesMX               = 'Naga';
SET @NagaMaleruRU               = 'Наг';
SET @NagaMalejaJP               = '';
SET @NagaMaleptPT               = '';
SET @NagaMaleitIT               = '';

SET @NagaRacialNameenUS         = 'Racial - Naga';
SET @NagaRacialNamekoKR         = '';
SET @NagaRacialNamefrFR         = '';
SET @NagaRacialNamedeDE         = '';
SET @NagaRacialNamezhCN         = '';
SET @NagaRacialNamezhTW         = '';
SET @NagaRacialNameesES         = '';
SET @NagaRacialNameesMX         = '';
SET @NagaRacialNameruRU         = '';
SET @NagaRacialNamejaJP         = '';
SET @NagaRacialNameptPT         = '';
SET @NagaRacialNameitIT         = '';

SET @NagaPlayerenUS             = '"PLAYER", " Naga"';
SET @NagaPlayerkoKR             = '';
SET @NagaPlayerfrFR             = '';
SET @NagaPlayerdeDE             = '';
SET @NagaPlayerzhCN             = '';
SET @NagaPlayerzhTW             = '';
SET @NagaPlayeresES             = '';
SET @NagaPlayeresMX             = '';
SET @NagaPlayerruRU             = '';
SET @NagaPlayerjaJP             = '';
SET @NagaPlayerptPT             = '';
SET @NagaPlayeritIT             = '';

SET @NagaFactionNameenUS        = 'Naga of the Horde';
SET @NagaFactionNamekoKR        = '';
SET @NagaFactionNamefrFR        = '';
SET @NagaFactionNamedeDE        = '';
SET @NagaFactionNamezhCN        = '';
SET @NagaFactionNamezhTW        = '';
SET @NagaFactionNameesES        = '';
SET @NagaFactionNameesMX        = '';
SET @NagaFactionNameruRU        = '';
SET @NagaFactionNamejaJP        = '';
SET @NagaFactionNameptPT        = '';
SET @NagaFactionNameitIT        = '';

SET @NagaFactionDescriptionenUS = 'The naga of the Shimmering Expanse, chased from their native waters, have joined the Horde to survive.';
SET @NagaFactionDescriptionkoKR = '';
SET @NagaFactionDescriptionfrFR = '';
SET @NagaFactionDescriptiondeDE = '';
SET @NagaFactionDescriptionzhCN = '';
SET @NagaFactionDescriptionzhTW = '';
SET @NagaFactionDescriptionesES = '';
SET @NagaFactionDescriptionesMX = '';
SET @NagaFactionDescriptionruRU = '';
SET @NagaFactionDescriptionjaJP = '';
SET @NagaFactionDescriptionptPT = '';
SET @NagaFactionDescriptionitIT = '';
