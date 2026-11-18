-- ============================================================================
-- I-384 Gilneas level-10 class quests
-- ============================================================================
-- 3.3.5a teaches Tame Beast, Summon Voidwalker and Searing Totem only through
-- level-10 quests far from Gilneas, which Worgen don't leave until 12. As F-013
-- does on the Lost Isles ([I-375], [I-376], [I-377]), Stormglen's trainers have
-- their own versions:
--   91420-91423 Huntsman Blake: Taming the Beast (Vilebrood Skitterer, Swamp
--               Crocolisk, Blackwald Fox) -> Tame Beast, Training the Beast
--   91424       Vitus Darkwalker: Creature of the Void - use the Attuned Orb of
--               Dominion at the summoning circle beside him, subjugate the
--               voidwalker -> Summon Voidwalker
--   91425-91427 the Gilneas shaman trainer (F-029, [I-379]) for ARAC's Worgen
--               shamans: Call of Fire - the Spirit of Fire in the burning woods
--               south of Stormglen, 6 Raging Embers, the torch back -> Searing
--               Totem + Fire Totem
-- Spawns are in phase 8 + 1024 + 2048 (Stormglen and the later phases). Places
-- are taken from existing spawns (ground): the circle on a Duskhaven Survivor's
-- spot by Vitus, the embers 4 yd from Vilebrood Skitterers. Not yet checked in
-- game. Spells, rods, orb and spell focus are dbc/[I-384]_*. The rods need F-013's
-- core patch (the I-376 rod fallback).
-- ============================================================================
SET @GilneasAracTrainers = COALESCE(@AllTrainersEnabled, 0) <> 0;

-- ---------------------------------------------------------------------------
-- Taming the Beast (Huntsman Blake)
-- ---------------------------------------------------------------------------
DELETE FROM `creature_template` WHERE entry BETWEEN 901020 AND 901022;
INSERT INTO `creature_template` (entry, name, subname, minlevel, maxlevel, faction, unit_flags, flags_extra, RegenHealth) VALUES
  (901020, 'Vilebrood Skitterer tamed', 'I-384 credit', 1, 1, 35, 33554432, 130, 1),
  (901021, 'Swamp Crocolisk tamed', 'I-384 credit', 1, 1, 35, 33554432, 130, 1),
  (901022, 'Blackwald Fox tamed', 'I-384 credit', 1, 1, 35, 33554432, 130, 1);
DELETE FROM `creature_template_model` WHERE CreatureID BETWEEN 901020 AND 901022;
INSERT INTO `creature_template_model` (CreatureID, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild) VALUES
  (901020, 0, 11686, 1, 1, 0),
  (901021, 0, 11686, 1, 1, 0),
  (901022, 0, 11686, 1, 1, 0);
DELETE FROM `item_template` WHERE entry = 84606;
INSERT INTO `item_template` SET
  entry = 84606, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901020, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Vilebrood Skitterer.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84607;
INSERT INTO `item_template` SET
  entry = 84607, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901021, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Swamp Crocolisk.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84608;
INSERT INTO `item_template` SET
  entry = 84608, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901022, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Blackwald Fox.', Material = -1;
DELETE FROM `quest_template` WHERE ID BETWEEN 91420 AND 91423;
INSERT INTO `quest_template` SET
  ID = 91420, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -261, RewardNextQuest = 91421, RewardXPDifficulty = 5,
  StartItem = 84606, Flags = 2, AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2,
  RequiredItemId1 = 84606, RequiredItemCount1 = 1, RequiredNpcOrGo1 = 901020, RequiredNpcOrGoCount1 = 1, ObjectiveText1 = 'Vilebrood Skitterer tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Vilebrood Skitterer in the woods south of Stormglen, then return the rod to Huntsman Blake in Stormglen.',
  QuestDescription = 'So you''ve a mind to keep a companion, $N? Good. Out here a hunter alone is a hunter dead.$B$BWe''ll begin with something that bites. The Vilebrood Skitterers in the woods south of Stormglen are vicious, but they can be taught. Take this Taming Rod, use it on one and keep its attention until it''s yours.$B$BThen bring the rod back. I''ve not got many left.',
  QuestCompletionLog = 'Return the Taming Rod to Huntsman Blake.';
