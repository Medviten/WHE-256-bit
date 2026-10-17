-- Race masks (race IDs are fixed in config.sql)
SET @LightforgedDraeneiMask                     = 1 << (@LightforgedDraenei - 1); -- race ID 30 → 536870912
SET @LightforgedDraeneiHelmetMask               = 1 << @LightforgedDraenei; -- race ID 30 → 1073741824

-- Important variable updates (Alliance vs. Horde)
SET @AllianceMask                               = @AllianceMask     | @LightforgedDraeneiMask;
SET @BarrensBros                                = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask                           = @PlayableRaceMask | @LightforgedDraeneiMask;
SET @CrossbowHunters                            = @CrossbowHunters  | @LightforgedDraeneiMask;
SET @LightforgedDraeneiLanguage                 = 7; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @LightforgedDraeneiAlliance                 = 0; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @LightforgedDraeneiKnowThyEnemy             = @KnowThyEnemyAlliance;

-- Miscellaneous
SET @LightforgedDraeneiFlags                    = @DraeneiFlags;
SET @LightforgedDraeneiExplorationSound         = @DraeneiExplorationSound;
SET @LightforgedDraeneiCinematicSequence        = @DraeneiCinematicSequence;
SET @LightforgedDraeneiBlood                    = @DraeneiBlood;
SET @LightforgedDraeneiMaleModelPath            = 'Character\\LightforgedDraenei\\Male\\LightforgedDraeneiMale.mdx';
SET @LightforgedDraeneiFemaleModelPath          = 'Character\\LightforgedDraenei\\Female\\LightforgedDraeneiFemale.mdx';
SET @LightforgedDraeneiMaleFootprint            = @FootprintHoof;
SET @LightforgedDraeneiFemaleFootprint          = @FootprintHoof;
SET @LightforgedDraeneiMount1ModelPath          = 'Creature\\LightforgedElekk\\LightforgedElekk.m2';
SET @LightforgedDraeneiFaction                  = 2165; -- Army of the Light (Legion ID)
SET @LightforgedDraeneiPlayer                   = 2232; -- Legion ID

-- Mounts (IDs are global, see config.sql)
SET @LightforgedDraeneiMount1                = @SpellLightforgedFelcrusher;
SET @LightforgedDraeneiMount1Model           = @LightforgedFelcrusherModel;
SET @LightforgedDraeneiMount1Display         = @LightforgedFelcrusherDisplay;
SET @LightforgedDraeneiMount1CreatureID      = @LightforgedFelcrusherCreatureID;
SET @LightforgedDraeneiMount1Item            = @LightforgedFelcrusherItem;
SET @LightforgedDraeneiMount1ItemDisplay     = @LightforgedFelcrusherItemDisplay;
SET @LightforgedDraeneiMount1IconID          = @IconLightforgedFelcrusher;

SET @LightforgedDraeneiMount2                = @SpellBlessedFelcrusher;
SET @LightforgedDraeneiMount2Model           = @LightforgedFelcrusherModel;
SET @LightforgedDraeneiMount2Display         = @BlessedFelcrusherDisplay;
SET @LightforgedDraeneiMount2CreatureID      = @BlessedFelcrusherCreatureID;
SET @LightforgedDraeneiMount2Item            = @BlessedFelcrusherItem;
SET @LightforgedDraeneiMount2ItemDisplay     = @BlessedFelcrusherItemDisplay;
SET @LightforgedDraeneiMount2IconID          = @IconBlessedFelcrusher;

SET @LightforgedDraeneiMount3                = @SpellAvengingFelcrusher;
SET @LightforgedDraeneiMount3Model           = @LightforgedFelcrusherModel;
SET @LightforgedDraeneiMount3Display         = @AvengingFelcrusherDisplay;
SET @LightforgedDraeneiMount3CreatureID      = @AvengingFelcrusherCreatureID;
SET @LightforgedDraeneiMount3Item            = @AvengingFelcrusherItem;
SET @LightforgedDraeneiMount3ItemDisplay     = @AvengingFelcrusherItemDisplay;
SET @LightforgedDraeneiMount3IconID          = @IconAvengingFelcrusher;

