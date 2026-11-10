-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Fungarian racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAFungarianSkillLineAbility1, @CoAFungarianSkillLineAbility2, @CoAFungarianSkillLineAbility3, @CoAFungarianSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAFungarianSkillLineAbility1, @FungarianRacials, @CoAFungarianRacial1, @FungarianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @FungarianMask_2), -- Mycelial Hide
(@CoAFungarianSkillLineAbility2, @FungarianRacials, @CoAFungarianRacial2, @FungarianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @FungarianMask_2), -- Network of Minds
(@CoAFungarianSkillLineAbility3, @FungarianRacials, @CoAFungarianRacial3, @FungarianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @FungarianMask_2), -- Rooted Resilience
(@CoAFungarianSkillLineAbility4, @FungarianRacials, @CoAFungarianRacial4, @FungarianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @FungarianMask_2); -- Sporebloom Circle
-- <<< CoA Custom 1.9 racials <<<
