-- skilllineability: 4 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @WorgenSkillLineAbility1, @WorgenSkillLineAbility2, @WorgenSkillLineAbility3, @WorgenSkillLineAbility4
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@WorgenSkillLineAbility1, @WorgenRacials, @WorgenRacial1, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellViciousness
(@WorgenSkillLineAbility2, @WorgenRacials, @WorgenRacial2, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellAberration
(@WorgenSkillLineAbility3, @WorgenRacials, @WorgenRacial3, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- @SpellFlayer
(@WorgenSkillLineAbility4, @WorgenRacials, @WorgenRacial4, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- @SpellDarkflight

-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Worgen racials, learned with the racial skill line
-- Commented out: the race already has its Cataclysm racials. Remove the comment markers to give the race CoA's racials instead.
/*
DELETE FROM `skilllineability` WHERE `id` IN (@CoAWorgenSkillLineAbility1, @CoAWorgenSkillLineAbility2, @CoAWorgenSkillLineAbility3, @CoAWorgenSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@CoAWorgenSkillLineAbility1, @WorgenRacials, @CoAWorgenRacial1, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Darkflight
(@CoAWorgenSkillLineAbility2, @WorgenRacials, @CoAWorgenRacial2, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Two Forms
(@CoAWorgenSkillLineAbility3, @WorgenRacials, @CoAWorgenRacial3, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Viciousness
(@CoAWorgenSkillLineAbility4, @WorgenRacials, @CoAWorgenRacial4, @WorgenMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- Aberration
*/
-- <<< CoA Custom 1.9 racials <<<
