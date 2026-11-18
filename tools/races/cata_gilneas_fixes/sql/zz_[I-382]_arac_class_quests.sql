-- [I-382] Gilneas class quests for ARAC's Worgen paladins and shamans.
--
-- The seven Cataclysm classes get a three-step chain in Gilneas City: Gwen Armstead sends them to their trainer, the
-- trainer has them practise a spell on a Bloodfang Worgen, and "Safety in Numbers" takes them to King Genn Greymane
-- (which Old Divisions and While You're At It need). With F-029, whose paladin and shaman trainers stand beside Sister
-- Almyra ([I-379]), paladins and shamans get the same chain, at the native one's levels and XP ([I-378]):
--   91410-91412 paladin: The Light Endures -> The Power of the Light (Judgement) -> Safety in Numbers
--   91413-91415 shaman:  The Old Ways -> Earth Shock -> Safety in Numbers
-- Without F-029 there is no trainer to send them to: Gwen doesn't offer the lead-ins and [I-379] lets those classes
-- through instead. Also here: the shaman trainer gives F-002's Call of Earth (92801), the level-4 Earth Totem quest
-- ARAC's shamans otherwise get from Firmanvaar, whom Worgen can't reach before leaving Gilneas.
--
-- Loads after [I-378] (whose rank copies on Bloodfang Worgen are ids 2000+) and [I-379]; credit rows are ids 3000+.

SET @GilneasAracTrainers = COALESCE(@AllTrainersEnabled, 0) <> 0;
SET @Gwen = 35840, @Greymane = 35112, @Bloodfang = 35118;

DELETE FROM `quest_template` WHERE `ID` BETWEEN 91410 AND 91415;
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `RewardNextQuest`, `RewardXPDifficulty`,
  `RewardMoney`, `RewardMoneyDifficulty`, `AllowableRaces`, `AllowableRaces_2`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`,
  `ObjectiveText1`, `LogTitle`, `LogDescription`, `QuestDescription`, `QuestCompletionLog`) VALUES
(91410, 2, 4, 1, 4714, 91411, 8, 105, 160, @WorgenMask, @WorgenMask_2, 0, 0, '', 'The Light Endures',
 'Speak to Brother Aldous Harrow in the Military District.',
 'Most of us made it here alive... but there are worgen on this side of the city as well.$B$BWe''re going to continue heading south once everyone''s accounted for.$B$BThat reminds me, someone was asking about you. Brother Aldous Harrow, of the cathedral. He said the Light had kept you alive for a reason, and that he meant to find out what it was.',
 ''),
(91411, 2, 4, 4, 4714, 91412, 3, 0, 130, @WorgenMask, @WorgenMask_2, @Bloodfang, 1, 'Practice Judgement',
 'The Power of the Light',
 'Speak to Brother Aldous Harrow and learn Judgement. Cast a Seal on yourself, then use Judgement on a Bloodfang Worgen.',
 'You came through the gates alive, $N. Not many did.$B$BThe Light does not abandon those who stand their ground. Let me show you how to carry it into battle: a Seal to bind its power to your blade, and Judgement to unleash it upon your foe.$B$BLearn it from me, then try it on the bloodfang worgen to our west.',
 ''),
(91412, 2, 3, 1, 4714, 0, 2, 83, 100, @WorgenMask, @WorgenMask_2, 0, 0, '', 'Safety in Numbers',
 'Speak to King Genn Greymane in the military district.',
 'I''ve taught you all that is practical for now.$B$BIt is time we joined with the other survivors. The others mentioned that King Greymane and his royal guard are just south of here.$B$BGo to him. A shield is no use standing alone.',
 ''),
(91413, 2, 4, 1, 4714, 91414, 8, 105, 160, @WorgenMask, @WorgenMask_2, 0, 0, '', 'The Old Ways',
 'Speak to Edwin Thornfield in the Military District.',
 'Most of us made it here alive... but there are worgen on this side of the city as well.$B$BWe''re going to continue heading south once everyone''s accounted for.$B$BThat reminds me, someone was asking about you. Old Edwin Thornfield, the one the farmers go to when the harvest fails. He said the earth itself had told him you were coming. Make of that what you will.',
 ''),
(91414, 2, 4, 4, 4714, 91415, 3, 0, 130, @WorgenMask, @WorgenMask_2, @Bloodfang, 1, 'Practice Earth Shock',
 'Earth Shock',
 'Speak to Edwin Thornfield and learn Earth Shock. Use Earth Shock on a Bloodfang Worgen.',
 'The wall kept the world out, $N, but it never kept out the earth beneath it. The old ways remember that, even if Gilneas forgot.$B$BListen to the ground and it will lend you its strength. I''ll show you how to strike with it. Then try it on the bloodfang worgen to our west.',
 ''),
(91415, 2, 3, 1, 4714, 0, 2, 83, 100, @WorgenMask, @WorgenMask_2, 0, 0, '', 'Safety in Numbers',
 'Speak to King Genn Greymane in the military district.',
 'I''ve taught you all that is practical for now.$B$BIt is time we joined with the other survivors. The others mentioned that King Greymane and his royal guard are just south of here.$B$BThe earth holds us all up, $N. So should we hold each other.',
 '');

DELETE FROM `quest_template_addon` WHERE `ID` BETWEEN 91410 AND 91415;
INSERT INTO `quest_template_addon` (`ID`, `AllowableClasses`, `PrevQuestID`, `NextQuestID`, `ExclusiveGroup`) VALUES
(91410, 2, 14099, 91411, 0), (91411, 2, 91410, 91412, 0), (91412, 2, 91411, 0, 14286),
(91413, 64, 14099, 91414, 0), (91414, 64, 91413, 91415, 0), (91415, 64, 91414, 0, 14286);

DELETE FROM `quest_request_items` WHERE `ID` BETWEEN 91410 AND 91415;
INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`) VALUES
(91411, 5, 6, 'Has the Light answered you yet?'), (91414, 5, 6, 'Did the ground speak to you?');
DELETE FROM `quest_offer_reward` WHERE `ID` BETWEEN 91410 AND 91415;
INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `RewardText`) VALUES
(91410, 4, '$N! The Light be praised, you''re alive.$B$BCome, there''s no time to waste.'),
(91411, 4, 'Well struck. The Light is with you, $N, even now.'),
(91412, 4, 'You''ve done well in coming here.  If we Gilneans stick together we might yet defeat this terrible enemy.'),
(91413, 4, 'So you''re the one. The earth was right about you.$B$BSit a moment. We''ll begin.'),
(91414, 4, 'You felt it, didn''t you? The ground answered. Good.'),
(91415, 4, 'You''ve done well in coming here.  If we Gilneans stick together we might yet defeat this terrible enemy.');