INSERT INTO `quest_template` SET
  ID = 91421, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -261, RewardNextQuest = 91422, RewardXPDifficulty = 5,
  StartItem = 84607, Flags = 2, AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2,
  RequiredItemId1 = 84607, RequiredItemCount1 = 1, RequiredNpcOrGo1 = 901021, RequiredNpcOrGoCount1 = 1, ObjectiveText1 = 'Swamp Crocolisk tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Swamp Crocolisk in the marsh east of Stormglen, then return the rod to Huntsman Blake in Stormglen.',
  QuestDescription = 'Crocolisks, $N. Thick hide, thicker skull, and they don''t let go. The Swamp Crocolisks in the marsh east of Stormglen came up out of the water when the land sank.$B$BTame one with this rod. Mind your boots.',
  QuestCompletionLog = 'Return the Taming Rod to Huntsman Blake.';
INSERT INTO `quest_template` SET
  ID = 91422, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -261, RewardNextQuest = 91423, RewardXPDifficulty = 5,
  RewardDisplaySpell = 23356,
  RewardSpell = 1579,
  StartItem = 84608, Flags = 2, AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2,
  RequiredItemId1 = 84608, RequiredItemCount1 = 1, RequiredNpcOrGo1 = 901022, RequiredNpcOrGoCount1 = 1, ObjectiveText1 = 'Blackwald Fox tamed',
  LogTitle = 'Taming the Beast',
  LogDescription = 'Use the Taming Rod to tame a Blackwald Fox in the Blackwald, then return the rod to Huntsman Blake in Stormglen.',
  QuestDescription = 'Last one. The foxes of the Blackwald are quick and clever, and the worgen haven''t caught a single one. If you can win one of those over, you can win over anything that walks on four legs.$B$BHere''s your last rod.',
  QuestCompletionLog = 'Return the Taming Rod to Huntsman Blake.';
INSERT INTO `quest_template` SET
  ID = 91423, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -261, RewardXPDifficulty = 3,
  RewardDisplaySpell = 23357, RewardSpell = 5300, Flags = 8, AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2,
  LogTitle = 'Training the Beast', LogDescription = 'Speak to Huntsman Blake.',
  QuestDescription = 'Taming is the easy part, $N. A companion has to be fed and trained, or it''ll be no use to you when the worgen come.$B$BLet me show you how to teach your pet. Then go and find one worth keeping.';
DELETE FROM `quest_template_addon` WHERE ID BETWEEN 91420 AND 91423;
INSERT INTO `quest_template_addon` (ID, AllowableClasses, PrevQuestID, ProvidedItemCount) VALUES
  (91420, 4, 0, 1), (91421, 4, 91420, 1), (91422, 4, 91421, 1), (91423, 4, 91422, 0);
DELETE FROM `quest_request_items` WHERE ID BETWEEN 91420 AND 91423;
INSERT INTO `quest_request_items` (ID, EmoteOnComplete, EmoteOnIncomplete, CompletionText) VALUES
  (91420, 1, 1, 'Still have all your fingers?'),
  (91421, 1, 1, 'Did it let you close?'),
  (91422, 1, 1, 'Did the fox come to you?');
DELETE FROM `quest_offer_reward` WHERE ID BETWEEN 91420 AND 91423;
INSERT INTO `quest_offer_reward` (ID, Emote1, RewardText) VALUES
  (91420, 273, 'Look at it, following you like a hound. Next, something with scales.'),
  (91421, 273, 'A crocolisk at your heel. One more lesson and you''ll not need my rods.'),
  (91422, 273, 'Well done, $N. From now on you can tame any beast you like, no rod required. Come back and I''ll show you how to look after it.'),
  (91423, 1, 'There. Your pet will learn new tricks now, and you know how to feed it. Keep it close, $N. Gilneas needs every fang it can get.');
