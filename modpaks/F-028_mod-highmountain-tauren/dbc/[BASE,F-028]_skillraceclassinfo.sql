-- [F-031] mod-azerothcore-high-elf: skillraceclassinfo: 1 inserts, 104 updates, 0 deletes
/*
-- Give Highmountain every skill permission a normal Tauren has.
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @HighmountainTaurenMask
WHERE (`race_mask` & @TaurenMask) <> 0;
*/
-- Dedicated racial skill line.
-- DELETE FROM `skillraceclassinfo` WHERE `id` = 1143;
-- INSERT INTO `skillraceclassinfo` (`id`, `skill_id`, `race_mask`, `class_mask`, `flags`, `min_level`, `skill_tier_id`, `skill_cost_id`)
-- VALUES (1143, @HighmountainTaurenRacials, @HighmountainTaurenMask, @AllClassMask, 1170, 0, 0, 0);
