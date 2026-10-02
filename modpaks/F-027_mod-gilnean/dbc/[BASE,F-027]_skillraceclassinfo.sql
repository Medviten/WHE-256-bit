-- skillraceclassinfo: 2 inserts, 30 updates, 0 deletes

-- New entries
DELETE FROM `skillraceclassinfo` WHERE `id` = @GilneanRacialSkillRaceClass; -- Gilnean racials
INSERT INTO `skillraceclassinfo` (`id`, `skill_id`, `race_mask`, `class_mask`, `flags`, `min_level`, `skill_tier_id`, `skill_cost_id`) VALUES (
    @GilneanRacialSkillRaceClass, @GilneanRacials, @GilneanMask, @AllClassMask, 1170, 0, 0, 0
);