SET @LightforgedDraeneiMount4                = @SpellGloriousFelcrusher;
SET @LightforgedDraeneiMount4Model           = @LightforgedFelcrusherModel;
SET @LightforgedDraeneiMount4Display         = @GloriousFelcrusherDisplay;
SET @LightforgedDraeneiMount4CreatureID      = @GloriousFelcrusherCreatureID;
SET @LightforgedDraeneiMount4Item            = @GloriousFelcrusherItem;
SET @LightforgedDraeneiMount4ItemDisplay     = @GloriousFelcrusherItemDisplay;
SET @LightforgedDraeneiMount4IconID          = @IconGloriousFelcrusher;

-- Spells
SET @LightforgedDraeneiRacial1                  = @SpellDemonbane;
SET @LightforgedDraeneiRacial2                  = @SpellForgeOfLight1;
SET @LightforgedDraeneiRacial3                  = @SpellForgeOfLight2;
SET @LightforgedDraeneiRacial4                  = @SpellHolyProvidence;
SET @LightforgedDraeneiRacial5                  = @SpellLightsJudgement;
SET @LightforgedDraeneiRacial6                  = @SpellLightsReckoning;

-- Icons
SET @LightforgedDraeneiRacialIcon1              = @IconDemonbane;
SET @LightforgedDraeneiRacialIcon2              = @IconForgeOfLight;
SET @LightforgedDraeneiRacialIcon3              = @LightforgedDraeneiRacialIcon2;
SET @LightforgedDraeneiRacialIcon4              = @IconHolyProvidence;
SET @LightforgedDraeneiRacialIcon5              = @IconLightsJudgement;
SET @LightforgedDraeneiRacialIcon6              = @IconLightsReckoning;

-- Icon name
SET @LightforgedDraeneiMount1IconName           = 'inv_lightforgedelekk';
SET @LightforgedDraeneiMount2IconName           = 'inv_lightforgedelekk_amethyst';
SET @LightforgedDraeneiMount3IconName           = 'inv_lightforgedelekk_blue';
SET @LightforgedDraeneiMount4IconName           = @LightforgedDraeneiMount1IconName;
SET @LightforgedDraeneiRacialIcon1Name          = 'ability_racial_demonbane';
SET @LightforgedDraeneiRacialIcon2Name          = 'ability_racial_forgeoflight';
SET @LightforgedDraeneiRacialIcon3Name          = @LightforgedDraeneiRacialIcon2Name;
SET @LightforgedDraeneiRacialIcon4Name          = 'ability_racial_holyresistance';
SET @LightforgedDraeneiRacialIcon5Name          = 'ability_racial_orbitalstrike';
SET @LightforgedDraeneiRacialIcon6Name          = 'ability_racial_finalverdict';

-- Icon paths
SET @LightforgedDraeneiMount1IconPath           = 'Interface\\Icons\\inv_lightforgedelekk';
SET @LightforgedDraeneiMount2IconPath           = 'Interface\\Icons\\inv_lightforgedelekk_amethyst';
SET @LightforgedDraeneiMount3IconPath           = 'Interface\\Icons\\inv_lightforgedelekk_blue';
SET @LightforgedDraeneiMount4IconPath           = @LightforgedDraeneiMount1IconPath;
SET @LightforgedDraeneiRacialIcon1Path          = 'Interface\\Icons\\ability_racial_demonbane';
SET @LightforgedDraeneiRacialIcon2Path          = 'Interface\\Icons\\ability_racial_forgeoflight';
SET @LightforgedDraeneiRacialIcon3Path          = @LightforgedDraeneiRacialIcon2Path;
SET @LightforgedDraeneiRacialIcon4Path          = 'Interface\\Icons\\ability_racial_holyresistance';
SET @LightforgedDraeneiRacialIcon5Path          = 'Interface\\Icons\\ability_racial_orbitalstrike';
SET @LightforgedDraeneiRacialIcon6Path          = 'Interface\\Icons\\ability_racial_finalverdict';

