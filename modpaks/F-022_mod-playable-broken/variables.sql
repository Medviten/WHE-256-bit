-- Race ID
SET @Broken := @NextRace := @NextRace +1;
SET @BrokenMask = 1 << (@Broken - 1);
SET @BrokenHelmetMask = 1 << @Broken;

-- Important variable update
SET @AllianceMask     = @AllianceMask    | @BrokenMask;
SET @PlayableRaceMask = @AllianceMask    | @HordeMask;
SET @CrossbowHunters  = @CrossbowHunters | @BrokenMask;
SET @BrokenAlliance   = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)

-- Miscellaneous
SET @BrokenExplorationSound = @DraeneiExplorationSound;
SET @BrokenCinematicSequence = @DraeneiCinematicSequence;

-- Strings
SET @BrokenClientPrefix = 'Br';
SET @BrokenClientString = 'Broken';

-- Localization Strings
SET @BrokenenUS                   = 'Broken';
SET @BrokenkoKR                   = '뒤틀린 드레나이';
SET @BrokenfrFR                   = 'Roué';
SET @BrokendeDE                   = 'Zerschlagener';
SET @BrokenzhCN                   = '破碎者';
SET @BrokenzhTW                   = '破碎者';
SET @BrokenesES                   = 'Tábido';
SET @BrokenesMX                   = 'Tábido';
SET @BrokenruRU                   = 'Падший';
SET @BrokenjaJP                   = '';
SET @BrokenptPT                   = '';
SET @BrokenitIT                   = '';

SET @BrokenFemaleenUS             = '';
SET @BrokenFemalekoKR             = '';
SET @BrokenFemalefrFR             = 'Rouée';
SET @BrokenFemaledeDE             = '';
SET @BrokenFemalezhCN             = '';
SET @BrokenFemalezhTW             = '';
SET @BrokenFemaleesES             = 'Tábida';
SET @BrokenFemaleesMX             = 'Tábida';
SET @BrokenFemaleruRU             = 'Падшая';
SET @BrokenFemalejaJP             = '';
SET @BrokenFemaleptPT             = '';
SET @BrokenFemaleitIT             = '';

SET @BrokenMaleenUS               = '';
SET @BrokenMalekoKR               = '';
SET @BrokenMalefrFR               = 'Roué';
SET @BrokenMaledeDE               = 'Zerschlagener';
SET @BrokenMalezhCN               = '';
SET @BrokenMalezhTW               = '';
SET @BrokenMaleesES               = 'Tábido';
SET @BrokenMaleesMX               = 'Tábido';
SET @BrokenMaleruRU               = 'Падший';
SET @BrokenMalejaJP               = '';
SET @BrokenMaleptPT               = '';
SET @BrokenMaleitIT               = '';

SET @BrokenRacialNameenUS         = 'Racial - Broken';
SET @BrokenRacialNamekoKR         = '';
SET @BrokenRacialNamefrFR         = '';
SET @BrokenRacialNamedeDE         = '';
SET @BrokenRacialNamezhCN         = '';
SET @BrokenRacialNamezhTW         = '';
SET @BrokenRacialNameesES         = '';
SET @BrokenRacialNameesMX         = '';
SET @BrokenRacialNameruRU         = '';
SET @BrokenRacialNamejaJP         = '';
SET @BrokenRacialNameptPT         = '';
SET @BrokenRacialNameitIT         = '';

SET @BrokenPlayerenUS             = '"PLAYER", " Broken"';
SET @BrokenPlayerkoKR             = '';
SET @BrokenPlayerfrFR             = '';
SET @BrokenPlayerdeDE             = '';
SET @BrokenPlayerzhCN             = '';
SET @BrokenPlayerzhTW             = '';
SET @BrokenPlayeresES             = '';
SET @BrokenPlayeresMX             = '';
SET @BrokenPlayerruRU             = '';
SET @BrokenPlayerjaJP             = '';
SET @BrokenPlayerptPT             = '';
SET @BrokenPlayeritIT             = '';

SET @BrokenFactionNameenUS        = 'Broken of the Alliance';
SET @BrokenFactionNamekoKR        = '';
SET @BrokenFactionNamefrFR        = '';
SET @BrokenFactionNamedeDE        = '';
SET @BrokenFactionNamezhCN        = '';
SET @BrokenFactionNamezhTW        = '';
SET @BrokenFactionNameesES        = '';
SET @BrokenFactionNameesMX        = '';
SET @BrokenFactionNameruRU        = '';
SET @BrokenFactionNamejaJP        = '';
SET @BrokenFactionNameptPT        = '';
SET @BrokenFactionNameitIT        = '';

SET @BrokenFactionDescriptionenUS = 'Broken who have joined the Alliance cause.';
SET @BrokenFactionDescriptionkoKR = '';
SET @BrokenFactionDescriptionfrFR = '';
SET @BrokenFactionDescriptiondeDE = '';
SET @BrokenFactionDescriptionzhCN = '';
SET @BrokenFactionDescriptionzhTW = '';
SET @BrokenFactionDescriptionesES = '';
SET @BrokenFactionDescriptionesMX = '';
SET @BrokenFactionDescriptionruRU = '';
SET @BrokenFactionDescriptionjaJP = '';
SET @BrokenFactionDescriptionptPT = '';
SET @BrokenFactionDescriptionitIT = '';
