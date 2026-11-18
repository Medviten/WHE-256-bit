-- ============================================================================
-- I-381 Taming the Beast in Goldshire and Brill (F-029)
-- ============================================================================
-- 3.3.5a grants Tame Beast / Beast Training only through the stock Taming the
-- Beast chains (Kharanos, Dolanaar, Razor Hill, Bloodhoof Village, Azure Watch,
-- Falconwing Square). The second-town hunter trainers F-029 adds in Goldshire
-- (Benjamin Foxworthy) and Brill (Dedlow Wormwood) now have their own, built
-- like F-013's Kezan chain ([I-376]) on the zones' stock beasts:
--   Goldshire 91400-91403: Stonetusk Boar, Forest Spider, Young Forest Bear, Training the Beast
--   Brill     91404-91407: Greater Duskbat, Vicious Night Web Spider, Worg, Training the Beast
-- The third tame rewards Tame Beast (1579 -> 1515), the last quest Beast Training (5300).
-- Rods 84600-84605 (spells 901000-901005, dbc/[I-381]_*), final tame spells 901006-901011,
-- credit creatures 901000-901005 (never spawned: killing a beast never counts).
-- Needs F-013's core patch (the I-376 rod fallback, ungated since I-381). Worgs are level 10-11:
-- the rod refuses one above the hunter's level.
-- ============================================================================

DELETE FROM `creature_template` WHERE entry BETWEEN 901000 AND 901005;
INSERT INTO `creature_template` (entry, name, subname, minlevel, maxlevel, faction, unit_flags, flags_extra, RegenHealth) VALUES
  (901000, 'Stonetusk Boar tamed', 'I-381 credit', 1, 1, 35, 33554432, 130, 1),
  (901001, 'Forest Spider tamed', 'I-381 credit', 1, 1, 35, 33554432, 130, 1),
  (901002, 'Young Forest Bear tamed', 'I-381 credit', 1, 1, 35, 33554432, 130, 1),
  (901003, 'Greater Duskbat tamed', 'I-381 credit', 1, 1, 35, 33554432, 130, 1),
  (901004, 'Vicious Night Web Spider tamed', 'I-381 credit', 1, 1, 35, 33554432, 130, 1),
  (901005, 'Worg tamed', 'I-381 credit', 1, 1, 35, 33554432, 130, 1);
DELETE FROM `creature_template_model` WHERE CreatureID BETWEEN 901000 AND 901005;
INSERT INTO `creature_template_model` (CreatureID, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild) VALUES
  (901000, 0, 11686, 1, 1, 0),
  (901001, 0, 11686, 1, 1, 0),
  (901002, 0, 11686, 1, 1, 0),
  (901003, 0, 11686, 1, 1, 0),
  (901004, 0, 11686, 1, 1, 0),
  (901005, 0, 11686, 1, 1, 0);

-- Taming Rods
DELETE FROM `item_template` WHERE entry = 84600;
INSERT INTO `item_template` SET
  entry = 84600, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901000, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Stonetusk Boar.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84601;
INSERT INTO `item_template` SET
  entry = 84601, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901001, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Forest Spider.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84602;
INSERT INTO `item_template` SET
  entry = 84602, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901002, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Young Forest Bear.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84603;
INSERT INTO `item_template` SET
  entry = 84603, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901003, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Greater Duskbat.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84604;
INSERT INTO `item_template` SET
  entry = 84604, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901004, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Vicious Night Web Spider.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84605;
INSERT INTO `item_template` SET
  entry = 84605, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901005, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Worg.', Material = -1;

