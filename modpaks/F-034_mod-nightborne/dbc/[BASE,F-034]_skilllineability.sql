-- skilllineability: 7 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @NightborneSkillLineAbility1, @NightborneSkillLineAbility2,
    @NightborneSkillLineAbility3, @NightborneSkillLineAbility4,
    @NightborneSkillLineAbility5, @NightborneSkillLineAbility6
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
-- (@NightborneSkillLineAbility1, @NightborneRacials, @NightborneRacial1, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@NightborneSkillLineAbility2, @NightborneRacials, @NightborneRacial2, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@NightborneSkillLineAbility3, @NightborneRacials, @NightborneRacial3, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@NightborneSkillLineAbility4, @NightborneRacials, @NightborneRacial4, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@NightborneSkillLineAbility5, @NightborneRacials, @NightborneRacial5, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);
-- (@NightborneSkillLineAbility6, @NightborneRacials, @NightborneRacial6, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);
-- (@NightborneSkillLineAbility7, @NightborneRacials, @NightborneRacial7, @NightborneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);
