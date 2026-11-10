-- skilllineability: the Pandaren racials. The race mask only holds the NPC race: a mask of 0 would mean every race. F-020 and F-021 add theirs

-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Pandaren racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoANeutralPandarenSkillLineAbility1, @CoANeutralPandarenSkillLineAbility2, @CoANeutralPandarenSkillLineAbility3, @CoANeutralPandarenSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@CoANeutralPandarenSkillLineAbility1, @NeutralPandarenRacials, @CoANeutralPandarenRacial1, @NeutralPandarenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Quaking Palm
(@CoANeutralPandarenSkillLineAbility2, @NeutralPandarenRacials, @CoANeutralPandarenRacial2, @NeutralPandarenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Inner Peace
(@CoANeutralPandarenSkillLineAbility3, @NeutralPandarenRacials, @CoANeutralPandarenRacial3, @NeutralPandarenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Bouncy
(@CoANeutralPandarenSkillLineAbility4, @NeutralPandarenRacials, @CoANeutralPandarenRacial4, @NeutralPandarenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- Gourmand
-- <<< CoA Custom 1.9 racials <<<
