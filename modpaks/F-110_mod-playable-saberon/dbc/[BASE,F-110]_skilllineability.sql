-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Saberon racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoASaberonSkillLineAbility1, @CoASaberonSkillLineAbility2, @CoASaberonSkillLineAbility3, @CoASaberonSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoASaberonSkillLineAbility1, @SaberonRacials, @CoASaberonRacial1, @SaberonMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SaberonMask_2), -- Pounce
(@CoASaberonSkillLineAbility2, @SaberonRacials, @CoASaberonRacial2, @SaberonMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SaberonMask_2), -- Feline Grace
(@CoASaberonSkillLineAbility3, @SaberonRacials, @CoASaberonRacial3, @SaberonMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SaberonMask_2), -- Predator
(@CoASaberonSkillLineAbility4, @SaberonRacials, @CoASaberonRacial4, @SaberonMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SaberonMask_2); -- Shadow Prowl
-- <<< CoA Custom 1.9 racials <<<