-- Quests (fields follow stock 6062/6083/6082/6081 and [I-376])
DELETE FROM `quest_template` WHERE ID BETWEEN 91400 AND 91407;
INSERT INTO `quest_template` SET
  ID = 91400,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardNextQuest = 91401,
  RewardXPDifficulty = 5,
  StartItem = 84600,
  Flags = 2,
  AllowableRaces = @AllianceMask,
  `AllowableRaces_2` = @AllianceMask_2,
  RequiredItemId1 = 84600,
  RequiredItemCount1 = 1,
  RequiredNpcOrGo1 = 901000,
  RequiredNpcOrGoCount1 = 1,
  ObjectiveText1 = 'Stonetusk Boar tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Stonetusk Boar in the fields south-west of Goldshire, then return the rod to Benjamin Foxworthy.',
  QuestDescription = 'So you''re the new $c everyone''s talking about? Good. A hunter without a companion is just someone with a bow and a bad attitude.$B$BWe''ll start you off easy. The Stonetusk Boars in the fields south-west of town are stubborn, but they''re no match for a bit of patience. Take this Taming Rod, use it on a boar and keep its attention until it''s yours.$B$BThen bring the rod back. I only have the one.',
  QuestCompletionLog = 'Return the Taming Rod to Benjamin Foxworthy.';
INSERT INTO `quest_template` SET
  ID = 91401,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardNextQuest = 91402,
  RewardXPDifficulty = 5,
  StartItem = 84601,
  Flags = 2,
  AllowableRaces = @AllianceMask,
  `AllowableRaces_2` = @AllianceMask_2,
  RequiredItemId1 = 84601,
  RequiredItemCount1 = 1,
  RequiredNpcOrGo1 = 901001,
  RequiredNpcOrGoCount1 = 1,
  ObjectiveText1 = 'Forest Spider tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Forest Spider in the woods south-west of Goldshire, then return the rod to Benjamin Foxworthy.',
  QuestDescription = 'Boars are one thing. Spiders are another. Most folk run from them; a hunter learns what makes them tick.$B$BThe Forest Spiders in the woods south-west of town are skittish and quick. Use the rod on one, hold its attention, and don''t flinch.',
  QuestCompletionLog = 'Return the Taming Rod to Benjamin Foxworthy.';
INSERT INTO `quest_template` SET
  ID = 91402,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardNextQuest = 91403,
  RewardXPDifficulty = 5,
  RewardDisplaySpell = 23356,
  RewardSpell = 1579,
  StartItem = 84602,
  Flags = 2,
  AllowableRaces = @AllianceMask,
  `AllowableRaces_2` = @AllianceMask_2,
  RequiredItemId1 = 84602,
  RequiredItemCount1 = 1,
  RequiredNpcOrGo1 = 901002,
  RequiredNpcOrGoCount1 = 1,
  ObjectiveText1 = 'Young Forest Bear tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Young Forest Bear in the forest south of Goldshire, then return the rod to Benjamin Foxworthy.',
  QuestDescription = 'Last one, and the toughest. The Young Forest Bears deeper in the forest south of Goldshire are strong and short-tempered, even the cubs.$B$BTame one of those and you can tame anything in Elwynn. Here''s your last rod.',
  QuestCompletionLog = 'Return the Taming Rod to Benjamin Foxworthy.';
INSERT INTO `quest_template` SET
  ID = 91403,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardXPDifficulty = 3,
  RewardDisplaySpell = 23357,
  RewardSpell = 5300,
  Flags = 8,
  AllowableRaces = @AllianceMask,
  `AllowableRaces_2` = @AllianceMask_2,
  LogTitle = 'Training the Beast',
  LogDescription = 'Speak to Benjamin Foxworthy.',
  QuestDescription = 'Taming a companion is the easy part. Keeping it fed, loyal and fighting at your side takes training.$B$BLet me show you how to teach your pet and see to its needs. Then go and find one worth keeping.';
INSERT INTO `quest_template` SET
  ID = 91404,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardNextQuest = 91405,
  RewardXPDifficulty = 5,
  StartItem = 84603,
  Flags = 2,
  AllowableRaces = @HordeMask,
  `AllowableRaces_2` = @HordeMask_2,
  RequiredItemId1 = 84603,
  RequiredItemCount1 = 1,
  RequiredNpcOrGo1 = 901003,
  RequiredNpcOrGoCount1 = 1,
  ObjectiveText1 = 'Greater Duskbat tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Greater Duskbat around Brill, then return the rod to Dedlow Wormwood.',
  QuestDescription = 'You want a companion, $N? The living keep dogs. We keep whatever survives.$B$BThe Greater Duskbats around Brill feed on whatever wanders out after dark. Take this Taming Rod, use it on one and hold its attention until it answers to you.$B$BThen bring the rod back. The Apothecaries count them.',
  QuestCompletionLog = 'Return the Taming Rod to Dedlow Wormwood.';
