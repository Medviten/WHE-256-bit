INSERT INTO `spell_script_names` (`spell_id`, `ScriptName`) VALUES
(68994, 'spell_costume_override'),
(110020, 'spell_costume_override')
ON DUPLICATE KEY UPDATE ScriptName = VALUES(ScriptName);