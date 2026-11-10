-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Nerubian racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoANerubianSkillLineAbility1, @CoANerubianSkillLineAbility2, @CoANerubianSkillLineAbility3, @CoANerubianSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoANerubianSkillLineAbility1, @NerubianRacials, @CoANerubianRacial1, @NerubianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @NerubianMask_2), -- Ancient Chitin
(@CoANerubianSkillLineAbility2, @NerubianRacials, @CoANerubianRacial2, @NerubianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @NerubianMask_2), -- Burrowed Reflexes
(@CoANerubianSkillLineAbility3, @NerubianRacials, @CoANerubianRacial3, @NerubianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @NerubianMask_2), -- Undying Empire
(@CoANerubianSkillLineAbility4, @NerubianRacials, @CoANerubianRacial4, @NerubianMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @NerubianMask_2); -- Carapace Slide
-- <<< CoA Custom 1.9 racials <<<
