-- [F-005] mod-azerothcore-high-elf: skilllineability: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @HighElfSkillLineAbility1, @HighElfSkillLineAbility2, @HighElfSkillLineAbility3, @HighElfSkillLineAbility4, @HighElfSkillLineAbility5
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@HighElfSkillLineAbility1, @HighElfRacials, @HighElfRacial1, @HighElfMask, @NonDKMask,       0, 0, 1, 0, 2, 0, 0, 0, 0),
(@HighElfSkillLineAbility2, @HighElfRacials, @HighElfRacial2, @HighElfMask, 0,                0, 0, 1, 0, 2, 0, 0, 0, 0),
(@HighElfSkillLineAbility3, @HighElfRacials, @HighElfRacial3, @HighElfMask, @DeathKnightMask, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(@HighElfSkillLineAbility4, @HighElfRacials, @HighElfRacial4, @HighElfMask, 0,                0, 0, 1, 0, 2, 0, 0, 0, 0),
(@HighElfSkillLineAbility5, @HighElfRacials, @HighElfRacial5, @HighElfMask, 0,                0, 0, 1, 0, 2, 0, 0, 0, 0);
