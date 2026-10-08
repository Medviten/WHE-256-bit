-- All skill-line abilities available to normal trolls are also valid for Zandalari.
UPDATE `skilllineability` SET `required_races` = `required_races` | @ZandalariTrollMask
WHERE (`required_races` & @TrollMask) <> 0;

-- skilllineability: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `skilllineability` WHERE `id` IN (
    @ZandalariTrollSkillLineAbility1, @ZandalariTrollSkillLineAbility2, @ZandalariTrollSkillLineAbility3, @ZandalariTrollSkillLineAbility4, @ZandalariTrollSkillLineAbility5
);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`) VALUES
-- (@ZandalariTrollSkillLineAbility1, @ZandalariTrollRacials, @ZandalariTrollRacial1, @ZandalariTrollMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@ZandalariTrollSkillLineAbility2, @ZandalariTrollRacials, @ZandalariTrollRacial2, @ZandalariTrollMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@ZandalariTrollSkillLineAbility3, @ZandalariTrollRacials, @ZandalariTrollRacial3, @ZandalariTrollMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@ZandalariTrollSkillLineAbility4, @ZandalariTrollRacials, @ZandalariTrollRacial4, @ZandalariTrollMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0),
-- (@ZandalariTrollSkillLineAbility5, @ZandalariTrollRacials, @ZandalariTrollRacial5, @ZandalariTrollMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0);
