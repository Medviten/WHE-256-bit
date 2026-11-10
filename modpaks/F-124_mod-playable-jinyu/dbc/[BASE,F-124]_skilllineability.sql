-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Jinyu racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAJinyuSkillLineAbility1, @CoAJinyuSkillLineAbility2, @CoAJinyuSkillLineAbility3, @CoAJinyuSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAJinyuSkillLineAbility1, @JinyuRacials, @CoAJinyuRacial1, @JinyuMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @JinyuMask_2), -- Waterspeaker's Blessing
(@CoAJinyuSkillLineAbility2, @JinyuRacials, @CoAJinyuRacial2, @JinyuMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @JinyuMask_2), -- Riptide Escape
(@CoAJinyuSkillLineAbility3, @JinyuRacials, @CoAJinyuRacial3, @JinyuMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @JinyuMask_2), -- Gift of the River
(@CoAJinyuSkillLineAbility4, @JinyuRacials, @CoAJinyuRacial4, @JinyuMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @JinyuMask_2); -- Cold Currents
-- <<< CoA Custom 1.9 racials <<<
