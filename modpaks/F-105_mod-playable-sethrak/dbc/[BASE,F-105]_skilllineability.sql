-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Sethrak racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoASethrakSkillLineAbility1, @CoASethrakSkillLineAbility2, @CoASethrakSkillLineAbility3, @CoASethrakSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoASethrakSkillLineAbility1, @SethrakRacials, @CoASethrakRacial1, @SethrakMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SethrakMask_2), -- Serpent's Escape
(@CoASethrakSkillLineAbility2, @SethrakRacials, @CoASethrakRacial2, @SethrakMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SethrakMask_2), -- Venom Blood
(@CoASethrakSkillLineAbility3, @SethrakRacials, @CoASethrakRacial3, @SethrakMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SethrakMask_2), -- Desert Scales
(@CoASethrakSkillLineAbility4, @SethrakRacials, @CoASethrakRacial4, @SethrakMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SethrakMask_2); -- Coiled Strength
-- <<< CoA Custom 1.9 racials <<<