INSERT INTO `quest_template` SET
  ID = 91405,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardNextQuest = 91406,
  RewardXPDifficulty = 5,
  StartItem = 84604,
  Flags = 2,
  AllowableRaces = @HordeMask,
  `AllowableRaces_2` = @HordeMask_2,
  RequiredItemId1 = 84604,
  RequiredItemCount1 = 1,
  RequiredNpcOrGo1 = 901004,
  RequiredNpcOrGoCount1 = 1,
  ObjectiveText1 = 'Vicious Night Web Spider tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Vicious Night Web Spider in the woods east of Brill, then return the rod to Dedlow Wormwood.',
  QuestDescription = 'The Vicious Night Web Spiders in the woods east of Brill are anything but friendly. They bite, they poison, and they don''t care whether you''re breathing.$B$BUse the rod on one and keep it busy until it''s yours. Try not to get wrapped up.',
  QuestCompletionLog = 'Return the Taming Rod to Dedlow Wormwood.';
INSERT INTO `quest_template` SET
  ID = 91406,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardNextQuest = 91407,
  RewardXPDifficulty = 5,
  RewardDisplaySpell = 23356,
  RewardSpell = 1579,
  StartItem = 84605,
  Flags = 2,
  AllowableRaces = @HordeMask,
  `AllowableRaces_2` = @HordeMask_2,
  RequiredItemId1 = 84605,
  RequiredItemCount1 = 1,
  RequiredNpcOrGo1 = 901005,
  RequiredNpcOrGoCount1 = 1,
  ObjectiveText1 = 'Worg tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Worg in the hills south-west of Brill, then return the rod to Dedlow Wormwood.',
  QuestDescription = 'The last test. The Worgs in the hills south-west of Brill hunt in packs and answer to no one. Bend one of them to your will and you can bend anything.$B$BHere is your last rod. Some of them are bigger than you; pick one you can handle.',
  QuestCompletionLog = 'Return the Taming Rod to Dedlow Wormwood.';
INSERT INTO `quest_template` SET
  ID = 91407,
  QuestType = 2,
  QuestLevel = 10,
  MinLevel = 10,
  QuestSortID = -261,
  RewardXPDifficulty = 3,
  RewardDisplaySpell = 23357,
  RewardSpell = 5300,
  Flags = 8,
  AllowableRaces = @HordeMask,
  `AllowableRaces_2` = @HordeMask_2,
  LogTitle = 'Training the Beast',
  LogDescription = 'Speak to Dedlow Wormwood.',
  QuestDescription = 'Taming is only the start. A companion has to be fed, trained and kept in line, or it will turn on you.$B$BLet me show you how to teach your pet. Then go find one worth the trouble.';
DELETE FROM `quest_template_addon` WHERE ID BETWEEN 91400 AND 91407;
INSERT INTO `quest_template_addon` (ID, AllowableClasses, PrevQuestID, ProvidedItemCount, SpecialFlags) VALUES
  (91400, 4, 0, 1, 0),
  (91401, 4, 91400, 1, 0),
  (91402, 4, 91401, 1, 0),
  (91403, 4, 91402, 0, 0),
  (91404, 4, 0, 1, 0),
  (91405, 4, 91404, 1, 0),
  (91406, 4, 91405, 1, 0),
  (91407, 4, 91406, 0, 0);
DELETE FROM `quest_request_items` WHERE ID BETWEEN 91400 AND 91407;
INSERT INTO `quest_request_items` (ID, EmoteOnComplete, EmoteOnIncomplete, CompletionText) VALUES
  (91400, 1, 1, 'Did the boar take to you, or did you take to the boar?'),
  (91401, 1, 1, 'Still in one piece? No bites?'),
  (91402, 1, 1, 'Did the bear let you get close?'),
  (91404, 1, 1, 'Has the bat accepted you yet?'),
  (91405, 1, 1, 'Still free of webs?'),
  (91406, 1, 1, 'Did the worg submit?');
