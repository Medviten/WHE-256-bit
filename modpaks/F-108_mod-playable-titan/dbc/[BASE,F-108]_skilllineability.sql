-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Titan racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoATitanSkillLineAbility1, @CoATitanSkillLineAbility2, @CoATitanSkillLineAbility3, @CoATitanSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoATitanSkillLineAbility1, @TitanRacials, @CoATitanRacial1, @TitanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TitanMask_2), -- Keeper's Fortitude
(@CoATitanSkillLineAbility2, @TitanRacials, @CoATitanRacial2, @TitanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TitanMask_2), -- Order Unyielding
(@CoATitanSkillLineAbility3, @TitanRacials, @CoATitanRacial3, @TitanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TitanMask_2), -- Titan-forged Might
(@CoATitanSkillLineAbility4, @TitanRacials, @CoATitanRacial4, @TitanMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TitanMask_2); -- Aegis of the Keepers
-- <<< CoA Custom 1.9 racials <<<
