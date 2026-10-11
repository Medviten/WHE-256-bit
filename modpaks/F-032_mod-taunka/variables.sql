-- Race ID
SET @Taunka := @NextRace := @NextRace +1;
SET @TaunkaMask = 1 << (@Taunka - 1);
SET @TaunkaHelmetMask = 1 << @Taunka;

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
