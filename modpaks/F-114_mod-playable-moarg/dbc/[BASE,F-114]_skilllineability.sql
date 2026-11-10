-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Mo'arg racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAMoargSkillLineAbility1, @CoAMoargSkillLineAbility2, @CoAMoargSkillLineAbility3, @CoAMoargSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAMoargSkillLineAbility1, @MoargRacials, @CoAMoargRacial1, @MoargMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoargMask_2), -- Felforged Plating
(@CoAMoargSkillLineAbility2, @MoargRacials, @CoAMoargRacial2, @MoargMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoargMask_2), -- Tinker's Mind
(@CoAMoargSkillLineAbility3, @MoargRacials, @CoAMoargRacial3, @MoargMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoargMask_2), -- Overclocked Legs
(@CoAMoargSkillLineAbility4, @MoargRacials, @CoAMoargRacial4, @MoargMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoargMask_2); -- Felfire Barrage
-- <<< CoA Custom 1.9 racials <<<
