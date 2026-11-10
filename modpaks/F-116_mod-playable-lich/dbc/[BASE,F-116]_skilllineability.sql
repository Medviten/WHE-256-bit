-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Lich racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoALichSkillLineAbility1, @CoALichSkillLineAbility2, @CoALichSkillLineAbility3, @CoALichSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoALichSkillLineAbility1, @LichRacials, @CoALichRacial1, @LichMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LichMask_2), -- Necrotic Aura
(@CoALichSkillLineAbility2, @LichRacials, @CoALichRacial2, @LichMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LichMask_2), -- Arcane Scholar
(@CoALichSkillLineAbility3, @LichRacials, @CoALichRacial3, @LichMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LichMask_2), -- Deathless Resolve
(@CoALichSkillLineAbility4, @LichRacials, @CoALichRacial4, @LichMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @LichMask_2); -- Necrotic Ward
-- <<< CoA Custom 1.9 racials <<<