-- Strings
SET @LightforgedDraeneiClientPrefix             = 'Dr'; -- Copying Draenei
SET @LightforgedDraeneiClientString             = 'LightforgedDraenei';
SET @LightforgedDraeneiFacialHairCustomization1 = 'NORMAL';
SET @LightforgedDraeneiFacialHairCustomization2 = 'HORNS';
SET @LightforgedDraeneiHairCustomization        = 'NORMAL';

-- Localization Strings
SET @LightforgedDraeneienUS                     = 'Lightforged Draenei';
SET @LightforgedDraeneikoKR                     = '';
SET @LightforgedDraeneifrFR                     = '';
SET @LightforgedDraeneideDE                     = '';
SET @LightforgedDraeneizhCN                     = '';
SET @LightforgedDraeneizhTW                     = '';
SET @LightforgedDraeneiesES                     = '';
SET @LightforgedDraeneiesMX                     = '';
SET @LightforgedDraeneiruRU                     = '';
SET @LightforgedDraeneijaJP                     = '';
SET @LightforgedDraeneiptPT                     = '';
SET @LightforgedDraeneiitIT                     = '';
SET @LightforgedDraeneiUnk1                     = '';
SET @LightforgedDraeneiUnk2                     = '';
SET @LightforgedDraeneiUnk3                     = '';
SET @LightforgedDraeneiUnk4                     = '';

SET @LightforgedDraeneiFemaleenUS               = '';
SET @LightforgedDraeneiFemalekoKR               = '';
SET @LightforgedDraeneiFemalefrFR               = '';
SET @LightforgedDraeneiFemaledeDE               = '';
SET @LightforgedDraeneiFemalezhCN               = '';
SET @LightforgedDraeneiFemalezhTW               = '';
SET @LightforgedDraeneiFemaleesES               = '';
SET @LightforgedDraeneiFemaleesMX               = '';
SET @LightforgedDraeneiFemaleruRU               = '';
SET @LightforgedDraeneiFemalejaJP               = '';
SET @LightforgedDraeneiFemaleptPT               = '';
SET @LightforgedDraeneiFemaleitIT               = '';
SET @LightforgedDraeneiFemaleUnk1               = '';
SET @LightforgedDraeneiFemaleUnk2               = '';
SET @LightforgedDraeneiFemaleUnk3               = '';
SET @LightforgedDraeneiFemaleUnk4               = '';

SET @LightforgedDraeneiMaleenUS                 = '';
SET @LightforgedDraeneiMalekoKR                 = '';
SET @LightforgedDraeneiMalefrFR                 = '';
SET @LightforgedDraeneiMaledeDE                 = '';
SET @LightforgedDraeneiMalezhCN                 = '';
SET @LightforgedDraeneiMalezhTW                 = '';
SET @LightforgedDraeneiMaleesES                 = '';
SET @LightforgedDraeneiMaleesMX                 = '';
SET @LightforgedDraeneiMaleruRU                 = '';
SET @LightforgedDraeneiMalejaJP                 = '';
SET @LightforgedDraeneiMaleptPT                 = '';
SET @LightforgedDraeneiMaleitIT                 = '';
SET @LightforgedDraeneiMaleUnk1                 = '';
SET @LightforgedDraeneiMaleUnk2                 = '';
SET @LightforgedDraeneiMaleUnk3                 = '';
SET @LightforgedDraeneiMaleUnk4                 = '';

