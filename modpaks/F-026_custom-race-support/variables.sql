-- Important variable updates (Alliance vs. Horde)
SET @ExtendedAllianceMask = @AllianceMask & ~@BaseAllianceMask;
SET @ExtendedHordeMask    = @HordeMask    & ~@BaseHordeMask;
