-- >>> CoA Custom 1.9 racials (tools/races/coa_racials.py) >>>
-- The Ogre (CoA's Two-Headed Ogre has none of its own) racials, learned with the racial skill line
DELETE FROM `skilllineability` WHERE `id` IN (@CoATwoHeadedOgreSkillLineAbility1, @CoATwoHeadedOgreSkillLineAbility2, @CoATwoHeadedOgreSkillLineAbility3, @CoATwoHeadedOgreSkillLineAbility4);
INSERT INTO `skilllineability` (`id`, `skill_line`, `spell_id`, `required_races`, `required_classes`, `excluded_races`, `excluded_classes`, `min_skill_value`, `spell_parent_id`, `acquire_method`, `skill_grey_level`, `skill_yellow_level`, `character_points_1`, `character_points_2`, `required_races_2`) VALUES
(@CoATwoHeadedOgreSkillLineAbility1, @TwoHeadedOgreRacials, @CoAOgreRacial1, @TwoHeadedOgreMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TwoHeadedOgreMask_2), -- Ogre Slam
(@CoATwoHeadedOgreSkillLineAbility2, @TwoHeadedOgreRacials, @CoAOgreRacial2, @TwoHeadedOgreMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TwoHeadedOgreMask_2), -- Two Heads Are Better
(@CoATwoHeadedOgreSkillLineAbility3, @TwoHeadedOgreRacials, @CoAOgreRacial3, @TwoHeadedOgreMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TwoHeadedOgreMask_2), -- Thick Skull
(@CoATwoHeadedOgreSkillLineAbility4, @TwoHeadedOgreRacials, @CoAOgreRacial4, @TwoHeadedOgreMask, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, @TwoHeadedOgreMask_2); -- Club Mastery
-- <<< CoA Custom 1.9 racials <<<