SET @LightforgedDraeneiRacialNameenUS           = 'Racial - Lightforged Draenei';
SET @LightforgedDraeneiRacialNamekoKR           = '';
SET @LightforgedDraeneiRacialNamefrFR           = '';
SET @LightforgedDraeneiRacialNamedeDE           = '';
SET @LightforgedDraeneiRacialNamezhCN           = '';
SET @LightforgedDraeneiRacialNamezhTW           = '';
SET @LightforgedDraeneiRacialNameesES           = '';
SET @LightforgedDraeneiRacialNameesMX           = '';
SET @LightforgedDraeneiRacialNameruRU           = '';
SET @LightforgedDraeneiRacialNamejaJP           = '';
SET @LightforgedDraeneiRacialNameptPT           = '';
SET @LightforgedDraeneiRacialNameitIT           = '';
SET @LightforgedDraeneiRacialNameUnk1           = '';
SET @LightforgedDraeneiRacialNameUnk2           = '';
SET @LightforgedDraeneiRacialNameUnk3           = '';
SET @LightforgedDraeneiRacialNameUnk4           = '';

SET @LightforgedDraeneiPlayerenUS               = '"PLAYER", " Lightforged Draenei"';
SET @LightforgedDraeneiPlayerkoKR               = '';
SET @LightforgedDraeneiPlayerfrFR               = '';
SET @LightforgedDraeneiPlayerdeDE               = '';
SET @LightforgedDraeneiPlayerzhCN               = '';
SET @LightforgedDraeneiPlayerzhTW               = '';
SET @LightforgedDraeneiPlayeresES               = '';
SET @LightforgedDraeneiPlayeresMX               = '';
SET @LightforgedDraeneiPlayerruRU               = '';
SET @LightforgedDraeneiPlayerjaJP               = '';
SET @LightforgedDraeneiPlayerptPT               = '';
SET @LightforgedDraeneiPlayeritIT               = '';
SET @LightforgedDraeneiPlayerUnk1               = '';
SET @LightforgedDraeneiPlayerUnk2               = '';
SET @LightforgedDraeneiPlayerUnk3               = '';
SET @LightforgedDraeneiPlayerUnk4               = '';

SET @LightforgedDraeneiFactionNameenUS          = 'Army of the Light';
SET @LightforgedDraeneiFactionNamekoKR          = '';
SET @LightforgedDraeneiFactionNamefrFR          = '';
SET @LightforgedDraeneiFactionNamedeDE          = '';
SET @LightforgedDraeneiFactionNamezhCN          = '';
SET @LightforgedDraeneiFactionNamezhTW          = '';
SET @LightforgedDraeneiFactionNameesES          = '';
SET @LightforgedDraeneiFactionNameesMX          = '';
SET @LightforgedDraeneiFactionNameruRU          = '';
SET @LightforgedDraeneiFactionNamejaJP          = '';
SET @LightforgedDraeneiFactionNameptPT          = '';
SET @LightforgedDraeneiFactionNameitIT          = '';
SET @LightforgedDraeneiFactionNameUnk1          = '';
SET @LightforgedDraeneiFactionNameUnk2          = '';
SET @LightforgedDraeneiFactionNameUnk3          = '';
SET @LightforgedDraeneiFactionNameUnk4          = '';

