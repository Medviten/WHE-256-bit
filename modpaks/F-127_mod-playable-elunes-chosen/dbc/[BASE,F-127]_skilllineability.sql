-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Elune's Chosen racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAEluneChosenSkillLineAbility1, @CoAEluneChosenSkillLineAbility2, @CoAEluneChosenSkillLineAbility3, @CoAEluneChosenSkillLineAbility4, @CoAEluneChosenSkillLineAbility5, @CoAEluneChosenSkillLineAbility6);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAEluneChosenSkillLineAbility1, @EluneChosenRacials, @CoAEluneChosenRacial1, @EluneChosenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @EluneChosenMask_2), -- Moonlit Ward
(@CoAEluneChosenSkillLineAbility2, @EluneChosenRacials, @CoAEluneChosenRacial2, @EluneChosenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @EluneChosenMask_2), -- Starlit Stride
(@CoAEluneChosenSkillLineAbility3, @EluneChosenRacials, @CoAEluneChosenRacial3, @EluneChosenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @EluneChosenMask_2), -- Veil of Elune
(@CoAEluneChosenSkillLineAbility4, @EluneChosenRacials, @CoAEluneChosenRacial4, @EluneChosenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @EluneChosenMask_2), -- Moonlit Resolve
(@CoAEluneChosenSkillLineAbility5, @EluneChosenRacials, @CoAEluneChosenRacial5, @EluneChosenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @EluneChosenMask_2), -- Elune's Embrace
(@CoAEluneChosenSkillLineAbility6, @EluneChosenRacials, @CoAEluneChosenRacial6, @EluneChosenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @EluneChosenMask_2); -- Moonlit Veil
-- <<< CoA Custom 1.9 racials <<<
