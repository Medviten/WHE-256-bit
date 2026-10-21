-- Race masks (race IDs are fixed in config.sql)
SET @OgreMask = 1 << (@Ogre - 1);       -- race ID 39 → 274877906944
SET @OgreMask_2= IF(@Ogre BETWEEN 65 AND 128, 1 << (@Ogre - 65), 0); -- races 65-128
SET @OgreHelmetMask = 1 << @Ogre;       -- race ID 39 → 549755813888

-- Important variable update
SET @HordeMask        = @HordeMask    | @OgreMask;
SET @HordeMask_2      = @HordeMask_2    | @OgreMask_2; -- races 65-128
SET @BarrensBros      = @HordeMask    & ~@UndercityMask;
SET @BarrensBros_2    = @HordeMask_2    & ~@UndercityMask_2; -- races 65-128
SET @PlayableRaceMask = @AllianceMask | @HordeMask;
SET @PlayableRaceMask_2= @AllianceMask_2 | @HordeMask_2; -- races 65-128
SET @BowHunters       = @BowHunters   | @OgreMask;
SET @BowHunters_2     = @BowHunters_2   | @OgreMask_2; -- races 65-128

-- Miscellaneous
SET @OgreExplorationSound = @OrcExplorationSound;
SET @OgreCinematicSequence = @OrcCinematicSequence;
