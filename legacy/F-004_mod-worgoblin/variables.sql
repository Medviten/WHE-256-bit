-- Race masks (race IDs are fixed in config.sql)
SET @GoblinMask           = 1 << (@Goblin - 1);        -- race ID 9 → 256
SET @GoblinMask_2         = IF(@Goblin BETWEEN 65 AND 128, 1 << (@Goblin - 65), 0); -- races 65-128
SET @GoblinHelmetMask     = 1 << @Goblin;              -- race ID 9 → 512
SET @WorgenMask           = 1 << (@Worgen - 1);        -- race ID 22 → 2097152
SET @WorgenMask_2         = IF(@Worgen BETWEEN 65 AND 128, 1 << (@Worgen - 65), 0); -- races 65-128
SET @WorgenHelmetMask     = 1 << @Worgen;              -- race ID 22 → 4194304
SET @GilneanMask          = 1 << (@Gilnean - 1);       -- race ID 23 → 4194304
SET @GilneanMask_2        = IF(@Gilnean BETWEEN 65 AND 128, 1 << (@Gilnean - 65), 0); -- races 65-128
SET @GilneanHelmetMask    = 1 << @Gilnean;             -- race ID 23 → 8388608

-- Important variable update
SET @AllianceMask     = @AllianceMask |  @WorgenMask | @GilneanMask;
SET @AllianceMask_2   = @AllianceMask_2 |  @WorgenMask_2 | @GilneanMask_2; -- races 65-128
SET @HordeMask        = @HordeMask    |  @GoblinMask;
SET @HordeMask_2      = @HordeMask_2    |  @GoblinMask_2; -- races 65-128
SET @BarrensBros      = @HordeMask    & ~@UndercityMask;
SET @BarrensBros_2    = @HordeMask_2    & ~@UndercityMask_2; -- races 65-128
SET @PlayableRaceMask = @AllianceMask |  @HordeMask;
SET @PlayableRaceMask_2= @AllianceMask_2 |  @HordeMask_2; -- races 65-128
SET @GunHunters       = @GunHunters   |  @WorgenMask | @GoblinMask | @GilneanMask;
SET @GunHunters_2     = @GunHunters_2   |  @WorgenMask_2 | @GoblinMask_2 | @GilneanMask_2; -- races 65-128

-- Miscellaneous
SET @GoblinExplorationSound   = @OrcExplorationSound;
SET @GoblinCinematicSequence  = @OrcCinematicSequence;
SET @WorgenExplorationSound   = @TaurenExplorationSound;
SET @WorgenCinematicSequence  = @NightElfCinematicSequence;
SET @GilneanExplorationSound  = @WorgenExplorationSound;
SET @GilneanCinematicSequence = @WorgenCinematicSequence;

-- Mounts (IDs are global, see config.sql)
SET @GoblinMount1                            = @SpellGoblinTrike;
SET @GoblinMount1Model                       = @GoblinTrikeModel;
SET @GoblinMount1Display                     = @GoblinTrikeDisplay;
SET @GoblinMount1CreatureID                  = @GoblinTrikeCreatureID;
SET @GoblinMount1Item                        = @GoblinTrikeItem;
SET @GoblinMount1ItemDisplay                 = @GoblinTrikeItemDisplay;

SET @GoblinMount2                            = @SpellGoblinTurboTrike;
SET @GoblinMount2Model                       = @GoblinTurboTrikeModel;
SET @GoblinMount2Display                     = @GoblinTurboTrikeDisplay;
SET @GoblinMount2CreatureID                  = @GoblinTurboTrikeCreatureID;
SET @GoblinMount2Item                        = @GoblinTurboTrikeItem;
SET @GoblinMount2ItemDisplay                 = @GoblinTurboTrikeItemDisplay;

-- Mounts (IDs are global, see config.sql)
SET @WorgenMount1                            = @SpellMountainHorse;
SET @WorgenMount1Model                       = @HorseModel;
SET @WorgenMount1Display                     = @MountainHorseDisplay;
SET @WorgenMount1CreatureID                  = @MountainHorseCreatureID;
SET @WorgenMount1Item                        = @MountainHorseItem;
SET @WorgenMount1ItemDisplay                 = @MountainHorseItemDisplay;

SET @WorgenMount2                            = @SpellSwiftMountainHorse;
SET @WorgenMount2Model                       = @HorseModel;
SET @WorgenMount2Display                     = @SwiftMountainHorseDisplay;
SET @WorgenMount2CreatureID                  = @SwiftMountainHorseCreatureID;
SET @WorgenMount2Item                        = @SwiftMountainHorseItem;
SET @WorgenMount2ItemDisplay                 = @SwiftMountainHorseItemDisplay;
