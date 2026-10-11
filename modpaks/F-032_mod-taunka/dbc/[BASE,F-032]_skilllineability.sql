-- All skill-line abilities available to Tauren are also valid for Taunka.
UPDATE `skilllineability` SET `required_races` = `required_races` | @TaunkaMask
WHERE (`required_races` & @TaurenMask) <> 0;
