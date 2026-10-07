/* Add goblin rocket barrage racial ability */
DELETE FROM `spell_script_names` WHERE `spell_id` = @SpellRocketBarrage;
INSERT INTO `spell_script_names` (`spell_id`, `ScriptName`) VALUES
(@SpellRocketBarrage, 'spell_rocket_barrage');
