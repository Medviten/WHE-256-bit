-- ============================================================================
-- I-386 Lost Isles druid class quests - Bear Form
-- ============================================================================
-- 3.3.5a teaches Bear Form only through the level-10 Moonglade chain (Heeding
-- the Call -> Great Bear Spirit -> Body and Heart), which goblins can't reach
-- from the Lost Isles. With F-029, whose druid trainer Fernie Mossgrubber
-- stands beside Sister Goldskimmer ([I-380]), ARAC's goblin druids get a local
-- version, as [I-375]-[I-377] do for the native classes:
--   91428 Heeding the Call   Fernie -> the Great Bear Spirit on the Lumber Yard shelf
--   91429 Body and Heart     defeat an Echo of Lunaclaw, return to Fernie
--                            -> Bear Form, Growl, Maul (19179, as stock 6001)
-- Spawns (phase 50176, the level-10 stages) beside [I-376]'s shelf beasts,
-- whose spots were checked in game; these aren't yet.
-- ============================================================================
SET @KezanAracTrainers = COALESCE(@AllTrainersEnabled, 0) <> 0;

DELETE FROM `creature_template` WHERE entry IN (901026, 901027);
INSERT INTO `creature_template` SET
  entry = 901026, name = 'Great Bear Spirit', minlevel = 60, maxlevel = 60, faction = 35, npcflag = 2, speed_walk = 1,
  speed_run = 1.14286, speed_swim = 1, speed_flight = 1, detection_range = 18, DamageModifier = 1, BaseAttackTime = 2000,
  RangeAttackTime = 2000, BaseVariance = 1, RangeVariance = 1, unit_class = 1, unit_flags = 768, unit_flags2 = 2048, type = 1,
  HoverHeight = 1, HealthModifier = 1, ManaModifier = 1, ArmorModifier = 1, ExperienceModifier = 1, RegenHealth = 1, flags_extra = 2;
INSERT INTO `creature_template` SET
  entry = 901027, name = 'Echo of Lunaclaw', minlevel = 10, maxlevel = 10, faction = 14, speed_walk = 1, speed_run = 1.14286,
  speed_swim = 1, speed_flight = 1, detection_range = 18, DamageModifier = 1, BaseAttackTime = 2000, RangeAttackTime = 2000,
  BaseVariance = 1, RangeVariance = 1, unit_class = 1, unit_flags2 = 2048, family = 4, type = 1, HoverHeight = 1,
  HealthModifier = 1.5, ManaModifier = 1, ArmorModifier = 1, ExperienceModifier = 1, RegenHealth = 1, MovementType = 1;
DELETE FROM `creature_template_model` WHERE CreatureID IN (901026, 901027);
INSERT INTO `creature_template_model` (CreatureID, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild) VALUES
  (901026, 0, 11909, 1, 1, 0),  -- stock 11956 Great Bear Spirit's look
  (901027, 0, 9389, 1, 1, 0);     -- stock 12138 Lunaclaw's look
DELETE FROM `creature` WHERE guid BETWEEN 3111010 AND 3111013;
INSERT INTO `creature` (guid, id, map, spawnMask, phaseMask, position_x, position_y, position_z, orientation, spawntimesecs, wander_distance, MovementType, Comment) VALUES
  (3111010, 901026, 1, 1, 50176, 1803.20, -10983.08, 51.70, 2.304, 60, 0, 0, '[I-386] Great Bear Spirit - Lumber Yard shelf'),
  (3111011, 901027, 1, 1, 50176, 1749.12, -10965.41, 63.08, 4.471, 60, 3, 1, '[I-386] Echo of Lunaclaw - Lumber Yard shelf'),
  (3111012, 901027, 1, 1, 50176, 1795.32, -11055.05, 67.48, 0.660, 60, 3, 1, '[I-386] Echo of Lunaclaw - Lumber Yard shelf'),
  (3111013, 901027, 1, 1, 50176, 1780.72, -11033.24, 69.96, 5.818, 60, 3, 1, '[I-386] Echo of Lunaclaw - Lumber Yard shelf');
DELETE FROM `creature` WHERE guid BETWEEN 3111010 AND 3111013 AND NOT @KezanAracTrainers;