DELETE FROM `creature_queststarter` WHERE quest BETWEEN 91420 AND 91423;
INSERT INTO `creature_queststarter` (id, quest) VALUES (38798, 91420), (38798, 91421), (38798, 91422), (38798, 91423);
DELETE FROM `creature_questender` WHERE quest BETWEEN 91420 AND 91423;
INSERT INTO `creature_questender` (id, quest) VALUES (38798, 91420), (38798, 91421), (38798, 91422), (38798, 91423);
DELETE FROM `conditions` WHERE SourceTypeOrReferenceId = 17 AND SourceEntry BETWEEN 901020 AND 901022;
INSERT INTO `conditions` (SourceTypeOrReferenceId, SourceGroup, SourceEntry, SourceId, ElseGroup, ConditionTypeOrReference, ConditionTarget, ConditionValue1, ConditionValue2, ConditionValue3, NegativeCondition, ErrorType, ErrorTextId, ScriptName, Comment) VALUES
  (17, 0, 901020, 0, 0, 31, 1, 3, 36813, 0, 0, 0, 0, '', 'I-384 Tame Vilebrood Skitterer - only on a Vilebrood Skitterer'),
  (17, 0, 901021, 0, 0, 31, 1, 3, 36882, 0, 0, 0, 0, '', 'I-384 Tame Swamp Crocolisk - only on a Swamp Crocolisk'),
  (17, 0, 901022, 0, 0, 31, 1, 3, 37492, 0, 0, 0, 0, '', 'I-384 Tame Blackwald Fox - only on a Blackwald Fox');
DELETE FROM `spell_script_names` WHERE spell_id BETWEEN 901020 AND 901025;
INSERT INTO `spell_script_names` (spell_id, ScriptName) VALUES
  (901020, 'spell_hun_tame_beast'), (901023, 'spell_hun_taming_the_beast'),
  (901021, 'spell_hun_tame_beast'), (901024, 'spell_hun_taming_the_beast'),
  (901022, 'spell_hun_tame_beast'), (901025, 'spell_hun_taming_the_beast');

-- ---------------------------------------------------------------------------
-- Creature of the Void (Vitus Darkwalker), as [I-375]'s Hostile Takeover
-- ---------------------------------------------------------------------------
DELETE FROM `item_template` WHERE entry = 84609;
INSERT INTO `item_template` SET
  entry = 84609, class = 12, subclass = 0, name = 'Attuned Orb of Dominion', displayid = 39424, Quality = 1, Flags = 64,
  BuyCount = 1, ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901026, spelltrigger_1 = 0, spellcooldown_1 = -1,
  spellcategorycooldown_1 = -1, bonding = 4,
  description = 'Use at the summoning circle beside Vitus Darkwalker to call and subjugate a voidwalker.', Material = 3;
DELETE FROM `quest_template` WHERE ID = 91424;
INSERT INTO `quest_template` SET
  ID = 91424, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -61, RewardXPDifficulty = 4,
  RewardDisplaySpell = 697, RewardSpell = 11520, StartItem = 84609, AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2,
  RequiredNpcOrGo1 = 901023, RequiredNpcOrGoCount1 = 1, RequiredItemId1 = 84609, RequiredItemCount1 = 1,
  ObjectiveText1 = 'Voidwalker subjugated',
  LogTitle = 'Creature of the Void',
  LogDescription = 'Use the Attuned Orb of Dominion at the summoning circle beside Vitus Darkwalker in Stormglen, subjugate the voidwalker that answers, then return the orb to Vitus.',
  QuestDescription = 'An imp is a pet, $N. A voidwalker is a shield, and in these woods you will want one between you and whatever comes out of the dark.$B$BThis orb holds the binding. Use it at the circle I have drawn beside me, and something from the Void will answer. It will not come willingly. Beat it down until it remembers who called it, and it will serve you.$B$BThen bring the orb back. I may yet need it again.',
  QuestCompletionLog = 'Return the Orb of Dominion to Vitus Darkwalker.';
DELETE FROM `quest_template_addon` WHERE ID = 91424;
INSERT INTO `quest_template_addon` (ID, AllowableClasses, ProvidedItemCount) VALUES (91424, 256, 1);
DELETE FROM `quest_request_items` WHERE ID = 91424;
INSERT INTO `quest_request_items` (ID, EmoteOnComplete, EmoteOnIncomplete, CompletionText) VALUES
  (91424, 1, 1, 'Has it bent the knee yet?');
DELETE FROM `quest_offer_reward` WHERE ID = 91424;
INSERT INTO `quest_offer_reward` (ID, Emote1, RewardText) VALUES
  (91424, 4, 'Yes... I can feel it on you, the cold of the Void. The bond is yours now, $N. Call it whenever you need something to stand between you and the teeth.');
