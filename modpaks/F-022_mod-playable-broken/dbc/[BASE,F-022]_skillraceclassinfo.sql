-- [F-022] mod-azerothcore-high-elf: skillraceclassinfo: 1 inserts, 104 updates, 0 deletes

-- Give Dark Iron every skill permission a normal draenei has.
UPDATE `skillraceclassinfo` SET `race_mask` = `race_mask` | @BrokenMask
WHERE (`race_mask` & @DraeneiMask) <> 0;

-- Dedicated racial skill line.
DELETE FROM `skillraceclassinfo` WHERE `id` = @BrokenRacialSkillRaceClass;
INSERT INTO `skillraceclassinfo` (`id`, `skill_id`, `race_mask`, `class_mask`, `flags`, `min_level`, `skill_tier_id`, `skill_cost_id`)
VALUES (@BrokenRacialSkillRaceClass, @BrokenRacials, @BrokenMask, @AllClassMask, 1170, 0, 0, 0);
