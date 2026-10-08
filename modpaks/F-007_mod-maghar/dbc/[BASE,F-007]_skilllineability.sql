-- [F-007] mod-maghar: skilllineability: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @MagharOrcSkillLineAbility1, @MagharOrcSkillLineAbility2, @MagharOrcSkillLineAbility3, @MagharOrcSkillLineAbility4
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@MagharOrcSkillLineAbility1, @MagharOrcRacials, @MagharOrcRacial1, @MagharOrcMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellAncestralCall
(@MagharOrcSkillLineAbility2, @MagharOrcRacials, @MagharOrcRacial2, @MagharOrcMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellSavageBlood
(@MagharOrcSkillLineAbility3, @MagharOrcRacials, @MagharOrcRacial4, @MagharOrcMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellSympatheticVigor
(@MagharOrcSkillLineAbility4, @MagharOrcRacials, @MagharOrcRacial5, @MagharOrcMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- @SpellOpenSkies
