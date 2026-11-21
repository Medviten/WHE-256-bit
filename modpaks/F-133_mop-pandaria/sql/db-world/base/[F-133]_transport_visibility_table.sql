-- Same definition as the core patch's pending update (patches/core/transport-visibility.patch), for world dumps taken
-- before the worldserver created the table.
-- Transports only players who have rewarded a quest see: a row hides transport `entry` (gameobject_template, type 15)
-- from everyone without `quest` rewarded, its passengers excepted. Rewarding the quest shows it at once.
CREATE TABLE IF NOT EXISTS `transport_visibility` (
    `entry` INT UNSIGNED NOT NULL COMMENT 'gameobject_template entry of the transport',
    `quest` INT UNSIGNED NOT NULL COMMENT 'quest_template id the player must have rewarded to see it',
    PRIMARY KEY (`entry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Transports shown only after a quest';
