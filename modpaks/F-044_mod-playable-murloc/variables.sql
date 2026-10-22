-- Race masks (race IDs are fixed in config.sql)
SET @MurlocMask                       = 1 << (@Murloc - 1); -- race ID 41 → 1099511627776
SET @MurlocMask_2                     = IF(@Murloc BETWEEN 65 AND 128, 1 << (@Murloc - 65), 0); -- races 65-128
SET @MurlocHelmetMask                 = 1 << @Murloc;       -- race ID 41 → 2199023255552

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                        = @HordeMask         | @MurlocMask;
SET @HordeMask_2                      = @HordeMask_2       | @MurlocMask_2; -- races 65-128
SET @BarrensBros                      = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @BarrensBros_2                    = @HordeMask_2  & ~@UndercityMask_2; -- races 65-128
SET @PlayableRaceMask                 = @PlayableRaceMask  | @MurlocMask;
SET @PlayableRaceMask_2               = @PlayableRaceMask_2 | @MurlocMask_2; -- races 65-128
SET @BowHunters                       = @BowHunters        | @MurlocMask;
SET @BowHunters_2                     = @BowHunters_2      | @MurlocMask_2; -- races 65-128
SET @MurlocLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MurlocAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @MurlocKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @MurlocFlags                      = @BarefootFlag | @CanMountFlag | @PlayableFlag; -- 14, as Troll
SET @MurlocExplorationSound           = @TrollExplorationSound;
SET @MurlocCinematicSequence          = @TrollCinematicSequence;
SET @MurlocBlood                      = 1;
SET @MurlocMaleModelPath              = 'Character\\Murloc\\Male\\Murloc.mdx';
SET @MurlocFemaleModelPath            = 'Character\\Murloc\\Female\\Murloc.mdx';
SET @MurlocCreatureModel              = 31;   -- Creature\Murloc\Murloc.mdx: size, collision and CreatureSoundData 31 (combat sounds)
SET @MurlocFaction                    = 1203; -- vacant slot
SET @MurlocPlayer                     = 1204; -- vacant slot

-- Voice: the murloc creature sounds stand in for a player voice set
SET @MurlocVoiceSound                 = 1109; -- MurlocAlert (mMurlocPreAggroA): error messages (VocalUISounds)
SET @MurlocEmoteSound                 = 416;  -- MurlocAggro (mMurlocAggroOld): voiced emotes (EmotesTextSound)

-- Strings
SET @MurlocClientPrefix               = 'Ta'; -- donor ChrRaces value (Tauren prefix)
SET @MurlocClientString               = 'Murloc';
SET @MurlocFacialHairCustomization1   = 'NORMAL';
SET @MurlocFacialHairCustomization2   = 'NORMAL';
SET @MurlocHairCustomization          = 'NORMAL';

-- Localization Strings
SET @MurlocenUS                       = 'Murloc';
SET @MurlockoKR                       = '멀록';
SET @MurlocfrFR                       = 'Murloc';
SET @MurlocdeDE                       = 'Murloc';
SET @MurloczhCN                       = '鱼人';
SET @MurloczhTW                       = '魚人';
SET @MurlocesES                       = 'múrloc';
SET @MurlocesMX                       = 'múrloc';
SET @MurlocruRU                       = 'мурлок';
SET @MurlocjaJP                       = '';
SET @MurlocptPT                       = '';
SET @MurlocitIT                       = '';
SET @MurlocUnk1                       = '';
SET @MurlocUnk2                       = '';
SET @MurlocUnk3                       = '';
SET @MurlocUnk4                       = '';

SET @MurlocFemaleenUS                 = '';
SET @MurlocFemalekoKR                 = '';
SET @MurlocFemalefrFR                 = '';
SET @MurlocFemaledeDE                 = '';
SET @MurlocFemalezhCN                 = '';
SET @MurlocFemalezhTW                 = '';
SET @MurlocFemaleesES                 = '';
SET @MurlocFemaleesMX                 = '';
SET @MurlocFemaleruRU                 = '';
SET @MurlocFemalejaJP                 = '';
SET @MurlocFemaleptPT                 = '';
SET @MurlocFemaleitIT                 = '';
SET @MurlocFemaleUnk1                 = '';
SET @MurlocFemaleUnk2                 = '';
SET @MurlocFemaleUnk3                 = '';
SET @MurlocFemaleUnk4                 = '';

SET @MurlocMaleenUS                   = '';
SET @MurlocMalekoKR                   = '';
SET @MurlocMalefrFR                   = '';
SET @MurlocMaledeDE                   = '';
SET @MurlocMalezhCN                   = '';
SET @MurlocMalezhTW                   = '';
SET @MurlocMaleesES                   = '';
SET @MurlocMaleesMX                   = '';
SET @MurlocMaleruRU                   = '';
SET @MurlocMalejaJP                   = '';
SET @MurlocMaleptPT                   = '';
SET @MurlocMaleitIT                   = '';
SET @MurlocMaleUnk1                   = '';
SET @MurlocMaleUnk2                   = '';
SET @MurlocMaleUnk3                   = '';
SET @MurlocMaleUnk4                   = '';

