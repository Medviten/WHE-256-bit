-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Harpy racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAHarpySkillLineAbility1, @CoAHarpySkillLineAbility2, @CoAHarpySkillLineAbility3, @CoAHarpySkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAHarpySkillLineAbility1, @HarpyRacials, @CoAHarpyRacial1, @HarpyMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @HarpyMask_2), -- Wing Gust
(@CoAHarpySkillLineAbility2, @HarpyRacials, @CoAHarpyRacial2, @HarpyMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @HarpyMask_2), -- Screech
(@CoAHarpySkillLineAbility3, @HarpyRacials, @CoAHarpyRacial3, @HarpyMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @HarpyMask_2), -- Swift Talons
(@CoAHarpySkillLineAbility4, @HarpyRacials, @CoAHarpyRacial4, @HarpyMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @HarpyMask_2); -- Keen Eyes
-- <<< CoA Custom 1.9 racials <<<
