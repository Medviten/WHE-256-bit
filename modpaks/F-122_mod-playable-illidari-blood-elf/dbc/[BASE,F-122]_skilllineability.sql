-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Illidari Blood Elf racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAIllidariBloodElfSkillLineAbility1, @CoAIllidariBloodElfSkillLineAbility2, @CoAIllidariBloodElfSkillLineAbility3, @CoAIllidariBloodElfSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAIllidariBloodElfSkillLineAbility1, @IllidariBloodElfRacials, @CoAFelElfRacial1, @IllidariBloodElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariBloodElfMask_2), -- Spectral Sight
(@CoAIllidariBloodElfSkillLineAbility2, @IllidariBloodElfRacials, @CoAFelElfRacial2, @IllidariBloodElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariBloodElfMask_2), -- Fel Rush
(@CoAIllidariBloodElfSkillLineAbility3, @IllidariBloodElfRacials, @CoAFelElfRacial3, @IllidariBloodElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariBloodElfMask_2), -- Demon Hunter's Resolve
(@CoAIllidariBloodElfSkillLineAbility4, @IllidariBloodElfRacials, @CoAFelElfRacial4, @IllidariBloodElfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @IllidariBloodElfMask_2); -- Felblood
-- <<< CoA Custom 1.9 racials <<<
