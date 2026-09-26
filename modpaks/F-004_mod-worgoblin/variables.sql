-- Race ID
SET @Goblin               = 9;                         -- default: 9
SET @GoblinMask           = 1 << (@Goblin - 1);        -- default: 256
SET @GoblinHelmetMask     = 1 << @Goblin;              -- default: 512
SET @Worgen := @NextRace := @NextRace +1;              -- default: 12
SET @WorgenMask           = 1 << (@Worgen - 1);        -- default: 2048
SET @WorgenHelmetMask     = 1 << @Worgen;              -- default: 4096
SET @Gilnean             := @NextRace := @NextRace +1; -- default: 23
SET @GilneanMask          = 1 << (@Gilnean - 1);       -- default: 4194304
SET @GilneanHelmetMask    = 1 << @Gilnean;             -- default: 8388608

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
