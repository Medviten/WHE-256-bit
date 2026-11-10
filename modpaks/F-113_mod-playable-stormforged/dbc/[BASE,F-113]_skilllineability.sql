-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Stormforged racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAStormforgedSkillLineAbility1, @CoAStormforgedSkillLineAbility2, @CoAStormforgedSkillLineAbility3, @CoAStormforgedSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAStormforgedSkillLineAbility1, @StormforgedRacials, @CoAStormforgedRacial1, @StormforgedMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @StormforgedMask_2), -- Stormborn
(@CoAStormforgedSkillLineAbility2, @StormforgedRacials, @CoAStormforgedRacial2, @StormforgedMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @StormforgedMask_2), -- Vrykul Hide
(@CoAStormforgedSkillLineAbility3, @StormforgedRacials, @CoAStormforgedRacial3, @StormforgedMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @StormforgedMask_2), -- Longship Stride
(@CoAStormforgedSkillLineAbility4, @StormforgedRacials, @CoAStormforgedRacial4, @StormforgedMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @StormforgedMask_2); -- Tempest Call
-- <<< CoA Custom 1.9 racials <<<
