-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Lost One racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoALostOneSkillLineAbility1, @CoALostOneSkillLineAbility2, @CoALostOneSkillLineAbility3, @CoALostOneSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoALostOneSkillLineAbility1, @LostOneRacials, @CoALostOneRacial1, @LostOneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LostOneMask_2), -- Lost to the Void
(@CoALostOneSkillLineAbility2, @LostOneRacials, @CoALostOneRacial2, @LostOneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LostOneMask_2), -- Spectral Pace
(@CoALostOneSkillLineAbility3, @LostOneRacials, @CoALostOneRacial3, @LostOneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LostOneMask_2), -- Echo of the Light
(@CoALostOneSkillLineAbility4, @LostOneRacials, @CoALostOneRacial4, @LostOneMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LostOneMask_2); -- Ghostly Dispersion
-- <<< CoA Custom 1.9 racials <<<
