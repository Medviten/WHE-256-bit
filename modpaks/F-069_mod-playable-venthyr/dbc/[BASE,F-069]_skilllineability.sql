-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Venthyr racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAVenthyrSkillLineAbility5);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@CoAVenthyrSkillLineAbility5, @VenthyrRacials, @CoAVenthyrRacial5, @VenthyrMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- Anima Frenzy
-- <<< CoA Custom 1.9 racials <<<