DELETE FROM `quest_template` WHERE ID IN (91428, 91429);
INSERT INTO `quest_template` SET
  ID = 91428, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -263, RewardXPDifficulty = 2,
  AllowableRaces = @GoblinMask, `AllowableRaces_2` = @GoblinMask_2, LogTitle = 'Heeding the Call',
  LogDescription = 'Speak with the Great Bear Spirit on the high ground east of the Bilgewater Lumber Yard.',
  QuestDescription = 'You''ve come a long way for someone who started out watering potted ferns, $N. Time for the next step.$B$BThere''s something up on the high ground past the lumber yard. The animals give it a wide berth and the loggers won''t go near it. I think it''s a spirit, an old one, the kind that teaches druids to take the shape of the bear.$B$BGo and listen to it. Try not to sell it anything.',
  QuestCompletionLog = 'Speak with the Great Bear Spirit.';
INSERT INTO `quest_template` SET
  ID = 91429, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -263, RewardXPDifficulty = 5,
  RewardSpell = 19179, RewardDisplaySpell = 19179, AllowableRaces = @GoblinMask, `AllowableRaces_2` = @GoblinMask_2,
  RequiredNpcOrGo1 = 901027, RequiredNpcOrGoCount1 = 1, ObjectiveText1 = 'Echo of Lunaclaw defeated',
  LogTitle = 'Body and Heart',
  LogDescription = 'Defeat an Echo of Lunaclaw on the high ground east of the Bilgewater Lumber Yard, then return to Fernie Mossgrubber.',
  QuestDescription = 'The bear is strength, young druid, but strength without heart is only weight. Your people have plenty of weight.$B$BAn echo of Lunaclaw walks this hill, a memory of one who once tested all who came to me. Face it. Show me your body can endure and your heart will not break, and the shape of the bear is yours.$B$BThen return to the one who sent you.',
  QuestCompletionLog = 'Return to Fernie Mossgrubber.';
DELETE FROM `quest_template_addon` WHERE ID IN (91428, 91429);
INSERT INTO `quest_template_addon` (ID, AllowableClasses, PrevQuestID) VALUES (91428, 1024, 0), (91429, 1024, 91428);
DELETE FROM `quest_request_items` WHERE ID IN (91428, 91429);
INSERT INTO `quest_request_items` (ID, EmoteOnComplete, EmoteOnIncomplete, CompletionText) VALUES
  (91429, 1, 1, 'Back already? Did the big spirit like you?');
DELETE FROM `quest_offer_reward` WHERE ID IN (91428, 91429);
INSERT INTO `quest_offer_reward` (ID, Emote1, RewardText) VALUES
  (91428, 1, 'A child of the island, smelling of oil and coin. ... And yet the wild answered when you called. Listen, then.'),
  (91429, 4, 'Look at you! Claws, fur, the whole package. That''s the bear, $N, and it''s yours now. Use it when the island gets rough, which is always.');
DELETE FROM `creature_queststarter` WHERE quest IN (91428, 91429);
INSERT INTO `creature_queststarter` (id, quest) VALUES (@KezanDruidTrainerCreatureID, 91428), (901026, 91429);
DELETE FROM `creature_questender` WHERE quest IN (91428, 91429);
INSERT INTO `creature_questender` (id, quest) VALUES (901026, 91428), (@KezanDruidTrainerCreatureID, 91429);

-- Quest POIs (Lost Isles WorldMapArea 544)
DELETE FROM `quest_poi` WHERE QuestID IN (91428, 91429);
INSERT INTO `quest_poi` (QuestID, id, ObjectiveIndex, MapID, WorldMapAreaId, Floor, Priority, Flags, VerifiedBuild) VALUES
  (91428, 0, -1, 1, 544, 0, 0, 1, 0), (91429, 0, -1, 1, 544, 0, 0, 1, 0), (91429, 1, 0, 1, 544, 0, 0, 1, 0);
DELETE FROM `quest_poi_points` WHERE QuestID IN (91428, 91429);
INSERT INTO `quest_poi_points` (QuestID, Idx1, Idx2, X, Y, VerifiedBuild) VALUES
  (91428, 0, 0, 1803, -10983, 0), (91429, 0, 0, 1830, -10871, 0),
  (91429, 1, 0, 1828, -10950, 0), (91429, 1, 1, 1828, -11075, 0), (91429, 1, 2, 1740, -11075, 0), (91429, 1, 3, 1740, -10950, 0);
