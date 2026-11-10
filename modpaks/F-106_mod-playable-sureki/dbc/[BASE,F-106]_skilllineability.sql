-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Sureki racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoASurekiSkillLineAbility1, @CoASurekiSkillLineAbility2, @CoASurekiSkillLineAbility3, @CoASurekiSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoASurekiSkillLineAbility1, @SurekiRacials, @CoASurekiRacial1, @SurekiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SurekiMask_2), -- Scholar of the Empire
(@CoASurekiSkillLineAbility2, @SurekiRacials, @CoASurekiRacial2, @SurekiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SurekiMask_2), -- Chitin Plating
(@CoASurekiSkillLineAbility3, @SurekiRacials, @CoASurekiRacial3, @SurekiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SurekiMask_2), -- Spinner's Poise
(@CoASurekiSkillLineAbility4, @SurekiRacials, @CoASurekiRacial4, @SurekiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SurekiMask_2); -- Silkbind
-- <<< CoA Custom 1.9 racials <<<