SET @LightforgedDraeneiFactionDescriptionenUS   = 'After the fall of Argus, the draenei\'s finest warriors followed the prime naaru Xe\'ra across the cosmos in an eternal war to bring about the Legion\'s end. Since then, other survivors of the Burning Crusade have joined the ranks of the Lightforged.';
SET @LightforgedDraeneiFactionDescriptionkoKR   = '';
SET @LightforgedDraeneiFactionDescriptionfrFR   = '';
SET @LightforgedDraeneiFactionDescriptiondeDE   = '';
SET @LightforgedDraeneiFactionDescriptionzhCN   = '';
SET @LightforgedDraeneiFactionDescriptionzhTW   = '';
SET @LightforgedDraeneiFactionDescriptionesES   = '';
SET @LightforgedDraeneiFactionDescriptionesMX   = '';
SET @LightforgedDraeneiFactionDescriptionruRU   = '';
SET @LightforgedDraeneiFactionDescriptionjaJP   = '';
SET @LightforgedDraeneiFactionDescriptionptPT   = '';
SET @LightforgedDraeneiFactionDescriptionitIT   = '';
SET @LightforgedDraeneiFactionDescriptionUnk1   = '';
SET @LightforgedDraeneiFactionDescriptionUnk2   = '';
SET @LightforgedDraeneiFactionDescriptionUnk3   = '';
SET @LightforgedDraeneiFactionDescriptionUnk4   = '';

-- Racial Mount Strings
SET @LightforgedDraeneiMount1NameenUS                = 'Lightforged Felcrusher';
SET @LightforgedDraeneiMount1NamekoKR                = '';
SET @LightforgedDraeneiMount1NamefrFR                = '';
SET @LightforgedDraeneiMount1NamedeDE                = '';
SET @LightforgedDraeneiMount1NamezhCN                = '';
SET @LightforgedDraeneiMount1NamezhTW                = '';
SET @LightforgedDraeneiMount1NameesES                = '';
SET @LightforgedDraeneiMount1NameesMX                = '';
SET @LightforgedDraeneiMount1NameruRU                = '';
SET @LightforgedDraeneiMount1NamejaJP                = '';
SET @LightforgedDraeneiMount1NameptPT                = '';
SET @LightforgedDraeneiMount1NameitIT                = '';
SET @LightforgedDraeneiMount1NameUnk1                = '';
SET @LightforgedDraeneiMount1NameUnk2                = '';
SET @LightforgedDraeneiMount1NameUnk3                = '';
SET @LightforgedDraeneiMount1NameUnk4                = '';

SET @LightforgedDraeneiMount1SpellDescriptionenUS    = 'Summons and dismisses a rideable Lightforged Felcrusher.';
SET @LightforgedDraeneiMount1SpellDescriptionkoKR    = '';
SET @LightforgedDraeneiMount1SpellDescriptionfrFR    = '';
SET @LightforgedDraeneiMount1SpellDescriptiondeDE    = '';
SET @LightforgedDraeneiMount1SpellDescriptionzhCN    = '';
SET @LightforgedDraeneiMount1SpellDescriptionzhTW    = '';
SET @LightforgedDraeneiMount1SpellDescriptionesES    = '';
SET @LightforgedDraeneiMount1SpellDescriptionesMX    = '';
SET @LightforgedDraeneiMount1SpellDescriptionruRU    = '';
SET @LightforgedDraeneiMount1SpellDescriptionjaJP    = '';
SET @LightforgedDraeneiMount1SpellDescriptionptPT    = '';
SET @LightforgedDraeneiMount1SpellDescriptionitIT    = '';
SET @LightforgedDraeneiMount1SpellDescriptionUnk1    = '';
SET @LightforgedDraeneiMount1SpellDescriptionUnk2    = '';
SET @LightforgedDraeneiMount1SpellDescriptionUnk3    = '';
SET @LightforgedDraeneiMount1SpellDescriptionUnk4    = '';

SET @LightforgedDraeneiMount1ItemNameenUS            = @LightforgedDraeneiMount1NameenUS;
SET @LightforgedDraeneiMount1ItemDescriptionenUS     = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Lightforged Felcrusher.';

