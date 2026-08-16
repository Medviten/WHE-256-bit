CREATE TABLE IF NOT EXISTS `custom_race_costumes` (
    `trigger_spell_id` INT UNSIGNED NOT NULL COMMENT 'The spell ID cast by the item/NPC',
    `race` TINYINT UNSIGNED NOT NULL COMMENT 'Target original race ID (0 for any)',
    `gender` TINYINT UNSIGNED NOT NULL COMMENT '0 = Male, 1 = Female, 2 = Both',
    `display_id` INT UNSIGNED NOT NULL COMMENT 'The CreatureDisplayInfo ID to apply',
    PRIMARY KEY (`trigger_spell_id`, `race`, `gender`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

REPLACE INTO `custom_race_costumes` (`trigger_spell_id`, `race`, `gender`, `display_id`) VALUES 
(68994, 0, 0, 94135), -- Gilnean male
(68994, 0, 1, 94136), -- Gilnean female
(110020, 0, 0, 20585), -- Tauren male
(110020, 0, 1, 20584); -- Tauren female