DELETE FROM `quest_offer_reward` WHERE ID BETWEEN 91400 AND 91407;
INSERT INTO `quest_offer_reward` (ID, Emote1, RewardText) VALUES
  (91400, 273, 'Look at that, it followed you halfway back! You''ve a knack for this, $N. Let''s try something with more legs.'),
  (91401, 273, 'Not a single bite. Well done, $N. One more lesson and you''ll be taming beasts without my rods.'),
  (91402, 273, 'A bear, $N! From now on you can tame any beast you like, no rod required. Come back when you''re ready to learn how to look after it.'),
  (91403, 1, 'There. Your pet can learn new tricks now, and you know how to feed it. Look after it, $N, and it will look after you.'),
  (91404, 273, 'It came when you called. Good. Bats are easy, $N; the next one has eight legs.'),
  (91405, 273, 'Not even a strand on you. One more, $N, and you won''t need my rods at all.'),
  (91406, 273, 'A worg at your heel. From now on you can tame any beast you like, no rod required. Come back and I''ll show you how to keep it.'),
  (91407, 1, 'It will learn new tricks now, and you know how to feed it. Keep it close, $N. In the Undercity, loyalty is rare.');
DELETE FROM `creature_queststarter` WHERE quest BETWEEN 91400 AND 91407;
INSERT INTO `creature_queststarter` (id, quest) VALUES (46983, 91400), (46983, 91401), (46983, 91402), (46983, 91403), (39100, 91404), (39100, 91405), (39100, 91406), (39100, 91407);
DELETE FROM `creature_questender` WHERE quest BETWEEN 91400 AND 91407;
INSERT INTO `creature_questender` (id, quest) VALUES (46983, 91400), (46983, 91401), (46983, 91402), (46983, 91403), (39100, 91404), (39100, 91405), (39100, 91406), (39100, 91407);

-- Each rod only works on its own beast (source type 17 = spell, target 1 = explicit target, type 31 = object entry)
DELETE FROM `conditions` WHERE SourceTypeOrReferenceId = 17 AND SourceEntry BETWEEN 901000 AND 901005;
INSERT INTO `conditions` (SourceTypeOrReferenceId, SourceGroup, SourceEntry, SourceId, ElseGroup, ConditionTypeOrReference, ConditionTarget, ConditionValue1, ConditionValue2, ConditionValue3, NegativeCondition, ErrorType, ErrorTextId, ScriptName, Comment) VALUES
  (17, 0, 901000, 0, 0, 31, 1, 3, 113, 0, 0, 0, 0, '', 'I-381 Tame Stonetusk Boar - only on a Stonetusk Boar'),
  (17, 0, 901001, 0, 0, 31, 1, 3, 30, 0, 0, 0, 0, '', 'I-381 Tame Forest Spider - only on a Forest Spider'),
  (17, 0, 901002, 0, 0, 31, 1, 3, 822, 0, 0, 0, 0, '', 'I-381 Tame Young Forest Bear - only on a Young Forest Bear'),
  (17, 0, 901003, 0, 0, 31, 1, 3, 1553, 0, 0, 0, 0, '', 'I-381 Tame Greater Duskbat - only on a Greater Duskbat'),
  (17, 0, 901004, 0, 0, 31, 1, 3, 1555, 0, 0, 0, 0, '', 'I-381 Tame Vicious Night Web Spider - only on a Vicious Night Web Spider'),
  (17, 0, 901005, 0, 0, 31, 1, 3, 1765, 0, 0, 0, 0, '', 'I-381 Tame Worg - only on a Worg');
