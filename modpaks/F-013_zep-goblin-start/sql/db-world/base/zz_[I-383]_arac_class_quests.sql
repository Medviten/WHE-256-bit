-- [I-383] Kezan practice quests for ARAC's goblin paladins and druids.
--
-- Kezan's class trainers each give a level-4 practice quest (14007-14013, [I-273]). With F-029, whose paladin and
-- druid trainers stand beside Sister Goldskimmer ([I-380]), those classes get one too:
--   91416 paladin: The Power of the Light - Judgement on a Training Dummy (Brother Brix Gearlight)
--   91417 druid:   Rejuvenating Touch - Rejuvenation on Injured Employees (Fernie Mossgrubber)
-- The trainers' templates exist without F-029 too (only their spawns go), so the quests do; nobody offers them then.
-- Credit rows on the dummy and the employees are ids 3000+ ([I-273]'s rank copies are 2000+).

DELETE FROM `quest_template` WHERE `ID` IN (91416, 91417);
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `RewardXPDifficulty`,
  `RewardMoneyDifficulty`, `AllowableRaces`, `AllowableRaces_2`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`,
  `ObjectiveText1`, `LogTitle`, `LogDescription`, `QuestDescription`) VALUES
(91416, 2, 4, 4, -141, 3, 60, @GoblinMask, @GoblinMask_2, 48304, 1, 'Practiced Judgement', 'The Power of the Light',
 'Speak with Brother Brix Gearlight and train Judgement. Cast a Seal on yourself, then use Judgement on a Training Dummy.',
 'Brother Brix Gearlight, at your service, $g sir : ma''am;. Yes, a goblin paladin. The Light doesn''t check your bank balance, which frankly is its only flaw.$B$BI think you''ll gain a great deal by me teaching you Judgement. Bind the Light to your weapon with a Seal, then let it loose on whatever''s in front of you. Excellent return on investment.$B$BLearn it from me and then go try it on a training dummy to the southeast.'),
(91417, 2, 4, 4, -263, 3, 60, @GoblinMask, @GoblinMask_2, 48305, 2, 'Practice Rejuvenation on Injured Employee',
 'Rejuvenating Touch',
 'Speak with Fernie Mossgrubber and train Rejuvenation. Practice casting Rejuvenation 2 times on Injured Employees.',
 'Fernie Mossgrubber. I keep the plants alive on this rock, which is harder than it sounds when everyone around you is trying to blow something up.$B$BThe same green power that grows a fern can close a wound, slowly and surely. Let me teach you Rejuvenation. Then go and use it on the injured employees around the courtyard. There''s never a shortage of them.');

DELETE FROM `quest_template_addon` WHERE `ID` IN (91416, 91417);
INSERT INTO `quest_template_addon` (`ID`, `AllowableClasses`) VALUES (91416, 2), (91417, 1024);
DELETE FROM `quest_request_items` WHERE `ID` IN (91416, 91417);
INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`) VALUES
(91416, 1, 1, 'Has the Light paid out yet?'), (91417, 1, 1, 'Feeling green yet?');
DELETE FROM `quest_offer_reward` WHERE `ID` IN (91416, 91417);
INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `RewardText`) VALUES
(91416, 4, 'There you go! Holy power, applied directly to the problem. Come back anytime you want more training.'),
(91417, 4, 'Look at that, they''re back on their feet and back on the clock. Come back when you want to learn more.');

DELETE FROM `creature_queststarter` WHERE `quest` IN (91416, 91417);
INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES (@KezanPaladinTrainerCreatureID, 91416), (@KezanDruidTrainerCreatureID, 91417);
DELETE FROM `creature_questender` WHERE `quest` IN (91416, 91417);
INSERT INTO `creature_questender` (`id`, `quest`) VALUES (@KezanPaladinTrainerCreatureID, 91416), (@KezanDruidTrainerCreatureID, 91417);

-- Credit: any Judgement on the Training Dummy, any Rejuvenation rank on an Injured Employee
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (48304, 48305) AND `id` BETWEEN 3000 AND 3099;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`,
  `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`,
  `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`,
  `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`)
SELECT s.npc, 0, 3000 + s.n, 0, 8, 0, 100, 0, s.spell, 0, 0, 0, 0, 0, 33, s.npc, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0,
  CONCAT('quest ', s.quest, ': credit when hit by ', s.spell, ' (I-383)')
FROM (SELECT 48304 npc, 0 n, 20271 spell, 91416 quest UNION ALL SELECT 48304, 1, 53407, 91416
      UNION ALL SELECT 48304, 2, 53408, 91416
      UNION ALL SELECT 48305, 0, 774, 91417 UNION ALL SELECT 48305, 1, 1058, 91417 UNION ALL SELECT 48305, 2, 1430, 91417
      UNION ALL SELECT 48305, 3, 2090, 91417 UNION ALL SELECT 48305, 4, 2091, 91417 UNION ALL SELECT 48305, 5, 3627, 91417
      UNION ALL SELECT 48305, 6, 8910, 91417 UNION ALL SELECT 48305, 7, 9839, 91417 UNION ALL SELECT 48305, 8, 9840, 91417
      UNION ALL SELECT 48305, 9, 9841, 91417 UNION ALL SELECT 48305, 10, 25299, 91417 UNION ALL SELECT 48305, 11, 26981, 91417
      UNION ALL SELECT 48305, 12, 26982, 91417 UNION ALL SELECT 48305, 13, 48440, 91417 UNION ALL SELECT 48305, 14, 48441, 91417) s;
