-- [F-015] mod-instamount: skilllineability: 1 insert, 0 updates, 0 deletes

-- New entries
-- Learned automatically once Riding reaches 150 (Journeyman) and unlearned below it (acquire method 1 =
-- learned on skill value); the core also applies this on login, so existing characters get it too
DELETE FROM `skilllineability` WHERE `id` IN (@RidingSkill100SkillLineAbility);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
(@RidingSkill100SkillLineAbility, @RidingSkill, @RidingSkill100, 0, 0, 0, 0, 150, 0, 1, 0, 0, 0, 0);
