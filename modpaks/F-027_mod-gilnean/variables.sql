-- Race ID
SET @Gilnean                                := @NextRace := @NextRace +1; -- default: 23
SET @GilneanMask                            = 1 << (@Gilnean - 1); -- default: 4194304
SET @GilneanHelmetMask                      = 1 << @Gilnean; -- default: 8388608

-- Important variable update
SET @AllianceMask                          = @AllianceMask     | @GilneanMask;
SET @PlayableRaceMask                      = @PlayableRaceMask | @GilneanMask;
SET @GunHunters                            = @GunHunters       | @GilneanMask;

-- Miscellaneous
SET @GilneanExplorationSound                = @HumanExplorationSound;
SET @GilneanCinematicSequence               = @HumanCinematicSequence;