DELETE FROM `creature_queststarter` WHERE `quest` BETWEEN 91410 AND 91415;
INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
(@Gwen, 91410), (@GilneasPaladinTrainerCreatureID, 91411), (@GilneasPaladinTrainerCreatureID, 91412),
(@Gwen, 91413), (@GilneasShamanTrainerCreatureID, 91414), (@GilneasShamanTrainerCreatureID, 91415);
-- without F-029 there is no trainer to send them to
DELETE FROM `creature_queststarter` WHERE `quest` IN (91410, 91413) AND NOT @GilneasAracTrainers;
DELETE FROM `creature_questender` WHERE `quest` BETWEEN 91410 AND 91415;
INSERT INTO `creature_questender` (`id`, `quest`) VALUES
(@GilneasPaladinTrainerCreatureID, 91410), (@GilneasPaladinTrainerCreatureID, 91411), (@Greymane, 91412),
(@GilneasShamanTrainerCreatureID, 91413), (@GilneasShamanTrainerCreatureID, 91414), (@Greymane, 91415);

-- Old Divisions and While You're At It: these Safety in Numbers count like the natives' ones
DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` = 19 AND `SourceGroup` = 0 AND `SourceEntry` IN (14157, 24930)
  AND `SourceId` = 0 AND `ElseGroup` IN (8, 9);
INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`,
  `ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`,
  `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES
  (19, 0, 14157, 0, 8, 8, 0, 91412, 0, 0, 0, 0, 0, '', 'Old Divisions: paladin Safety in Numbers (I-382)'),
  (19, 0, 14157, 0, 9, 8, 0, 91415, 0, 0, 0, 0, 0, '', 'Old Divisions: shaman Safety in Numbers (I-382)'),
  (19, 0, 24930, 0, 8, 8, 0, 91412, 0, 0, 0, 0, 0, '', 'While You''re At It: paladin Safety in Numbers (I-382)'),
  (19, 0, 24930, 0, 9, 8, 0, 91415, 0, 0, 0, 0, 0, '', 'While You''re At It: shaman Safety in Numbers (I-382)');

-- Credit on the Bloodfang Worgen: any Judgement, any Earth Shock rank
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = @Bloodfang AND `id` BETWEEN 3000 AND 3099;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`,
  `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`,
  `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`,
  `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`)
SELECT @Bloodfang, 0, 3000 + s.n, 0, 8, 0, 100, 0, s.spell, 0, 0, 0, 0, 0, 33, @Bloodfang, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0,
  CONCAT('quest ', s.quest, ': credit when hit by ', s.spell, ' (I-382)')
FROM (SELECT 0 n, 20271 spell, 91411 quest UNION ALL SELECT 1, 53407, 91411 UNION ALL SELECT 2, 53408, 91411
      UNION ALL SELECT 3, 8042, 91414 UNION ALL SELECT 4, 8044, 91414 UNION ALL SELECT 5, 8045, 91414
      UNION ALL SELECT 6, 8046, 91414 UNION ALL SELECT 7, 10412, 91414 UNION ALL SELECT 8, 10413, 91414
      UNION ALL SELECT 9, 10414, 91414 UNION ALL SELECT 10, 25454, 91414 UNION ALL SELECT 11, 49230, 91414
      UNION ALL SELECT 12, 49231, 91414) s;

-- F-002's Call of Earth (Alliance, 92801) from the Gilneas shaman trainer, when both modpaks are in the manifest
DELETE FROM `creature_queststarter` WHERE `id` = @GilneasShamanTrainerCreatureID AND `quest` = 92801;
DELETE FROM `creature_questender` WHERE `id` = @GilneasShamanTrainerCreatureID AND `quest` = 92801;
INSERT INTO `creature_queststarter` (`id`, `quest`)
  SELECT @GilneasShamanTrainerCreatureID, `ID` FROM `quest_template` WHERE `ID` = 92801 AND @GilneasAracTrainers;
INSERT INTO `creature_questender` (`id`, `quest`)
  SELECT @GilneasShamanTrainerCreatureID, `ID` FROM `quest_template` WHERE `ID` = 92801 AND @GilneasAracTrainers;
