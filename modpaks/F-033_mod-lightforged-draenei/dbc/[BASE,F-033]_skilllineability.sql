-- skilllineability: 4 inserts, 0 updates, 0 deletes
/*
-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @LightforgedDraeneiSkillLineAbility1, @LightforgedDraeneiSkillLineAbility2, @LightforgedDraeneiSkillLineAbility3, @LightforgedDraeneiSkillLineAbility4, @LightforgedDraeneiSkillLineAbility5
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@LightforgedDraeneiSkillLineAbility1, @LightforgedDraeneiRacials, @LightforgedDraeneiRacial1, @LightforgedDraeneiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(@LightforgedDraeneiSkillLineAbility2, @LightforgedDraeneiRacials, @LightforgedDraeneiRacial2, @LightforgedDraeneiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(@LightforgedDraeneiSkillLineAbility3, @LightforgedDraeneiRacials, @LightforgedDraeneiRacial3, @LightforgedDraeneiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(@LightforgedDraeneiSkillLineAbility4, @LightforgedDraeneiRacials, @LightforgedDraeneiRacial4, @LightforgedDraeneiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);
(@LightforgedDraeneiSkillLineAbility5, @LightforgedDraeneiRacials, @LightforgedDraeneiRacial5, @LightforgedDraeneiMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);
*/