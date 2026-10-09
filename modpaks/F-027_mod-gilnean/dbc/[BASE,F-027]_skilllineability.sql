-- skilllineability: 0 inserts, 0 updates, 0 deletes
/*
-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @GilneanSkillLineAbility1, @GilneanSkillLineAbility2, @GilneanSkillLineAbility3, @GilneanSkillLineAbility4
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@GilneanSkillLineAbility1, @GilneanRacials, @GilneanRacial1, @GilneanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellViciousness
(@GilneanSkillLineAbility2, @GilneanRacials, @GilneanRacial2, @GilneanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellAberration
(@GilneanSkillLineAbility3, @GilneanRacials, @GilneanRacial3, @GilneanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellFlayer
(@GilneanSkillLineAbility4, @GilneanRacials, @GilneanRacial4, @GilneanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- @SpellDarkflight
*/