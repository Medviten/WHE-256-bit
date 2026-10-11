-- Race ID
SET @LightforgedDraenei                                := @NextRace := @NextRace +1;
SET @LightforgedDraeneiMask                            = 1 << (@LightforgedDraenei - 1);
SET @LightforgedDraeneiHelmetMask                      = 1 << @LightforgedDraenei;

-- Important variable update
SET @AllianceMask                          = @AllianceMask     | @LightforgedDraeneiMask;
SET @PlayableRaceMask                      = @PlayableRaceMask | @LightforgedDraeneiMask;
SET @CrossbowHunters                       = @CrossbowHunters  | @LightforgedDraeneiMask;

-- Miscellaneous
SET @LightforgedDraeneiExplorationSound                = @DraeneiExplorationSound;
SET @LightforgedDraeneiCinematicSequence               = @DraeneiCinematicSequence;

-- Strings
SET @LightforgedDraeneiClientPrefix = 'Dr'; -- Copying Draenei
SET @LightforgedDraeneiClientString = 'LightforgedDraenei';

-- Localization Strings
SET @LightforgedDraeneienUS                   = 'Lightforged Draenei';
SET @LightforgedDraeneikoKR                   = '';
SET @LightforgedDraeneifrFR                   = '';
SET @LightforgedDraeneideDE                   = '';
SET @LightforgedDraeneizhCN                   = '';
SET @LightforgedDraeneizhTW                   = '';
SET @LightforgedDraeneiesES                   = '';
SET @LightforgedDraeneiesMX                   = '';
SET @LightforgedDraeneiruRU                   = '';
SET @LightforgedDraeneijaJP                   = '';
SET @LightforgedDraeneiptPT                   = '';
SET @LightforgedDraeneiitIT                   = '';

SET @LightforgedDraeneiFemaleenUS             = '';
SET @LightforgedDraeneiFemalekoKR             = '';
SET @LightforgedDraeneiFemalefrFR             = '';
SET @LightforgedDraeneiFemaledeDE             = '';
SET @LightforgedDraeneiFemalezhCN             = '';
SET @LightforgedDraeneiFemalezhTW             = '';
SET @LightforgedDraeneiFemaleesES             = '';
SET @LightforgedDraeneiFemaleesMX             = '';
SET @LightforgedDraeneiFemaleruRU             = '';
SET @LightforgedDraeneiFemalejaJP             = '';
SET @LightforgedDraeneiFemaleptPT             = '';
SET @LightforgedDraeneiFemaleitIT             = '';

SET @LightforgedDraeneiMaleenUS               = '';
SET @LightforgedDraeneiMalekoKR               = '';
SET @LightforgedDraeneiMalefrFR               = '';
SET @LightforgedDraeneiMaledeDE               = '';
SET @LightforgedDraeneiMalezhCN               = '';
SET @LightforgedDraeneiMalezhTW               = '';
SET @LightforgedDraeneiMaleesES               = '';
SET @LightforgedDraeneiMaleesMX               = '';
SET @LightforgedDraeneiMaleruRU               = '';
SET @LightforgedDraeneiMalejaJP               = '';
SET @LightforgedDraeneiMaleptPT               = '';
SET @LightforgedDraeneiMaleitIT               = '';

SET @LightforgedDraeneiRacialNameenUS         = 'Racial - Lightforged Draenei';
SET @LightforgedDraeneiRacialNamekoKR         = '';
SET @LightforgedDraeneiRacialNamefrFR         = '';
SET @LightforgedDraeneiRacialNamedeDE         = '';
SET @LightforgedDraeneiRacialNamezhCN         = '';
SET @LightforgedDraeneiRacialNamezhTW         = '';
SET @LightforgedDraeneiRacialNameesES         = '';
SET @LightforgedDraeneiRacialNameesMX         = '';
SET @LightforgedDraeneiRacialNameruRU         = '';
SET @LightforgedDraeneiRacialNamejaJP         = '';
SET @LightforgedDraeneiRacialNameptPT         = '';
SET @LightforgedDraeneiRacialNameitIT         = '';

SET @LightforgedDraeneiPlayerenUS             = '"PLAYER", " Lightforged Draenei"';
SET @LightforgedDraeneiPlayerkoKR             = '';
SET @LightforgedDraeneiPlayerfrFR             = '';
SET @LightforgedDraeneiPlayerdeDE             = '';
SET @LightforgedDraeneiPlayerzhCN             = '';
SET @LightforgedDraeneiPlayerzhTW             = '';
SET @LightforgedDraeneiPlayeresES             = '';
SET @LightforgedDraeneiPlayeresMX             = '';
SET @LightforgedDraeneiPlayerruRU             = '';
SET @LightforgedDraeneiPlayerjaJP             = '';
SET @LightforgedDraeneiPlayerptPT             = '';
SET @LightforgedDraeneiPlayeritIT             = '';

SET @LightforgedDraeneiFactionNameenUS        = 'Army of the Light';
SET @LightforgedDraeneiFactionNamekoKR        = '';
SET @LightforgedDraeneiFactionNamefrFR        = '';
SET @LightforgedDraeneiFactionNamedeDE        = '';
SET @LightforgedDraeneiFactionNamezhCN        = '';
SET @LightforgedDraeneiFactionNamezhTW        = '';
SET @LightforgedDraeneiFactionNameesES        = '';
SET @LightforgedDraeneiFactionNameesMX        = '';
SET @LightforgedDraeneiFactionNameruRU        = '';
SET @LightforgedDraeneiFactionNamejaJP        = '';
SET @LightforgedDraeneiFactionNameptPT        = '';
SET @LightforgedDraeneiFactionNameitIT        = '';

SET @LightforgedDraeneiFactionDescriptionenUS = 'After the fall of Argus, the draenei\'s finest warriors followed the prime naaru Xe\'ra across the cosmos in an eternal war to bring about the Legion\'s end. Since then, other survivors of the Burning Crusade have joined the ranks of the Lightforged.';
SET @LightforgedDraeneiFactionDescriptionkoKR = '';
SET @LightforgedDraeneiFactionDescriptionfrFR = '';
SET @LightforgedDraeneiFactionDescriptiondeDE = '';
SET @LightforgedDraeneiFactionDescriptionzhCN = '';
SET @LightforgedDraeneiFactionDescriptionzhTW = '';
SET @LightforgedDraeneiFactionDescriptionesES = '';
SET @LightforgedDraeneiFactionDescriptionesMX = '';
SET @LightforgedDraeneiFactionDescriptionruRU = '';
SET @LightforgedDraeneiFactionDescriptionjaJP = '';
SET @LightforgedDraeneiFactionDescriptionptPT = '';
SET @LightforgedDraeneiFactionDescriptionitIT = '';