DELETE FROM `creature_queststarter` WHERE quest = 91424;
INSERT INTO `creature_queststarter` (id, quest) VALUES (38797, 91424);
DELETE FROM `creature_questender` WHERE quest = 91424;
INSERT INTO `creature_questender` (id, quest) VALUES (38797, 91424);
DELETE FROM `creature_template` WHERE entry = 901023;
INSERT INTO `creature_template` SET
  entry = 901023, name = 'Unbound Voidwalker', minlevel = 10, maxlevel = 10, faction = 14, speed_walk = 1, speed_run = 1.14286,
  speed_swim = 1, speed_flight = 1, detection_range = 18, dmgschool = 5, DamageModifier = 0.9, BaseAttackTime = 2000,
  RangeAttackTime = 2000, BaseVariance = 1, RangeVariance = 1, unit_class = 1, unit_flags = 512, unit_flags2 = 2048, type = 3,
  AIName = 'SmartAI', MovementType = 1, HoverHeight = 1, HealthModifier = 1, ManaModifier = 1, ArmorModifier = 0.95,
  ExperienceModifier = 1, RegenHealth = 1, flags_extra = 2;
DELETE FROM `creature_template_model` WHERE CreatureID = 901023;
INSERT INTO `creature_template_model` (CreatureID, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild) VALUES (901023, 0, 1132, 1, 1, 0);
DELETE FROM `creature_text` WHERE CreatureID = 901023;
INSERT INTO `creature_text` (CreatureID, GroupID, ID, Text, Type, Language, Probability, Emote, Duration, Sound, BroadcastTextId, TextRange, comment) VALUES
  (901023, 0, 0, 'Who dares summon the power of the void?', 12, 8, 100, 0, 0, 0, 1986, 0, 'Unbound Voidwalker - summoned (stock 5676)'),
  (901023, 1, 0, 'You will live forever in torment for this, pathetic warlock.', 12, 8, 100, 0, 0, 0, 1987, 0, 'Unbound Voidwalker - aggro (stock 5676)'),
  (901023, 2, 0, 'Enough... The orb has spoken. I serve.', 12, 0, 100, 0, 0, 0, 0, 0, 'Unbound Voidwalker - submits (I-384)');
