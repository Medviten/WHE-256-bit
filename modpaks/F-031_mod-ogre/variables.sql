-- Race masks (race IDs are fixed in config.sql)
SET @OgreMask = 1 << (@Ogre - 1);       -- race ID 39 → 274877906944
SET @OgreHelmetMask = 1 << @Ogre;       -- race ID 39 → 549755813888

-- Important variable update
SET @HordeMask        = @HordeMask    | @OgreMask;
SET @BarrensBros      = @HordeMask    & ~@UndercityMask;
SET @PlayableRaceMask = @AllianceMask | @HordeMask;
SET @BowHunters       = @BowHunters   | @OgreMask;

-- Miscellaneous
SET @OgreExplorationSound = @OrcExplorationSound;
SET @OgreCinematicSequence = @OrcCinematicSequence;
