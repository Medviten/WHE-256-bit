-- [F-031] mod-azerothcore-high-elf: skillraceclassinfo: 1 inserts, 104 updates, 0 deletes

-- New entries
DELETE FROM `skillraceclassinfo` WHERE `id` = @DarkIronDwarfRacialSkillRaceClass;
INSERT INTO `skillraceclassinfo` (`id`, `skill_id`, `race_mask`, `class_mask`, `flags`, `min_level`, `skill_tier_id`, `skill_cost_id`)
VALUES (
    @DarkIronDwarfRacialSkillRaceClass, @DarkIronDwarfRacials, @DarkIronDwarfMask, @AllClassMask, 1170, 0, 0, 0
);
