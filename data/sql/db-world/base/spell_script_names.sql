/* Add goblin rocket barrage racial ability */
DELETE FROM `spell_script_names` WHERE `spell_id` = 69041;
INSERT INTO `spell_script_names` (`spell_id`, `ScriptName`) VALUES (69041, 'spell_rocket_barrage');

INSERT INTO `spell_script_names` (`spell_id`, `ScriptName`) VALUES
(68994, 'spell_costume_override'),
(110020, 'spell_costume_override')
ON DUPLICATE KEY UPDATE ScriptName = VALUES(ScriptName);