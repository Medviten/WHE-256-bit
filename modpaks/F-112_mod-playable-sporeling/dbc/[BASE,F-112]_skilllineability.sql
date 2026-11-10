-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Sporeling racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoASporelingSkillLineAbility1, @CoASporelingSkillLineAbility2, @CoASporelingSkillLineAbility3, @CoASporelingSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoASporelingSkillLineAbility1, @SporelingRacials, @CoASporelingRacial1, @SporelingMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SporelingMask_2), -- Spore-Blooded
(@CoASporelingSkillLineAbility2, @SporelingRacials, @CoASporelingRacial2, @SporelingMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SporelingMask_2), -- Quick Spores
(@CoASporelingSkillLineAbility3, @SporelingRacials, @CoASporelingRacial3, @SporelingMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SporelingMask_2), -- Mycelial Mind
(@CoASporelingSkillLineAbility4, @SporelingRacials, @CoASporelingRacial4, @SporelingMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @SporelingMask_2); -- Spore Burst
-- <<< CoA Custom 1.9 racials <<<
