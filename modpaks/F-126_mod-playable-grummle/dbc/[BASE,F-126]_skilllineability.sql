-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Grummle racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAGrummleSkillLineAbility1, @CoAGrummleSkillLineAbility2, @CoAGrummleSkillLineAbility3, @CoAGrummleSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAGrummleSkillLineAbility1, @GrummleRacials, @CoAGrummleRacial1, @GrummleMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @GrummleMask_2), -- Pack Toss
(@CoAGrummleSkillLineAbility2, @GrummleRacials, @CoAGrummleRacial2, @GrummleMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @GrummleMask_2), -- Trail Snack
(@CoAGrummleSkillLineAbility3, @GrummleRacials, @CoAGrummleRacial3, @GrummleMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @GrummleMask_2), -- Lucky Foot
(@CoAGrummleSkillLineAbility4, @GrummleRacials, @CoAGrummleRacial4, @GrummleMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @GrummleMask_2); -- Heavy Pack
-- <<< CoA Custom 1.9 racials <<<
