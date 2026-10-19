-- Race masks (race IDs are fixed in config.sql)
SET @GoblinMask           = 1 << (@Goblin - 1);        -- race ID 9 → 256
SET @GoblinHelmetMask     = 1 << @Goblin;              -- race ID 9 → 512
SET @WorgenMask           = 1 << (@Worgen - 1);        -- race ID 22 → 2097152
SET @WorgenHelmetMask     = 1 << @Worgen;              -- race ID 22 → 4194304
SET @GilneanMask          = 1 << (@Gilnean - 1);       -- race ID 23 → 4194304
SET @GilneanHelmetMask    = 1 << @Gilnean;             -- race ID 23 → 8388608

-- Important variable update
SET @AllianceMask     = @AllianceMask |  @WorgenMask | @GilneanMask;
SET @HordeMask        = @HordeMask    |  @GoblinMask;
SET @BarrensBros      = @HordeMask    & ~@UndercityMask;
SET @PlayableRaceMask = @AllianceMask |  @HordeMask;
SET @GunHunters       = @GunHunters   |  @WorgenMask | @GoblinMask | @GilneanMask;

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
