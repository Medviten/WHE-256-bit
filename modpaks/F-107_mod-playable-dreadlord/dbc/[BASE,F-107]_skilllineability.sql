-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Dreadlord racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoADreadlordSkillLineAbility1, @CoADreadlordSkillLineAbility2, @CoADreadlordSkillLineAbility3, @CoADreadlordSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoADreadlordSkillLineAbility1, @DreadlordRacials, @CoADreadlordRacial1, @DreadlordMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @DreadlordMask_2), -- Fel-Touched
(@CoADreadlordSkillLineAbility2, @DreadlordRacials, @CoADreadlordRacial2, @DreadlordMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @DreadlordMask_2), -- Nathrezim Might
(@CoADreadlordSkillLineAbility3, @DreadlordRacials, @CoADreadlordRacial3, @DreadlordMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @DreadlordMask_2), -- Vampiric Vigor
(@CoADreadlordSkillLineAbility4, @DreadlordRacials, @CoADreadlordRacial4, @DreadlordMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @DreadlordMask_2); -- Dread Presence
-- <<< CoA Custom 1.9 racials <<<
