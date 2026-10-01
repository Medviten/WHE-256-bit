-- skilllineability: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @DarkIronDwarfSkillLineAbility1, @DarkIronDwarfSkillLineAbility2, @DarkIronDwarfSkillLineAbility3, @DarkIronDwarfSkillLineAbility4, @DarkIronDwarfSkillLineAbility5
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
-- (@DarkIronDwarfSkillLineAbility1, @DarkIronDwarfRacials, @DarkIronDwarfRacial1, @DarkIronDwarfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@DarkIronDwarfSkillLineAbility2, @DarkIronDwarfRacials, @DarkIronDwarfRacial2, @DarkIronDwarfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@DarkIronDwarfSkillLineAbility3, @DarkIronDwarfRacials, @DarkIronDwarfRacial3, @DarkIronDwarfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@DarkIronDwarfSkillLineAbility4, @DarkIronDwarfRacials, @DarkIronDwarfRacial4, @DarkIronDwarfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(@DarkIronDwarfSkillLineAbility5, @DarkIronDwarfRacials, @DarkIronDwarfRacial5, @DarkIronDwarfMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);

/*
-- Dark Iron racial spell links. Uses stable WotLK dwarf racial spell IDs.
DELETE FROM `skilllineability` WHERE `id` BETWEEN 31550 AND 31554;
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(31550, @DarkIronDwarfRacials, @DarkIronDwarfRacial1, @DarkIronDwarfMask, @AllClassMask, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(31551, @DarkIronDwarfRacials, @DarkIronDwarfRacial2, @DarkIronDwarfMask, @AllClassMask, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(31552, @DarkIronDwarfRacials, @DarkIronDwarfRacial3, @DarkIronDwarfMask, @AllClassMask, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(31553, @DarkIronDwarfRacials, @DarkIronDwarfRacial4, @DarkIronDwarfMask, @AllClassMask, 0, 0, 1, 0, 2, 0, 0, 0, 0),
(31554, @DarkIronDwarfRacials, @DarkIronDwarfRacial5, @DarkIronDwarfMask, @AllClassMask, 0, 0, 1, 0, 2, 0, 0, 0, 0);
-- All skill-line abilities available to normal dwarves are also valid for Dark Iron.
UPDATE `skilllineability` SET `required_races` = `required_races` | @DarkIronDwarfMask
WHERE (`required_races` & @DwarfMask) <> 0;
*/