DELETE FROM `smart_scripts` WHERE entryorguid = 901023 AND source_type = 0;
DELETE FROM `smart_scripts` WHERE entryorguid IN (90102300, 90102301) AND source_type = 9;
INSERT INTO `smart_scripts` (entryorguid, source_type, id, link, event_type, event_phase_mask, event_chance, event_flags, event_param1, event_param2, event_param3, event_param4, event_param5, event_param6, action_type, action_param1, action_param2, action_param3, action_param4, action_param5, action_param6, target_type, target_param1, target_param2, target_param3, target_param4, target_x, target_y, target_z, target_o, comment) VALUES
  (901023, 0, 0, 0, 54, 0, 100, 1, 0, 0, 0, 0, 0, 0, 80, 90102300, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - On Just Summoned - Run Intro'),
  (901023, 0, 1, 0, 2, 0, 100, 1, 0, 30, 0, 0, 0, 0, 11, 7750, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Between 0-30% Health - Cast Consuming Rage'),
  (901023, 0, 2, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - On Aggro - Say Line 1'),
  (901023, 0, 3, 0, 21, 0, 100, 0, 0, 0, 0, 0, 0, 0, 41, 1000, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - On Reached Home - Despawn'),
  (901023, 0, 4, 0, 2, 0, 100, 1, 0, 15, 0, 0, 0, 0, 80, 90102301, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Between 0-15% Health - Run Submit'),
  (90102300, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 42, 0, 10, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Invincible below 10% health'),
  (90102300, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 35, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Set Faction 35'),
  (90102300, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 7741, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Cast Summoned Demon'),
  (90102300, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Say Line 0'),
  (90102300, 9, 4, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 2, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Set Faction 14'),
  (90102300, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Start Attacking'),
  (90102301, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 35, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Set Faction 35'),
  (90102301, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Combat Stop'),
  (90102301, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Set Passive'),
  (90102301, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Emote Bow'),
  (90102301, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Say Line 2'),
  (90102301, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 901023, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Kill Credit to Summoner'),
  (90102301, 9, 6, 0, 0, 0, 100, 0, 2500, 2500, 0, 0, 0, 0, 86, 697, 2, 23, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Summoner casts Summon Voidwalker (triggered)'),
  (90102301, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Despawn');
-- the orb's event summons the voidwalker on the circle, 3 min despawn (stock 1787 pattern)
DELETE FROM `event_scripts` WHERE id = 901026;
INSERT INTO `event_scripts` (id, delay, command, datalong, datalong2, dataint, x, y, z, o) VALUES
  (901026, 0, 10, 901023, 180000, 0, -2437.430, 1504.320, 19.536, 0);
-- the circle: stock look (display 465, size 2, 10 yd radius), its own focus 1652
DELETE FROM `gameobject_template` WHERE entry = 901020;
INSERT INTO `gameobject_template` (entry, type, displayId, name, size, Data0, Data1) VALUES (901020, 8, 465, 'Summoning Circle', 2, 1652, 10);
DELETE FROM `gameobject_template_addon` WHERE entry = 901020;
INSERT INTO `gameobject_template_addon` (entry, faction) VALUES (901020, 35);
DELETE FROM `gameobject` WHERE guid = 7009901;
INSERT INTO `gameobject` (guid, id, map, spawnMask, phaseMask, position_x, position_y, position_z, orientation, rotation0, rotation1, rotation2, rotation3, spawntimesecs, animprogress, state, Comment) VALUES
  (7009901, 901020, 0, 1, 3080, -2437.430, 1504.320, 19.536, 0, 0, 0, 0, 1, 300, 100, 1, '[I-384] Summoning Circle - Stormglen, by Vitus Darkwalker');

-- ---------------------------------------------------------------------------
-- Call of Fire (the Gilneas shaman trainer, F-029 only), as [I-377]'s Lost Isles chain
-- ---------------------------------------------------------------------------
DELETE FROM `creature_template` WHERE entry IN (901024, 901025);
INSERT INTO `creature_template` SET
  entry = 901024, name = 'Spirit of Fire', minlevel = 12, maxlevel = 12, faction = 35, npcflag = 2, speed_walk = 1,
  speed_run = 1.14286, speed_swim = 1, speed_flight = 1, detection_range = 18, DamageModifier = 1, BaseAttackTime = 2000,
  RangeAttackTime = 2000, BaseVariance = 1, RangeVariance = 1, unit_class = 1, unit_flags = 768, unit_flags2 = 2048, type = 4,
  HoverHeight = 2.5, HealthModifier = 1, ManaModifier = 1, ArmorModifier = 1, ExperienceModifier = 1, RegenHealth = 1, flags_extra = 2;
INSERT INTO `creature_template` SET
  entry = 901025, name = 'Raging Ember', minlevel = 10, maxlevel = 10, faction = 14, speed_walk = 1, speed_run = 0.857143,
  speed_swim = 1, speed_flight = 1, detection_range = 18, dmgschool = 2, DamageModifier = 1, BaseAttackTime = 2000,
  RangeAttackTime = 2000, BaseVariance = 1, RangeVariance = 1, unit_class = 1, unit_flags2 = 2048, type = 4, HoverHeight = 1,
  HealthModifier = 1, ManaModifier = 1, ArmorModifier = 1, ExperienceModifier = 1, RegenHealth = 1, CreatureImmunitiesId = -62,
  lootid = 901025, MovementType = 1;
DELETE FROM `creature_template_model` WHERE CreatureID IN (901024, 901025);
INSERT INTO `creature_template_model` (CreatureID, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild) VALUES
  (901024, 0, 2172, 2, 1, 0),  -- fire elemental (stock 5893's), 2x as [I-377]
  (901025, 0, 1405, 1.3, 1, 0); -- Living Flame (stock 3417)
-- hover as [I-377]: the HD pack's fire elemental hangs below its origin
DELETE FROM `creature_template_movement` WHERE CreatureId = 901024;
INSERT INTO `creature_template_movement` (CreatureId, Ground, Swim, Flight, Rooted, Chase, Random, InteractionPauseTimer) VALUES
  (901024, 2, 1, 0, 0, 0, 0, 0);
DELETE FROM `creature_loot_template` WHERE Entry = 901025;
INSERT INTO `creature_loot_template` (Entry, Item, Reference, Chance, QuestRequired, LootMode, GroupId, MinCount, MaxCount, Comment) VALUES
  (901025, 3857, 0, 20, 0, 1, 0, 1, 1, 'I-384 Raging Ember - Coal');
DELETE FROM `creature` WHERE guid BETWEEN 13009911 AND 13009919;
INSERT INTO `creature` (guid, id, map, spawnMask, phaseMask, position_x, position_y, position_z, orientation, spawntimesecs, wander_distance, MovementType, Comment) VALUES
  (13009911, 901024, 0, 1, 3080, -2426.410, 1355.010, 15.041, 0, 60, 0, 0, '[I-384] Spirit of Fire - south of Stormglen'),
  (13009912, 901025, 0, 1, 3080, -2470.106, 1345.010, 16.913, 4.803, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009913, 901025, 0, 1, 3080, -2477.214, 1313.201, 16.702, 4.582, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009914, 901025, 0, 1, 3080, -2456.625, 1362.406, 16.814, 1.657, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009915, 901025, 0, 1, 3080, -2297.474, 1301.253, 7.231, 1.482, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009916, 901025, 0, 1, 3080, -2318.759, 1390.335, -2.344, 1.554, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009917, 901025, 0, 1, 3080, -2443.904, 1308.627, 17.271, 6.204, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009918, 901025, 0, 1, 3080, -2391.846, 1316.847, 13.116, 5.638, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen'),
  (13009919, 901025, 0, 1, 3080, -2437.761, 1469.402, 16.842, 0.331, 180, 6, 1, '[I-384] Raging Ember - south of Stormglen');
DELETE FROM `quest_template` WHERE ID BETWEEN 91425 AND 91427;
INSERT INTO `quest_template` SET
  ID = 91425, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -82, RewardNextQuest = 91426, RewardXPDifficulty = 2,
  AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2, LogTitle = 'Call of Fire',
  LogDescription = 'Speak with the Spirit of Fire in the burning woods south of Stormglen.',
  QuestDescription = 'The Forsaken came over the wall with fire, $N, and they left it behind them. The woods south of Stormglen are still burning, and the earth tells me something in the flames is angry.$B$BFire is the hardest of the elements to speak with. It does not listen; it consumes. But if you mean to walk the old ways, you will have to face it. Go to the burning woods and speak with the spirit there.',
  QuestCompletionLog = 'Speak with the Spirit of Fire.';
INSERT INTO `quest_template` SET
  ID = 91426, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -82, RewardNextQuest = 91427, RewardXPDifficulty = 4,
  AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2, RequiredNpcOrGo1 = 901025, RequiredNpcOrGoCount1 = 6,
  ObjectiveText1 = 'Raging Ember destroyed', LogTitle = 'Tempers Flare',
  LogDescription = 'Destroy 6 Raging Embers in the woods south of Stormglen, then return to the Spirit of Fire.',
  QuestDescription = 'They threw fire at your walls, little shaman, fire with no master and no purpose but to burn. It has taken root in these woods, and from my anger it has taken shape.$B$BFire that only destroys is fire without a master. Put out the embers, and show me you can stand in the heat without being consumed.',
  QuestCompletionLog = 'Return to the Spirit of Fire south of Stormglen.';
INSERT INTO `quest_template` SET
  ID = 91427, QuestType = 2, QuestLevel = 10, MinLevel = 10, QuestSortID = -82, RewardXPDifficulty = 5,
  RewardSpell = 2075, RewardDisplaySpell = 3599, RewardItem1 = 5176, RewardAmount1 = 1, StartItem = 6654,
  AllowableRaces = @WorgenMask, `AllowableRaces_2` = @WorgenMask_2, RequiredItemId1 = 6654, RequiredItemCount1 = 1,
  LogTitle = 'Call of Fire', LogDescription = 'Bring the Torch of the Eternal Flame to your shaman trainer in Stormglen.',
  QuestDescription = 'It is done. The woods will burn out in their own time, and grow again.$B$BTake this torch. A spark of me burns in it and will not go out. Carry it to the one who sent you, and let him bind it to a totem for you.',
  QuestCompletionLog = 'Return to your shaman trainer.';
DELETE FROM `quest_template_addon` WHERE ID BETWEEN 91425 AND 91427;
INSERT INTO `quest_template_addon` (ID, AllowableClasses, PrevQuestID, ProvidedItemCount) VALUES
  (91425, 64, 0, 0), (91426, 64, 91425, 0), (91427, 64, 91426, 1);
DELETE FROM `quest_request_items` WHERE ID BETWEEN 91425 AND 91427;
INSERT INTO `quest_request_items` (ID, EmoteOnComplete, EmoteOnIncomplete, CompletionText) VALUES
  (91426, 1, 1, 'The embers still burn, little shaman. I feel every one.'),
  (91427, 1, 1, 'You smell of smoke. Tell me that''s the torch.');
DELETE FROM `quest_offer_reward` WHERE ID BETWEEN 91425 AND 91427;
INSERT INTO `quest_offer_reward` (ID, Emote1, RewardText) VALUES
  (91425, 1, 'Another of the walled-in people. You hid from the world for years, and the world came over the wall anyway. ... But you came here to listen. That is rare. Listen, then.'),
  (91426, 2, 'Quieter. You did not run from the heat, and you did not burn more than you had to. That is the first lesson fire teaches.'),
  (91427, 273, 'An eternal flame. I''d not have believed it if I weren''t holding it. Hold still while I bind it into a totem for you, $N. Plant it, and let the fire fight for you.');
DELETE FROM `creature_queststarter` WHERE quest BETWEEN 91425 AND 91427;
INSERT INTO `creature_queststarter` (id, quest) VALUES
  (@GilneasShamanTrainerCreatureID, 91425), (901024, 91426), (901024, 91427);
DELETE FROM `creature_questender` WHERE quest BETWEEN 91425 AND 91427;
INSERT INTO `creature_questender` (id, quest) VALUES
  (901024, 91425), (901024, 91426), (@GilneasShamanTrainerCreatureID, 91427);
-- without F-029 there is no Gilneas shaman trainer, and no embers to keep in the woods
DELETE FROM `creature` WHERE guid BETWEEN 13009911 AND 13009919 AND NOT @GilneasAracTrainers;

-- Quest POIs (Gilneas, WorldMapArea 545)
DELETE FROM `quest_poi` WHERE QuestID IN (91420, 91421, 91422, 91423, 91424, 91425, 91426, 91427);
INSERT INTO `quest_poi` (QuestID, id, ObjectiveIndex, MapID, WorldMapAreaId, Floor, Priority, Flags, VerifiedBuild) VALUES
  (91420, 0, -1, 0, 545, 0, 0, 1, 0), (91420, 1, 0, 0, 545, 0, 0, 1, 0),
  (91421, 0, -1, 0, 545, 0, 0, 1, 0), (91421, 1, 0, 0, 545, 0, 0, 1, 0),
  (91422, 0, -1, 0, 545, 0, 0, 1, 0), (91422, 1, 0, 0, 545, 0, 0, 1, 0),
  (91423, 0, -1, 0, 545, 0, 0, 1, 0),
  (91424, 0, -1, 0, 545, 0, 0, 1, 0), (91424, 1, 0, 0, 545, 0, 0, 1, 0),
  (91425, 0, -1, 0, 545, 0, 0, 1, 0), (91426, 0, -1, 0, 545, 0, 0, 1, 0), (91426, 1, 0, 0, 545, 0, 0, 1, 0), (91427, 0, -1, 0, 545, 0, 0, 1, 0);
DELETE FROM `quest_poi_points` WHERE QuestID IN (91420, 91421, 91422, 91423, 91424, 91425, 91426, 91427);
INSERT INTO `quest_poi_points` (QuestID, Idx1, Idx2, X, Y, VerifiedBuild) VALUES
  (91420, 0, 0, -2437, 1537, 0), (91420, 1, 0, -2285, 1300, 0), (91420, 1, 1, -2285, 1488, 0), (91420, 1, 2, -2481, 1488, 0), (91420, 1, 3, -2481, 1300, 0),
  (91421, 0, 0, -2437, 1537, 0), (91421, 1, 0, -1919, 1731, 0), (91421, 1, 1, -1919, 1860, 0), (91421, 1, 2, -2092, 1860, 0), (91421, 1, 3, -2092, 1731, 0),
  (91422, 0, 0, -2437, 1537, 0), (91422, 1, 0, -2004, 1378, 0), (91422, 1, 1, -2004, 1676, 0), (91422, 1, 2, -2308, 1676, 0), (91422, 1, 3, -2308, 1378, 0),
  (91423, 0, 0, -2437, 1537, 0),
  (91424, 0, 0, -2444, 1497, 0), (91424, 1, 0, -2437, 1504, 0),
  (91425, 0, 0, -2426, 1355, 0), (91426, 0, 0, -2426, 1355, 0), (91426, 1, 0, -2282, 1286, 0), (91426, 1, 1, -2282, 1484, 0), (91426, 1, 2, -2492, 1484, 0), (91426, 1, 3, -2492, 1286, 0), (91427, 0, 0, -2454, 1535, 0);
