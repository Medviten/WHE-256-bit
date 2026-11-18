-- I-388  Players near the Merchant Square stairs were put in combat
--
-- Target Trigger 174740 (by the Gilnean Crows) is hostile (faction 14) so that its "target in range" event, which
-- only runs in combat, can tell the crows to fly off: every player who walked by was pulled into combat with an
-- invisible trigger that then despawned and came back. It is friendly now and uses the out-of-combat line of sight
-- event instead (not hostile, 10 yards, once a second), like the crows' own.

UPDATE `creature_template` SET `faction` = 35 WHERE `entry` = 174740;
UPDATE `smart_scripts` SET `event_type` = 10, `event_param1` = 1, `event_param2` = 10, `event_param3` = 1000,
  `event_param4` = 1000
WHERE `entryorguid` = 174740 AND `source_type` = 0 AND `id` = 0;
