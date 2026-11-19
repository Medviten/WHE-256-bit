-- F-137 Exile's Reach: SmartAI for the ship intro and Darkmaul Citadel, in place of TrinityCore's C++
-- (zone_exiles_reach.cpp, instance_darkmaul_citadel). Hand-written; runs after the generated zz_[AUTO,F-137] files,
-- so the creature_template changes here stay.

-- ---- The ships (both factions) ----------------------------------------------------------------------------------
-- Warming Up: Combat Dummies give the quest's credit (KillCredit1 174954, generated) and don't fight back; faction 7
-- (Creature, attackable) for retail's 2643, which 3.3.5a lacks
UPDATE `creature_template` SET `faction` = 7, `AIName` = 'SmartAI' WHERE `entry` = 160737;
DELETE FROM `smart_scripts` WHERE `entryorguid` = 160737 AND `source_type` = 0;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
  (160737, 0, 0, 0, 25, 0, 100, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Combat Dummy - On reset - Set react state passive');

-- Stand Your Ground: Private Cole (Alliance) and Grunt Throg (Horde) spar with whoever takes the quest and yield at
-- 30% health, crediting their opponent (155607, the quest's spar credit)
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (160664, 166583);
DELETE FROM `smart_scripts` WHERE `entryorguid` IN (160664, 166583) AND `source_type` = 0;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
  (160664, 0, 0, 1, 19, 0, 100, 0, 58209, 0, 0, 0, 0, 0, 2, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Private Cole - On Stand Your Ground accepted - Turn hostile'),
  (160664, 0, 1, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Private Cole - Linked - Attack the player'),
  (160664, 0, 2, 3, 2, 0, 100, 0, 0, 30, 1000, 1000, 0, 0, 33, 155607, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Private Cole - At 30% health - Spar credit to his opponent'),
  (160664, 0, 3, 4, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Private Cole - Linked - Default faction'),
  (160664, 0, 4, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Private Cole - Linked - Evade'),
  (166583, 0, 0, 1, 19, 0, 100, 0, 59927, 0, 0, 0, 0, 0, 2, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grunt Throg - On Stand Your Ground accepted - Turn hostile'),
  (166583, 0, 1, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Grunt Throg - Linked - Attack the player'),
  (166583, 0, 2, 3, 2, 0, 100, 0, 0, 30, 1000, 1000, 0, 0, 33, 155607, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 'Grunt Throg - At 30% health - Spar credit to his opponent'),
  (166583, 0, 3, 4, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grunt Throg - Linked - Default faction'),
  (166583, 0, 4, 0, 61, 0, 100, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Grunt Throg - Linked - Evade');

-- Brace for Impact: turning it in on deck wrecks the ship; retail plays the crash scene and wakes you on the beach
-- (TrinityCore's spells 305425 / 325131 land at the same spot), here the turn-in teleports you there
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (156280, 166827);
DELETE FROM `smart_scripts` WHERE `entryorguid` IN (156280, 166827) AND `source_type` = 0;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
  (156280, 0, 0, 0, 20, 0, 100, 0, 58208, 0, 0, 0, 0, 0, 62, 2175, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, -462.4, -2619.8, 0.4, 0.53, 'Lady Jaina Proudmoore - On Brace for Impact rewarded - Shipwrecked: to the beach'),
  (166827, 0, 0, 0, 20, 0, 100, 0, 59928, 0, 0, 0, 0, 0, 62, 2175, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, -462.4, -2619.8, 0.4, 0.53, 'Thrall - On Brace for Impact rewarded - Shipwrecked: to the beach');

-- ---- Darkmaul Citadel --------------------------------------------------------------------------------------------
-- Gor'groth: TrinityCore's script makes him attackable when his ritual starts; here he is from the start. His kill
-- stands in for "Gor'groth's final ritual stopped" (generated objective)
UPDATE `creature_template` SET `unit_flags` = 0 WHERE `entry` = 156814;

-- Kalecgos, Gor'groth's captive: talking to him credits "Speak with Kalecgos to leave Darkmaul Citadel" (Alliance
-- 161350, Horde 167663) and takes the player out to the citadel's gate. There Kalecgos (244389, spawned at Wowhead's
-- point) credits An End to Beginnings' "Speak to Kalecgos to travel" and sends the player to their capital, bound
-- there, where Captain Garrick / Warlord Breka Grimaxe end it (core: exiles_reach_start.cpp, exiles-reach-start.patch)
UPDATE `creature_template` SET `faction` = 35, `unit_flags` = 0, `npcflag` = `npcflag` | 1, `AIName` = '', `ScriptName` = 'npc_darkmaul_kalecgos' WHERE `entry` = 156501;
UPDATE `creature_template` SET `npcflag` = `npcflag` | 1, `AIName` = '', `ScriptName` = 'npc_exiles_reach_kalecgos' WHERE `entry` = 244389;
DELETE FROM `smart_scripts` WHERE `entryorguid` IN (156501, 244389) AND `source_type` = 0;
