-- skilllineability: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @GoblinSkillLineAbility1, @GoblinSkillLineAbility2, @GoblinSkillLineAbility3,
    @GoblinSkillLineAbility4, @GoblinSkillLineAbility5, @GoblinSkillLineAbility6
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@GoblinSkillLineAbility1, @GoblinRacials, @GoblinRacial1, @GoblinMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellRocketBarrage
(@GoblinSkillLineAbility2, @GoblinRacials, @GoblinRacial2, @GoblinMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellTimeIsMoney
(@GoblinSkillLineAbility3, @GoblinRacials, @GoblinRacial3, @GoblinMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellBestDealsAnywhere
(@GoblinSkillLineAbility4, @GoblinRacials, @GoblinRacial4, @GoblinMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellBetterLivingThroughChemistry
(@GoblinSkillLineAbility5, @GoblinRacials, @GoblinRacial5, @GoblinMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellPackHobgoblin
(@GoblinSkillLineAbility6, @GoblinRacials, @GoblinRacial6, @GoblinMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- @SpellRocketJump
