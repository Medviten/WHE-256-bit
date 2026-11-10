-- skillraceclassinfo: 1 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skillraceclassinfo` WHERE `id` = @SurekiRacialSkillRaceClass;
INSERT INTO `skillraceclassinfo` (`id`, `skill_id`, `race_mask`, `class_mask`, `flags`, `min_level`, `skill_tier_id`, `skill_cost_id`) VALUES
(@SurekiRacialSkillRaceClass, @SurekiRacials, @SurekiMask, @AllClassMask, 1170, 0, 0, 0);
