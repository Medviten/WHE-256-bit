/*
-- All skill-line abilities available to Tauren are also valid for Highmountain Tauren.
UPDATE `skilllineability` SET `required_races` = `required_races` | @HighmountainTaurenMask
WHERE (`required_races` & @TaurenMask) <> 0;
*/