SET @LightforgedDraeneiMount2NameenUS                = 'Blessed Felcrusher';
SET @LightforgedDraeneiMount2NamekoKR                = '';
SET @LightforgedDraeneiMount2NamefrFR                = '';
SET @LightforgedDraeneiMount2NamedeDE                = '';
SET @LightforgedDraeneiMount2NamezhCN                = '';
SET @LightforgedDraeneiMount2NamezhTW                = '';
SET @LightforgedDraeneiMount2NameesES                = '';
SET @LightforgedDraeneiMount2NameesMX                = '';
SET @LightforgedDraeneiMount2NameruRU                = '';
SET @LightforgedDraeneiMount2NamejaJP                = '';
SET @LightforgedDraeneiMount2NameptPT                = '';
SET @LightforgedDraeneiMount2NameitIT                = '';
SET @LightforgedDraeneiMount2NameUnk1                = '';
SET @LightforgedDraeneiMount2NameUnk2                = '';
SET @LightforgedDraeneiMount2NameUnk3                = '';
SET @LightforgedDraeneiMount2NameUnk4                = '';

SET @LightforgedDraeneiMount2SpellDescriptionenUS    = 'Summons and dismisses a rideable Blessed Felcrusher.';
SET @LightforgedDraeneiMount2SpellDescriptionkoKR    = '';
SET @LightforgedDraeneiMount2SpellDescriptionfrFR    = '';
SET @LightforgedDraeneiMount2SpellDescriptiondeDE    = '';
SET @LightforgedDraeneiMount2SpellDescriptionzhCN    = '';
SET @LightforgedDraeneiMount2SpellDescriptionzhTW    = '';
SET @LightforgedDraeneiMount2SpellDescriptionesES    = '';
SET @LightforgedDraeneiMount2SpellDescriptionesMX    = '';
SET @LightforgedDraeneiMount2SpellDescriptionruRU    = '';
SET @LightforgedDraeneiMount2SpellDescriptionjaJP    = '';
SET @LightforgedDraeneiMount2SpellDescriptionptPT    = '';
SET @LightforgedDraeneiMount2SpellDescriptionitIT    = '';
SET @LightforgedDraeneiMount2SpellDescriptionUnk1    = '';
SET @LightforgedDraeneiMount2SpellDescriptionUnk2    = '';
SET @LightforgedDraeneiMount2SpellDescriptionUnk3    = '';
SET @LightforgedDraeneiMount2SpellDescriptionUnk4    = '';

SET @LightforgedDraeneiMount2ItemNameenUS            = @LightforgedDraeneiMount2NameenUS;
SET @LightforgedDraeneiMount2ItemDescriptionenUS     = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Blessed Felcrusher.';

SET @LightforgedDraeneiMount3NameenUS                = 'Avenging Felcrusher';
SET @LightforgedDraeneiMount3NamekoKR                = '';
SET @LightforgedDraeneiMount3NamefrFR                = '';
SET @LightforgedDraeneiMount3NamedeDE                = '';
SET @LightforgedDraeneiMount3NamezhCN                = '';
SET @LightforgedDraeneiMount3NamezhTW                = '';
SET @LightforgedDraeneiMount3NameesES                = '';
SET @LightforgedDraeneiMount3NameesMX                = '';
SET @LightforgedDraeneiMount3NameruRU                = '';
SET @LightforgedDraeneiMount3NamejaJP                = '';
SET @LightforgedDraeneiMount3NameptPT                = '';
SET @LightforgedDraeneiMount3NameitIT                = '';
SET @LightforgedDraeneiMount3NameUnk1                = '';
SET @LightforgedDraeneiMount3NameUnk2                = '';
SET @LightforgedDraeneiMount3NameUnk3                = '';
SET @LightforgedDraeneiMount3NameUnk4                = '';