-- Same scripts as the stock rods and final tames: tame checks on the rod, despawn-on-dismiss on the temporary pet
DELETE FROM `spell_script_names` WHERE spell_id BETWEEN 901000 AND 901011;
INSERT INTO `spell_script_names` (spell_id, ScriptName) VALUES
  (901000, 'spell_hun_tame_beast'),
  (901006, 'spell_hun_taming_the_beast'),
  (901001, 'spell_hun_tame_beast'),
  (901007, 'spell_hun_taming_the_beast'),
  (901002, 'spell_hun_tame_beast'),
  (901008, 'spell_hun_taming_the_beast'),
  (901003, 'spell_hun_tame_beast'),
  (901009, 'spell_hun_taming_the_beast'),
  (901004, 'spell_hun_tame_beast'),
  (901010, 'spell_hun_taming_the_beast'),
  (901005, 'spell_hun_tame_beast'),
  (901011, 'spell_hun_taming_the_beast');

-- Quest POIs: the turn-in (-1) and the beast's ground (objective 0) on Elwynn (30) / Tirisfal (20)
DELETE FROM `quest_poi` WHERE QuestID BETWEEN 91400 AND 91407;
INSERT INTO `quest_poi` (QuestID, id, ObjectiveIndex, MapID, WorldMapAreaId, Floor, Priority, Flags, VerifiedBuild) VALUES
  (91400, 0, -1, 0, 30, 0, 0, 1, 0),
  (91400, 1, 0, 0, 30, 0, 0, 1, 0),
  (91401, 0, -1, 0, 30, 0, 0, 1, 0),
  (91401, 1, 0, 0, 30, 0, 0, 1, 0),
  (91402, 0, -1, 0, 30, 0, 0, 1, 0),
  (91402, 1, 0, 0, 30, 0, 0, 1, 0),
  (91403, 0, -1, 0, 30, 0, 0, 1, 0),
  (91404, 0, -1, 0, 20, 0, 0, 1, 0),
  (91404, 1, 0, 0, 20, 0, 0, 1, 0),
  (91405, 0, -1, 0, 20, 0, 0, 1, 0),
  (91405, 1, 0, 0, 20, 0, 0, 1, 0),
  (91406, 0, -1, 0, 20, 0, 0, 1, 0),
  (91406, 1, 0, 0, 20, 0, 0, 1, 0),
  (91407, 0, -1, 0, 20, 0, 0, 1, 0);
DELETE FROM `quest_poi_points` WHERE QuestID BETWEEN 91400 AND 91407;
INSERT INTO `quest_poi_points` (QuestID, Idx1, Idx2, X, Y, VerifiedBuild) VALUES
  (91400, 0, 0, -9465, 117, 0),
  (91400, 1, 0, -9530, 4, 0), (91400, 1, 1, -9530, 187, 0), (91400, 1, 2, -9738, 187, 0), (91400, 1, 3, -9738, 4, 0),
  (91401, 0, 0, -9465, 117, 0),
  (91401, 1, 0, -9559, -12, 0), (91401, 1, 1, -9559, 218, 0), (91401, 1, 2, -9760, 218, 0), (91401, 1, 3, -9760, -12, 0),
  (91402, 0, 0, -9465, 117, 0),
  (91402, 1, 0, -9695, -173, 0), (91402, 1, 1, -9695, 29, 0), (91402, 1, 2, -9908, 29, 0), (91402, 1, 3, -9908, -173, 0),
  (91403, 0, 0, -9465, 117, 0),
  (91404, 0, 0, 2231, 241, 0),
  (91404, 1, 0, 2355, 38, 0), (91404, 1, 1, 2355, 488, 0), (91404, 1, 2, 1982, 488, 0), (91404, 1, 3, 1982, 38, 0),
  (91405, 0, 0, 2231, 241, 0),
  (91405, 1, 0, 2417, -921, 0), (91405, 1, 1, 2417, -691, 0), (91405, 1, 2, 2112, -691, 0), (91405, 1, 3, 2112, -921, 0),
  (91406, 0, 0, 2231, 241, 0),
  (91406, 1, 0, 1586, 502, 0), (91406, 1, 1, 1586, 729, 0), (91406, 1, 2, 1376, 729, 0), (91406, 1, 3, 1376, 502, 0),
  (91407, 0, 0, 2231, 241, 0);
