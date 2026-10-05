-- Race ID
SET @HighmountainTauren := @NextRace := @NextRace +1;
SET @HighmountainTaurenMask = 1 << (@HighmountainTauren - 1);
SET @HighmountainTaurenHelmetMask = 1 << @HighmountainTauren;

-- Important variable update
SET @HordeMask = @HordeMask | @HighmountainTaurenMask;
SET @BarrensBros = @HordeMask & ~@UndercityMask;
SET @PlayableRaceMask = @AllianceMask | @HordeMask;

-- Miscellaneous
SET @HighmountainTaurenExplorationSound = @TaurenExplorationSound;
SET @HighmountainTaurenCinematicSequence = @TaurenCinematicSequence;

-- Strings
SET @HighmountainTaurenClientPrefix = 'Ta'; -- Copying Tauren
SET @HighmountainTaurenClientString = 'HighmountainTauren';

-- Localization Strings
SET @HighmountainTaurenenUS                   = 'Highmountain Tauren';
SET @HighmountainTaurenkoKR                   = '';
SET @HighmountainTaurenfrFR                   = '';
SET @HighmountainTaurendeDE                   = '';
SET @HighmountainTaurenzhCN                   = '';
SET @HighmountainTaurenzhTW                   = '';
SET @HighmountainTaurenesES                   = '';
SET @HighmountainTaurenesMX                   = '';
SET @HighmountainTaurenruRU                   = '';
SET @HighmountainTaurenjaJP                   = '';
SET @HighmountainTaurenptPT                   = '';
SET @HighmountainTaurenitIT                   = '';

SET @HighmountainTaurenFemaleenUS             = '';
SET @HighmountainTaurenFemalekoKR             = '';
SET @HighmountainTaurenFemalefrFR             = '';
SET @HighmountainTaurenFemaledeDE             = '';
SET @HighmountainTaurenFemalezhCN             = '';
SET @HighmountainTaurenFemalezhTW             = '';
SET @HighmountainTaurenFemaleesES             = '';
SET @HighmountainTaurenFemaleesMX             = '';
SET @HighmountainTaurenFemaleruRU             = '';
SET @HighmountainTaurenFemalejaJP             = '';
SET @HighmountainTaurenFemaleptPT             = '';
SET @HighmountainTaurenFemaleitIT             = '';

SET @HighmountainTaurenMaleenUS               = '';
SET @HighmountainTaurenMalekoKR               = '';
SET @HighmountainTaurenMalefrFR               = '';
SET @HighmountainTaurenMaledeDE               = '';
SET @HighmountainTaurenMalezhCN               = '';
SET @HighmountainTaurenMalezhTW               = '';
SET @HighmountainTaurenMaleesES               = '';
SET @HighmountainTaurenMaleesMX               = '';
SET @HighmountainTaurenMaleruRU               = '';
SET @HighmountainTaurenMalejaJP               = '';
SET @HighmountainTaurenMaleptPT               = '';
SET @HighmountainTaurenMaleitIT               = '';

SET @HighmountainTaurenRacialNameenUS         = 'Racial - Highmountain Tauren';
SET @HighmountainTaurenRacialNamekoKR         = '';
SET @HighmountainTaurenRacialNamefrFR         = '';
SET @HighmountainTaurenRacialNamedeDE         = '';
SET @HighmountainTaurenRacialNamezhCN         = '';
SET @HighmountainTaurenRacialNamezhTW         = '';
SET @HighmountainTaurenRacialNameesES         = '';
SET @HighmountainTaurenRacialNameesMX         = '';
SET @HighmountainTaurenRacialNameruRU         = '';
SET @HighmountainTaurenRacialNamejaJP         = '';
SET @HighmountainTaurenRacialNameptPT         = '';
SET @HighmountainTaurenRacialNameitIT         = '';

SET @HighmountainTaurenPlayerenUS             = '"PLAYER", " Highmountain Tauren"';
SET @HighmountainTaurenPlayerkoKR             = '';
SET @HighmountainTaurenPlayerfrFR             = '';
SET @HighmountainTaurenPlayerdeDE             = '';
SET @HighmountainTaurenPlayerzhCN             = '';
SET @HighmountainTaurenPlayerzhTW             = '';
SET @HighmountainTaurenPlayeresES             = '';
SET @HighmountainTaurenPlayeresMX             = '';
SET @HighmountainTaurenPlayerruRU             = '';
SET @HighmountainTaurenPlayerjaJP             = '';
SET @HighmountainTaurenPlayerptPT             = '';
SET @HighmountainTaurenPlayeritIT             = '';

SET @HighmountainTaurenFactionNameenUS        = 'Highmountain Tribe';
SET @HighmountainTaurenFactionNamekoKR        = '';
SET @HighmountainTaurenFactionNamefrFR        = '';
SET @HighmountainTaurenFactionNamedeDE        = '';
SET @HighmountainTaurenFactionNamezhCN        = '';
SET @HighmountainTaurenFactionNamezhTW        = '';
SET @HighmountainTaurenFactionNameesES        = '';
SET @HighmountainTaurenFactionNameesMX        = '';
SET @HighmountainTaurenFactionNameruRU        = '';
SET @HighmountainTaurenFactionNamejaJP        = '';
SET @HighmountainTaurenFactionNameptPT        = '';
SET @HighmountainTaurenFactionNameitIT        = '';

SET @HighmountainTaurenFactionDescriptionenUS = 'The Highmountain Tribe has dwindled in numbers over the years, and with the drogbar threat looming, seek new allies to save their homeland.';
SET @HighmountainTaurenFactionDescriptionkoKR = '';
SET @HighmountainTaurenFactionDescriptionfrFR = '';
SET @HighmountainTaurenFactionDescriptiondeDE = '';
SET @HighmountainTaurenFactionDescriptionzhCN = '';
SET @HighmountainTaurenFactionDescriptionzhTW = '';
SET @HighmountainTaurenFactionDescriptionesES = '';
SET @HighmountainTaurenFactionDescriptionesMX = '';
SET @HighmountainTaurenFactionDescriptionruRU = '';
SET @HighmountainTaurenFactionDescriptionjaJP = '';
SET @HighmountainTaurenFactionDescriptionptPT = '';
SET @HighmountainTaurenFactionDescriptionitIT = '';