SET @LightforgedDraeneiMount3SpellDescriptionenUS    = 'Summons and dismisses a rideable Avenging Felcrusher.';
SET @LightforgedDraeneiMount3SpellDescriptionkoKR    = '';
SET @LightforgedDraeneiMount3SpellDescriptionfrFR    = '';
SET @LightforgedDraeneiMount3SpellDescriptiondeDE    = '';
SET @LightforgedDraeneiMount3SpellDescriptionzhCN    = '';
SET @LightforgedDraeneiMount3SpellDescriptionzhTW    = '';
SET @LightforgedDraeneiMount3SpellDescriptionesES    = '';
SET @LightforgedDraeneiMount3SpellDescriptionesMX    = '';
SET @LightforgedDraeneiMount3SpellDescriptionruRU    = '';
SET @LightforgedDraeneiMount3SpellDescriptionjaJP    = '';
SET @LightforgedDraeneiMount3SpellDescriptionptPT    = '';
SET @LightforgedDraeneiMount3SpellDescriptionitIT    = '';
SET @LightforgedDraeneiMount3SpellDescriptionUnk1    = '';
SET @LightforgedDraeneiMount3SpellDescriptionUnk2    = '';
SET @LightforgedDraeneiMount3SpellDescriptionUnk3    = '';
SET @LightforgedDraeneiMount3SpellDescriptionUnk4    = '';

SET @LightforgedDraeneiMount3ItemNameenUS            = @LightforgedDraeneiMount3NameenUS;
SET @LightforgedDraeneiMount3ItemDescriptionenUS     = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Avenging Felcrusher.';

SET @LightforgedDraeneiMount4NameenUS                = 'Glorious Felcrusher';
SET @LightforgedDraeneiMount4NamekoKR                = '';
SET @LightforgedDraeneiMount4NamefrFR                = '';
SET @LightforgedDraeneiMount4NamedeDE                = '';
SET @LightforgedDraeneiMount4NamezhCN                = '';
SET @LightforgedDraeneiMount4NamezhTW                = '';
SET @LightforgedDraeneiMount4NameesES                = '';
SET @LightforgedDraeneiMount4NameesMX                = '';
SET @LightforgedDraeneiMount4NameruRU                = '';
SET @LightforgedDraeneiMount4NamejaJP                = '';
SET @LightforgedDraeneiMount4NameptPT                = '';
SET @LightforgedDraeneiMount4NameitIT                = '';
SET @LightforgedDraeneiMount4NameUnk1                = '';
SET @LightforgedDraeneiMount4NameUnk2                = '';
SET @LightforgedDraeneiMount4NameUnk3                = '';
SET @LightforgedDraeneiMount4NameUnk4                = '';

SET @LightforgedDraeneiMount4SpellDescriptionenUS    = 'Summons and dismisses a rideable Glorious Felcrusher.';
SET @LightforgedDraeneiMount4SpellDescriptionkoKR    = '';
SET @LightforgedDraeneiMount4SpellDescriptionfrFR    = '';
SET @LightforgedDraeneiMount4SpellDescriptiondeDE    = '';
SET @LightforgedDraeneiMount4SpellDescriptionzhCN    = '';
SET @LightforgedDraeneiMount4SpellDescriptionzhTW    = '';
SET @LightforgedDraeneiMount4SpellDescriptionesES    = '';
SET @LightforgedDraeneiMount4SpellDescriptionesMX    = '';
SET @LightforgedDraeneiMount4SpellDescriptionruRU    = '';
SET @LightforgedDraeneiMount4SpellDescriptionjaJP    = '';
SET @LightforgedDraeneiMount4SpellDescriptionptPT    = '';
SET @LightforgedDraeneiMount4SpellDescriptionitIT    = '';
SET @LightforgedDraeneiMount4SpellDescriptionUnk1    = '';
SET @LightforgedDraeneiMount4SpellDescriptionUnk2    = '';
SET @LightforgedDraeneiMount4SpellDescriptionUnk3    = '';
SET @LightforgedDraeneiMount4SpellDescriptionUnk4    = '';

SET @LightforgedDraeneiMount4ItemNameenUS            = @LightforgedDraeneiMount4NameenUS;
SET @LightforgedDraeneiMount4ItemDescriptionenUS     = 'Teaches you how to summon this mount.\n\nSummons and dismisses a rideable Glorious Felcrusher.';