SET @MurlocRacialNameenUS             = 'Racial - Murloc';
SET @MurlocRacialNamekoKR             = '';
SET @MurlocRacialNamefrFR             = '';
SET @MurlocRacialNamedeDE             = '';
SET @MurlocRacialNamezhCN             = '';
SET @MurlocRacialNamezhTW             = '';
SET @MurlocRacialNameesES             = '';
SET @MurlocRacialNameesMX             = '';
SET @MurlocRacialNameruRU             = '';
SET @MurlocRacialNamejaJP             = '';
SET @MurlocRacialNameptPT             = '';
SET @MurlocRacialNameitIT             = '';
SET @MurlocRacialNameUnk1             = '';
SET @MurlocRacialNameUnk2             = '';
SET @MurlocRacialNameUnk3             = '';
SET @MurlocRacialNameUnk4             = '';

SET @MurlocPlayerenUS                 = '"PLAYER", Murloc';
SET @MurlocPlayerkoKR                 = '플레이어 - 멀록';
SET @MurlocPlayerfrFR                 = '"JOUEUR", Murloc';
SET @MurlocPlayerdeDE                 = '"SPIELER", Murloc';
SET @MurlocPlayerzhCN                 = '鱼人(玩家)';
SET @MurlocPlayerzhTW                 = '魚人(玩家)';
SET @MurlocPlayeresES                 = '"JUGADOR", múrloc';
SET @MurlocPlayeresMX                 = '"JUGADOR", múrloc';
SET @MurlocPlayerruRU                 = 'ИГРОК: мурлок';
SET @MurlocPlayerjaJP                 = '';
SET @MurlocPlayerptPT                 = '';
SET @MurlocPlayeritIT                 = '';
SET @MurlocPlayerUnk1                 = '';
SET @MurlocPlayerUnk2                 = '';
SET @MurlocPlayerUnk3                 = '';
SET @MurlocPlayerUnk4                 = '';

-- Placeholder name and description (no lore faction for Horde murlocs)
SET @MurlocFactionNameenUS            = 'Mrgl Tribe';
SET @MurlocFactionNamekoKR            = '';
SET @MurlocFactionNamefrFR            = '';
SET @MurlocFactionNamedeDE            = '';
SET @MurlocFactionNamezhCN            = '';
SET @MurlocFactionNamezhTW            = '';
SET @MurlocFactionNameesES            = '';
SET @MurlocFactionNameesMX            = '';
SET @MurlocFactionNameruRU            = '';
SET @MurlocFactionNamejaJP            = '';
SET @MurlocFactionNameptPT            = '';
SET @MurlocFactionNameitIT            = '';
SET @MurlocFactionNameUnk1            = '';
SET @MurlocFactionNameUnk2            = '';
SET @MurlocFactionNameUnk3            = '';
SET @MurlocFactionNameUnk4            = '';

SET @MurlocFactionDescriptionenUS     = 'Coastal murlocs of Durotar who threw in their lot with the Horde.';
SET @MurlocFactionDescriptionkoKR     = '';
SET @MurlocFactionDescriptionfrFR     = '';
SET @MurlocFactionDescriptiondeDE     = '';
SET @MurlocFactionDescriptionzhCN     = '';
SET @MurlocFactionDescriptionzhTW     = '';
SET @MurlocFactionDescriptionesES     = '';
SET @MurlocFactionDescriptionesMX     = '';
SET @MurlocFactionDescriptionruRU     = '';
SET @MurlocFactionDescriptionjaJP     = '';
SET @MurlocFactionDescriptionptPT     = '';
SET @MurlocFactionDescriptionitIT     = '';
SET @MurlocFactionDescriptionUnk1     = '';
SET @MurlocFactionDescriptionUnk2     = '';
SET @MurlocFactionDescriptionUnk3     = '';
SET @MurlocFactionDescriptionUnk4     = '';

SET @MurlocAchievementenUS            = 'Realm First! Level 80 Murloc';
SET @MurlocAchievementkoKR            = '';
SET @MurlocAchievementfrFR            = '';
SET @MurlocAchievementdeDE            = '';
SET @MurlocAchievementzhCN            = '';
SET @MurlocAchievementzhTW            = '';
SET @MurlocAchievementesES            = '';
SET @MurlocAchievementesMX            = '';
SET @MurlocAchievementruRU            = '';
SET @MurlocAchievementjaJP            = '';
SET @MurlocAchievementptPT            = '';
SET @MurlocAchievementitIT            = '';
SET @MurlocAchievementUnk1            = '';
SET @MurlocAchievementUnk2            = '';
SET @MurlocAchievementUnk3            = '';
SET @MurlocAchievementUnk4            = '';

SET @MurlocAchievementDescriptionenUS = 'First Murloc on the realm to achieve level 80.';
SET @MurlocAchievementDescriptionkoKR = '';
SET @MurlocAchievementDescriptionfrFR = '';
SET @MurlocAchievementDescriptiondeDE = '';
SET @MurlocAchievementDescriptionzhCN = '';
SET @MurlocAchievementDescriptionzhTW = '';
SET @MurlocAchievementDescriptionesES = '';
SET @MurlocAchievementDescriptionesMX = '';
SET @MurlocAchievementDescriptionruRU = '';
SET @MurlocAchievementDescriptionjaJP = '';
SET @MurlocAchievementDescriptionptPT = '';
SET @MurlocAchievementDescriptionitIT = '';
SET @MurlocAchievementDescriptionUnk1 = '';
SET @MurlocAchievementDescriptionUnk2 = '';
SET @MurlocAchievementDescriptionUnk3 = '';
SET @MurlocAchievementDescriptionUnk4 = '';
