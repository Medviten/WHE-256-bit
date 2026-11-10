-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Mogu racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoAMoguSkillLineAbility1, @CoAMoguSkillLineAbility2, @CoAMoguSkillLineAbility3, @CoAMoguSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoAMoguSkillLineAbility1, @MoguRacials, @CoAMoguRacial1, @MoguMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoguMask_2), -- Stoneskin
(@CoAMoguSkillLineAbility2, @MoguRacials, @CoAMoguRacial2, @MoguMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoguMask_2), -- Thunder King's Might
(@CoAMoguSkillLineAbility3, @MoguRacials, @CoAMoguRacial3, @MoguMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoguMask_2), -- Pride of the Mogu
(@CoAMoguSkillLineAbility4, @MoguRacials, @CoAMoguRacial4, @MoguMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @MoguMask_2); -- Stonebreaker Shockwave
-- <<< CoA Custom 1.9 racials <<<
