-- Race masks (race IDs are fixed in config.sql)
SET @TaunkaMask = 1 << (@Taunka - 1); -- race ID 19 → 262144
SET @TaunkaHelmetMask = 1 << @Taunka; -- race ID 19 → 524288

-- Important variable update
SET @HordeMask = @HordeMask | @TaunkaMask;
SET @BarrensBros = @HordeMask & ~@UndercityMask;
SET @PlayableRaceMask = @AllianceMask | @HordeMask;

-- Miscellaneous
SET @TaunkaExplorationSound = @TaurenExplorationSound;
SET @TaunkaCinematicSequence = @TaurenCinematicSequence;

-- Strings
SET @TaunkaClientPrefix = 'Ta'; -- Copying Tauren
SET @TaunkaClientString = 'Taunka';

-- Localization Strings
SET @TaunkaenUS                   = 'Taunka';
SET @TaunkakoKR                   = '';
SET @TaunkafrFR                   = '';
SET @TaunkadeDE                   = '';
SET @TaunkazhCN                   = '';
SET @TaunkazhTW                   = '';
SET @TaunkaesES                   = '';
SET @TaunkaesMX                   = '';
SET @TaunkaruRU                   = '';
SET @TaunkajaJP                   = '';
SET @TaunkaptPT                   = '';
SET @TaunkaitIT                   = '';
SET @TaunkaUnk1                   = '';
SET @TaunkaUnk2                   = '';
SET @TaunkaUnk3                   = '';
SET @TaunkaUnk4                   = '';

SET @TaunkaFemaleenUS             = '';
SET @TaunkaFemalekoKR             = '';
SET @TaunkaFemalefrFR             = '';
SET @TaunkaFemaledeDE             = '';
SET @TaunkaFemalezhCN             = '';
SET @TaunkaFemalezhTW             = '';
SET @TaunkaFemaleesES             = '';
SET @TaunkaFemaleesMX             = '';
SET @TaunkaFemaleruRU             = '';
SET @TaunkaFemalejaJP             = '';
SET @TaunkaFemaleptPT             = '';
SET @TaunkaFemaleitIT             = '';
SET @TaunkaFemaleUnk1             = '';
SET @TaunkaFemaleUnk2             = '';
SET @TaunkaFemaleUnk3             = '';
SET @TaunkaFemaleUnk4             = '';

SET @TaunkaMaleenUS               = '';
SET @TaunkaMalekoKR               = '';
SET @TaunkaMalefrFR               = '';
SET @TaunkaMaledeDE               = '';
SET @TaunkaMalezhCN               = '';
SET @TaunkaMalezhTW               = '';
SET @TaunkaMaleesES               = '';
SET @TaunkaMaleesMX               = '';
SET @TaunkaMaleruRU               = '';
SET @TaunkaMalejaJP               = '';
SET @TaunkaMaleptPT               = '';
SET @TaunkaMaleitIT               = '';
SET @TaunkaMaleUnk1               = '';
SET @TaunkaMaleUnk2               = '';
SET @TaunkaMaleUnk3               = '';
SET @TaunkaMaleUnk4               = '';

SET @TaunkaRacialNameenUS         = 'Racial - Taunka';
SET @TaunkaRacialNamekoKR         = '';
SET @TaunkaRacialNamefrFR         = '';
SET @TaunkaRacialNamedeDE         = '';
SET @TaunkaRacialNamezhCN         = '';
SET @TaunkaRacialNamezhTW         = '';
SET @TaunkaRacialNameesES         = '';
SET @TaunkaRacialNameesMX         = '';
SET @TaunkaRacialNameruRU         = '';
SET @TaunkaRacialNamejaJP         = '';
SET @TaunkaRacialNameptPT         = '';
SET @TaunkaRacialNameitIT         = '';
SET @TaunkaRacialNameUnk1         = '';
SET @TaunkaRacialNameUnk2         = '';
SET @TaunkaRacialNameUnk3         = '';
SET @TaunkaRacialNameUnk4         = '';

SET @TaunkaPlayerenUS             = '"PLAYER", " Taunka"';
SET @TaunkaPlayerkoKR             = '';
SET @TaunkaPlayerfrFR             = '';
SET @TaunkaPlayerdeDE             = '';
SET @TaunkaPlayerzhCN             = '';
SET @TaunkaPlayerzhTW             = '';
SET @TaunkaPlayeresES             = '';
SET @TaunkaPlayeresMX             = '';
SET @TaunkaPlayerruRU             = '';
SET @TaunkaPlayerjaJP             = '';
SET @TaunkaPlayerptPT             = '';
SET @TaunkaPlayeritIT             = '';
SET @TaunkaPlayerUnk1             = '';
SET @TaunkaPlayerUnk2             = '';
SET @TaunkaPlayerUnk3             = '';
SET @TaunkaPlayerUnk4             = '';

SET @TaunkaFactionNameenUS        = 'Taunka of the Horde';
SET @TaunkaFactionNamekoKR        = '';
SET @TaunkaFactionNamefrFR        = '';
SET @TaunkaFactionNamedeDE        = '';
SET @TaunkaFactionNamezhCN        = '';
SET @TaunkaFactionNamezhTW        = '';
SET @TaunkaFactionNameesES        = '';
SET @TaunkaFactionNameesMX        = '';
SET @TaunkaFactionNameruRU        = '';
SET @TaunkaFactionNamejaJP        = '';
SET @TaunkaFactionNameptPT        = '';
SET @TaunkaFactionNameitIT        = '';
SET @TaunkaFactionNameUnk1        = '';
SET @TaunkaFactionNameUnk2        = '';
SET @TaunkaFactionNameUnk3        = '';
SET @TaunkaFactionNameUnk4        = '';

SET @TaunkaFactionDescriptionenUS = 'Some of the most adventurous Taunka have joined their plains-dwelling cousins in the Horde.';
SET @TaunkaFactionDescriptionkoKR = '';
SET @TaunkaFactionDescriptionfrFR = '';
SET @TaunkaFactionDescriptiondeDE = '';
SET @TaunkaFactionDescriptionzhCN = '';
SET @TaunkaFactionDescriptionzhTW = '';
SET @TaunkaFactionDescriptionesES = '';
SET @TaunkaFactionDescriptionesMX = '';
SET @TaunkaFactionDescriptionruRU = '';
SET @TaunkaFactionDescriptionjaJP = '';
SET @TaunkaFactionDescriptionptPT = '';
SET @TaunkaFactionDescriptionitIT = '';
SET @TaunkaFactionDescriptionUnk1 = '';
SET @TaunkaFactionDescriptionUnk2 = '';
SET @TaunkaFactionDescriptionUnk3 = '';
SET @TaunkaFactionDescriptionUnk4 = '';
