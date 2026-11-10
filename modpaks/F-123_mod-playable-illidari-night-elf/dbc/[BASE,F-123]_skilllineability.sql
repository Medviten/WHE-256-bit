-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Illidari Night Elf racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAIllidariNightElfSkillLineAbility1, @CoAIllidariNightElfSkillLineAbility2, @CoAIllidariNightElfSkillLineAbility3, @CoAIllidariNightElfSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAIllidariNightElfSkillLineAbility1, @IllidariNightElfRacials, @CoAIllidariNightElfRacial1, @IllidariNightElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariNightElfMask_2), -- Mana Break
(@CoAIllidariNightElfSkillLineAbility2, @IllidariNightElfRacials, @CoAIllidariNightElfRacial2, @IllidariNightElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariNightElfMask_2), -- Illidari Shadows
(@CoAIllidariNightElfSkillLineAbility3, @IllidariNightElfRacials, @CoAIllidariNightElfRacial3, @IllidariNightElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariNightElfMask_2), -- Demonbane
(@CoAIllidariNightElfSkillLineAbility4, @IllidariNightElfRacials, @CoAIllidariNightElfRacial4, @IllidariNightElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariNightElfMask_2); -- Demonic Senses
-- <<< CoA Custom 1.9 racials <<<
