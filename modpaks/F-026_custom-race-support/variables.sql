-- Important variable updates (Alliance vs. Horde)
SET @ExtendedAllianceMask = @AllianceMask & ~@BaseAllianceMask;
SET @ExtendedHordeMask    = @HordeMask    & ~@BaseHordeMask;

-- Capital reputation spillover (reputation_spillover_faction), same as the stock capitals
SET @CapitalSpilloverRate    = 0.25; -- share of the reputation gain each other capital of the side receives
SET @CapitalSpilloverMaxRank = 7;    -- Exalted: spillover continues up to the top rank
