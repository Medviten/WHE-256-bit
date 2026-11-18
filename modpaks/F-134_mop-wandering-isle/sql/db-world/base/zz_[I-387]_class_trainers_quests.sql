-- ============================================================================
-- I-387 Wandering Isle class trainers and class quests
-- ============================================================================
-- Mists of Pandaria taught spells as characters levelled, so the Wandering Isle
-- has no class trainers, and its level-4 and level-10 class quests are missing
-- too: on 3.3.5a Pandaren couldn't train until they left the island. Now:
-- - a trainer per class in the middle of Master Shang Xi's training grounds
--   (901030-901038); the ARAC classes' (paladin, warlock, druid) only with F-029
--   (@AllTrainersEnabled)
-- - level-4 practice quests at each (91430-91438, as F-029's Cataclysm ones):
--   the spell on the training targets (53714, credit 901040) or a heal on the
--   Injured Trainees (901041) beside them; every rank gives credit
-- - the shaman trainer gives ARAC's Call of Earth (92801 / 92802) when F-002
--   is in the manifest
-- - level-10 chains at Korga Strongmane's camp by the Wreck of the Skyseeker,
--   where the hunter, shaman, warlock and druid trainers also stand: Taming the
--   Beast (Ash Moth, Pei-Wu Tiger Cub, Pei-Wu Tiger; 91440-91443), Creature of
--   the Void (91444, a summoning circle at the camp), Call of Fire (91445-91447,
--   Spirit of Fire and 8 Raging Embers in the Pei-Wu Forest), Bear Form
--   (91448-91449, Great Bear Spirit and Echoes of Lunaclaw by the tiger cubs)
-- Spots are existing spawns' (ground) or the flat target field; not yet checked
-- in game. Spells, rods, orb and spell focus are dbc/[I-387]_*; the rods need
-- F-013's core patch (the I-376 rod fallback).
-- ============================================================================
SET @AracTrainers = COALESCE(@AllTrainersEnabled, 0) <> 0;

DELETE FROM `creature_template` WHERE `entry` IN (901030, 901031, 901032, 901033, 901034, 901035, 901036, 901037, 901038, 901040, 901041, 901042, 901043, 901044, 901045, 901046, 901047, 901048, 901049);
INSERT INTO `creature_template` (`entry`, `difficulty_entry_1`, `difficulty_entry_2`, `difficulty_entry_3`, `KillCredit1`, `KillCredit2`, `name`, `subname`, `IconName`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `speed_swim`, `speed_flight`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `BaseVariance`, `RangeVariance`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `pickpocketloot`, `skinloot`, `PetSpellDataId`, `VehicleId`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HoverHeight`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RacialLeader`, `movementId`, `RegenHealth`, `CreatureImmunitiesId`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
  (901030, 0, 0, 0, 0, 0, 'Master Tsao Ironpalm', 'Warrior Trainer', NULL, 4645, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901031, 0, 0, 0, 0, 0, 'Master Lien Sunwatch', 'Paladin Trainer', NULL, 7260, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901032, 0, 0, 0, 0, 0, 'Master Huo Longsight', 'Hunter Trainer', NULL, 4010, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901033, 0, 0, 0, 0, 0, 'Master Shen Quietstep', 'Rogue Trainer', NULL, 410, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901034, 0, 0, 0, 0, 0, 'Master Ying Brightsoul', 'Priest Trainer', NULL, 4665, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901035, 0, 0, 0, 0, 0, 'Master Bo Earthsong', 'Shaman Trainer', NULL, 4103, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901036, 0, 0, 0, 0, 0, 'Master Liu Starfan', 'Mage Trainer', NULL, 4661, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901037, 0, 0, 0, 0, 0, 'Master Gao Shadowbrew', 'Warlock Trainer', NULL, 4667, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901038, 0, 0, 0, 0, 0, 'Master Ren Leafwhisper', 'Druid Trainer', NULL, 4605, 10, 10, 0, 35, 51, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901040, 0, 0, 0, 0, 0, 'Practice Credit', 'I-387 credit', NULL, 0, 1, 1, 0, 35, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 33554432, 2048, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 130, '', 0),
  (901041, 0, 0, 0, 0, 0, 'Injured Trainee', NULL, NULL, 0, 5, 5, 0, 35, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 0, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'SmartAI', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901042, 0, 0, 0, 0, 0, 'Ash Moth tamed', 'I-387 credit', NULL, 0, 1, 1, 0, 35, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 33554432, 2048, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 130, '', 0),
  (901043, 0, 0, 0, 0, 0, 'Pei-Wu Tiger Cub tamed', 'I-387 credit', NULL, 0, 1, 1, 0, 35, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 33554432, 2048, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 130, '', 0),
  (901044, 0, 0, 0, 0, 0, 'Pei-Wu Tiger tamed', 'I-387 credit', NULL, 0, 1, 1, 0, 35, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 33554432, 2048, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 130, '', 0),
  (901045, 0, 0, 0, 0, 0, 'Unbound Voidwalker', NULL, NULL, 0, 10, 10, 0, 14, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 512, 2048, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 'SmartAI', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 2, '', 0),
  (901046, 0, 0, 0, 0, 0, 'Spirit of Fire', NULL, NULL, 0, 12, 12, 0, 35, 2, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 768, 2048, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 2, '', 0),
  (901047, 0, 0, 0, 0, 0, 'Raging Ember', NULL, NULL, 0, 10, 10, 0, 14, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 0, 2048, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (901048, 0, 0, 0, 0, 0, 'Great Bear Spirit', NULL, NULL, 0, 60, 60, 0, 35, 2, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 768, 2048, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 2, '', 0),
  (901049, 0, 0, 0, 0, 0, 'Echo of Lunaclaw', NULL, NULL, 0, 10, 10, 0, 14, 0, 1, 1.14286, 1, 1, 18, 0, 0, 1, 2000, 2000, 1, 1, 1, 0, 2048, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0);
UPDATE `creature_template` SET `dmgschool` = 5, `DamageModifier` = 0.9, `ArmorModifier` = 0.95, `MovementType` = 1 WHERE `entry` = 901045;
UPDATE `creature_template` SET `dmgschool` = 2, `CreatureImmunitiesId` = -62, `lootid` = 901047, `MovementType` = 1 WHERE `entry` = 901047;
UPDATE `creature_template` SET `family` = 4, `HealthModifier` = 1.5, `MovementType` = 1 WHERE `entry` = 901049;
UPDATE `creature_template` SET `HoverHeight` = 2.5 WHERE `entry` = 901046;
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (901030, 901031, 901032, 901033, 901034, 901035, 901036, 901037, 901038, 901040, 901041, 901042, 901043, 901044, 901045, 901046, 901047, 901048, 901049);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
  (901030, 0, 44069, 1, 1, 0),
  (901031, 0, 44070, 1, 1, 0),
  (901032, 0, 44071, 1, 1, 0),
  (901033, 0, 44072, 1, 1, 0),
  (901034, 0, 45864, 1, 1, 0),
  (901035, 0, 45865, 1, 1, 0),
  (901036, 0, 45866, 1, 1, 0),
  (901037, 0, 45867, 1, 1, 0),
  (901038, 0, 45872, 1, 1, 0),
  (901040, 0, 11686, 1, 1, 0),
  (901041, 0, 44073, 1, 1, 0),
  (901042, 0, 11686, 1, 1, 0),
  (901043, 0, 11686, 1, 1, 0),
  (901044, 0, 11686, 1, 1, 0),
  (901045, 0, 1132, 1, 1, 0),
  (901046, 0, 2172, 2, 1, 0),
  (901047, 0, 1405, 1.3, 1, 0),
  (901048, 0, 11909, 1, 1, 0),
  (901049, 0, 9389, 1, 1, 0);
DELETE FROM `creature_template_movement` WHERE `CreatureId` = 901046;
INSERT INTO `creature_template_movement` (`CreatureId`, `Ground`, `Swim`, `Flight`, `Rooted`, `Chase`, `Random`, `InteractionPauseTimer`) VALUES (901046, 2, 1, 0, 0, 0, 0, 0);
DELETE FROM `creature_template_addon` WHERE `entry` = 901041;
INSERT INTO `creature_template_addon` (`entry`, `path_id`, `mount`, `bytes1`, `bytes2`, `emote`, `visibilityDistanceType`, `auras`) VALUES (901041, 0, 0, 8, 0, 0, 0, NULL);  -- kneeling
DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN (901030, 901031, 901032, 901033, 901034, 901035, 901036, 901037, 901038);
INSERT INTO `creature_default_trainer` (`CreatureId`, `TrainerId`) VALUES
  (901030, 1),
  (901031, 3),
  (901032, 7),
  (901033, 9),
  (901034, 11),
  (901035, 14),
  (901036, 16),
  (901037, 31),
  (901038, 33);
DELETE FROM `creature_loot_template` WHERE `Entry` = 901047;
INSERT INTO `creature_loot_template` (`Entry`, `Item`, `Reference`, `Chance`, `QuestRequired`, `LootMode`, `GroupId`, `MinCount`, `MaxCount`, `Comment`) VALUES (901047, 3857, 0, 20, 0, 1, 0, 1, 1, 'I-387 Raging Ember - Coal');
UPDATE `creature_template` SET `type_flags` = `type_flags` | 1 WHERE `entry` = 56174;  -- Pei-Wu Tiger Cub: tameable, as the grown tigers
DELETE FROM `creature` WHERE `guid` BETWEEN 13409901 AND 13410000;
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `MovementType`, `Comment`) VALUES
  (13409901, 901030, 860, 0, 0, 1, 1, 0, 1477.0, 3431.0, 171.1, 3.142, 300, 0, 0, 0, '[I-387] Warrior trainer - training grounds'),
  (13409902, 901031, 860, 0, 0, 1, 1, 0, 1475.36, 3435.5, 171.1, 3.84, 300, 0, 0, 0, '[I-387] Paladin trainer - training grounds'),
  (13409903, 901032, 860, 0, 0, 1, 1, 0, 1471.22, 3437.89, 171.1, 4.538, 300, 0, 0, 0, '[I-387] Hunter trainer - training grounds'),
  (13409904, 901033, 860, 0, 0, 1, 1, 0, 1466.5, 3437.06, 171.1, 5.236, 300, 0, 0, 0, '[I-387] Rogue trainer - training grounds'),
  (13409905, 901034, 860, 0, 0, 1, 1, 0, 1463.42, 3433.39, 171.1, 5.934, 300, 0, 0, 0, '[I-387] Priest trainer - training grounds'),
  (13409906, 901035, 860, 0, 0, 1, 1, 0, 1463.42, 3428.61, 171.1, 0.349, 300, 0, 0, 0, '[I-387] Shaman trainer - training grounds'),
  (13409907, 901036, 860, 0, 0, 1, 1, 0, 1466.5, 3424.94, 171.1, 1.047, 300, 0, 0, 0, '[I-387] Mage trainer - training grounds'),
  (13409908, 901037, 860, 0, 0, 1, 1, 0, 1471.22, 3424.11, 171.1, 1.745, 300, 0, 0, 0, '[I-387] Warlock trainer - training grounds'),
  (13409909, 901038, 860, 0, 0, 1, 1, 0, 1475.36, 3426.5, 171.1, 2.443, 300, 0, 0, 0, '[I-387] Druid trainer - training grounds'),
  (13409910, 901041, 860, 0, 0, 1, 1, 0, 1479.19, 3440.19, 171.1, 3.927, 60, 0, 0, 0, '[I-387] Injured Trainee - training grounds'),
  (13409911, 901041, 860, 0, 0, 1, 1, 0, 1460.81, 3440.19, 171.1, 5.498, 60, 0, 0, 0, '[I-387] Injured Trainee - training grounds'),
  (13409912, 901041, 860, 0, 0, 1, 1, 0, 1460.81, 3421.81, 171.1, 0.785, 60, 0, 0, 0, '[I-387] Injured Trainee - training grounds'),
  (13409913, 901041, 860, 0, 0, 1, 1, 0, 1479.19, 3421.81, 171.1, 2.356, 60, 0, 0, 0, '[I-387] Injured Trainee - training grounds'),
  (13409914, 901032, 860, 0, 0, 1, 1, 0, 422.7, 3648.0, 92.59, 5.61, 300, 0, 0, 0, '[I-387] Hunter trainer - Korga''s camp'),
  (13409915, 901035, 860, 0, 0, 1, 1, 0, 426.9, 3620.0, 92.9, 0.85, 300, 0, 0, 0, '[I-387] Shaman trainer - Korga''s camp'),
  (13409916, 901037, 860, 0, 0, 1, 1, 0, 420.1, 3617.3, 93.31, 2.51, 300, 0, 0, 0, '[I-387] Warlock trainer - Korga''s camp'),
  (13409917, 901038, 860, 0, 0, 1, 1, 0, 418.7, 3648.0, 92.59, 5.61, 300, 0, 0, 0, '[I-387] Druid trainer - Korga''s camp'),
  (13409918, 901046, 860, 0, 0, 1, 1, 0, 277.49, 3578.94, 79.36, 0, 60, 0, 0, 0, '[I-387] Spirit of Fire - Pei-Wu Forest'),
  (13409919, 901047, 860, 0, 0, 1, 1, 0, 312.41, 3445.92, 90.14, 0.803, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409920, 901047, 860, 0, 0, 1, 1, 0, 358.62, 3456.01, 94.17, 3.364, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409921, 901047, 860, 0, 0, 1, 1, 0, 258.93, 3472.1, 87.22, 5.224, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409922, 901047, 860, 0, 0, 1, 1, 0, 298.42, 3502.47, 93.81, 6.026, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409923, 901047, 860, 0, 0, 1, 1, 0, 261.2, 3524.03, 94.25, 1.331, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409924, 901047, 860, 0, 0, 1, 1, 0, 283.35, 3749.05, 79.91, 1.707, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409925, 901047, 860, 0, 0, 1, 1, 0, 214.58, 3718.74, 71.28, 1.954, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409926, 901047, 860, 0, 0, 1, 1, 0, 294.29, 3707.78, 78.7, 4.279, 180, 6, 0, 1, '[I-387] Raging Ember - Pei-Wu Forest'),
  (13409927, 901048, 860, 0, 0, 1, 1, 0, 318.01, 3453.54, 91.35, 0, 60, 0, 0, 0, '[I-387] Great Bear Spirit - Pei-Wu Forest'),
  (13409928, 901049, 860, 0, 0, 1, 1, 0, 324.07, 3453.04, 91.17, 5.434, 60, 3, 0, 1, '[I-387] Echo of Lunaclaw - Pei-Wu Forest'),
  (13409929, 901049, 860, 0, 0, 1, 1, 0, 267.31, 3520.56, 94.85, 2.379, 60, 3, 0, 1, '[I-387] Echo of Lunaclaw - Pei-Wu Forest'),
  (13409930, 901049, 860, 0, 0, 1, 1, 0, 496.81, 3692.98, 83.7, 1.37, 60, 3, 0, 1, '[I-387] Echo of Lunaclaw - Pei-Wu Forest');
-- the ARAC classes' trainers, and the druid chain's NPCs, only with F-029
DELETE FROM `creature` WHERE `guid` BETWEEN 13409901 AND 13410000 AND `id` IN (901037, 901031, 901038, 901048, 901049) AND NOT @AracTrainers;
-- ---------------------------------------------------------------------------
-- Quests
-- ---------------------------------------------------------------------------
DELETE FROM `quest_template` WHERE `ID` IN (91430, 91431, 91432, 91433, 91434, 91435, 91436, 91437, 91438, 91440, 91441, 91442, 91443, 91444, 91445, 91446, 91447, 91448, 91449);
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `RewardXPDifficulty`, `RewardMoneyDifficulty`, `AllowableRaces`, `AllowableRaces_2`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`, `ObjectiveText1`, `LogTitle`, `LogDescription`, `QuestDescription`) VALUES
  (91430, 2, 4, 4, -81, 3, 60, 0, 0, 901040, 1, 'Practice Charge', 'Charge', 'Learn Charge from Master Tsao Ironpalm, then practise it on the training targets at Master Shang Xi''s training grounds.', 'Strength is nothing without the will to close the distance, $N. I will teach you to Charge, to cross the field before your enemy can raise a guard.$B$BLearn it from me, then try it on the training targets around us.'),
  (91431, 2, 4, 4, -141, 3, 60, 0, 0, 901040, 1, 'Practice Judgement', 'Judgement', 'Learn Judgement from Master Lien Sunwatch, then practise it on the training targets at Master Shang Xi''s training grounds.', 'The Light is not so different from the harmony we seek, $N. Let me show you how to carry it into battle: a Seal to bind it to your weapon, and Judgement to unleash it.$B$BLearn it from me, then try it on the training targets around us.'),
  (91432, 2, 4, 4, -261, 3, 60, 0, 0, 901040, 5, 'Practice Serpent Sting', 'Serpent Sting', 'Learn Serpent Sting from Master Huo Longsight, then practise it 5 times on the training targets at Master Shang Xi''s training grounds.', 'A hunter does not need to win in one strike, $N. A sting will keep working long after the arrow lands.$B$BLearn Serpent Sting from me, then practise it on the training targets around us.'),
  (91433, 2, 4, 4, -162, 3, 60, 0, 0, 901040, 3, 'Practice Eviscerate', 'Eviscerate', 'Learn Eviscerate from Master Shen Quietstep, then practise it 3 times on the training targets at Master Shang Xi''s training grounds.', 'Patience, then one decisive cut. That is our way, $N. Build your advantage, then finish it with Eviscerate.$B$BLearn it from me, then practise it on the training targets around us.'),
  (91434, 2, 4, 4, -262, 3, 60, 0, 0, 901041, 3, 'Practice Lesser Heal', 'Lesser Heal', 'Learn Lesser Heal from Master Ying Brightsoul, then practise it 3 times on the Injured Trainees at Master Shang Xi''s training grounds.', 'Not every lesson here leaves a student standing, $N. The injured trainees around us could use a gentle hand.$B$BLearn Lesser Heal from me, then use it on them.'),
  (91435, 2, 4, 4, -82, 3, 60, 0, 0, 901040, 3, 'Practice Earth Shock', 'Earth Shock', 'Learn Earth Shock from Master Bo Earthsong, then practise it 3 times on the training targets at Master Shang Xi''s training grounds.', 'This island is a living turtle, $N, and the earth on its back has a voice. Let it lend you its strength.$B$BLearn Earth Shock from me, then try it on the training targets around us.'),
  (91436, 2, 4, 4, -161, 3, 60, 0, 0, 901040, 2, 'Practice Frostbolt', 'Frostbolt', 'Learn Frostbolt from Master Liu Starfan, then practise it 2 times on the training targets at Master Shang Xi''s training grounds.', 'Fire is not the only answer, $N. Cold slows the hasty and humbles the proud.$B$BLearn Frostbolt from me, then try it on the training targets around us.'),
  (91437, 2, 4, 4, -61, 3, 60, 0, 0, 901040, 5, 'Practice Immolate', 'Immolate', 'Learn Immolate from Master Gao Shadowbrew, then practise it 5 times on the training targets at Master Shang Xi''s training grounds.', 'Every fire begins as a small flame, $N. Let me show you one that keeps burning.$B$BLearn Immolate from me, then practise it on the training targets around us.'),
  (91438, 2, 4, 4, -263, 3, 60, 0, 0, 901041, 2, 'Practice Rejuvenation', 'Rejuvenation', 'Learn Rejuvenation from Master Ren Leafwhisper, then practise it 2 times on the Injured Trainees at Master Shang Xi''s training grounds.', 'The bamboo bends and grows back stronger, $N. The same green power can mend a body, slowly and surely.$B$BLearn Rejuvenation from me, then use it on the injured trainees around us.');
INSERT INTO `quest_template` (`ID`, `QuestType`, `QuestLevel`, `MinLevel`, `QuestSortID`, `RewardNextQuest`, `RewardXPDifficulty`, `RewardDisplaySpell`, `RewardSpell`, `RewardItem1`, `RewardAmount1`, `StartItem`, `Flags`, `AllowableRaces`, `AllowableRaces_2`, `RequiredItemId1`, `RequiredItemCount1`, `RequiredNpcOrGo1`, `RequiredNpcOrGoCount1`, `ObjectiveText1`, `LogTitle`, `LogDescription`, `QuestDescription`, `QuestCompletionLog`) VALUES
  (91440, 2, 10, 10, -261, 91441, 5, 0, 0, 0, 0, 84610, 2, 0, 0, 84610, 1, 901042, 1, 'Ash Moth tamed', 'Taming the Beast', 'Use the Taming Rod to tame a Ash Moth in the Pei-Wu Forest, then return the rod to Master Huo Longsight.', 'Every companion starts with trust, $N. Begin with something gentle. The Ash Moths of the Pei-Wu Forest drift close to the camp. Use this Taming Rod on one and hold its attention until it is yours.$B$BThen bring the rod back.', 'Return the Taming Rod to Master Huo Longsight.'),
  (91441, 2, 10, 10, -261, 91442, 5, 0, 0, 0, 0, 84611, 2, 0, 0, 84611, 1, 901043, 1, 'Pei-Wu Tiger Cub tamed', 'Taming the Beast', 'Use the Taming Rod to tame a Pei-Wu Tiger Cub in the Pei-Wu Forest, then return the rod to Master Huo Longsight.', 'The tiger cubs of the Pei-Wu Forest are playful and proud. Win one over and you will learn that patience is stronger than force.$B$BTake this rod.', 'Return the Taming Rod to Master Huo Longsight.'),
  (91442, 2, 10, 10, -261, 91443, 5, 23356, 1579, 0, 0, 84612, 2, 0, 0, 84612, 1, 901044, 1, 'Pei-Wu Tiger tamed', 'Taming the Beast', 'Use the Taming Rod to tame a Pei-Wu Tiger in the Pei-Wu Forest, then return the rod to Master Huo Longsight.', 'Last one. The grown tigers of the Pei-Wu Forest answer to no one. Choose one you can handle; some of them are far stronger than you.$B$BHere is your last rod.', 'Return the Taming Rod to Master Huo Longsight.'),
  (91443, 2, 10, 10, -261, 0, 3, 23357, 5300, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, '', 'Training the Beast', 'Speak to Master Huo Longsight.', 'Taming is the easy part, $N. A companion has to be fed and trained, or it will be no use to you.$B$BLet me show you how to teach your pet. Then go and find one worth keeping.', ''),
  (91444, 2, 10, 10, -61, 0, 4, 697, 11520, 0, 0, 84613, 0, 0, 0, 84613, 1, 901045, 1, 'Voidwalker subjugated', 'Creature of the Void', 'Use the Attuned Orb of Dominion at the summoning circle in Korga Strongmane''s camp, subjugate the voidwalker that answers, then return the orb to Master Gao Shadowbrew.', 'An imp is a companion, $N. A voidwalker is a shield.$B$BThis orb holds the binding. Use it at the circle drawn in the camp, and something from the Void will answer. It will not come willingly. Beat it down until it remembers who called it, and it will serve you.$B$BThen bring the orb back.', 'Return the Orb of Dominion to Master Gao Shadowbrew.'),
  (91445, 2, 10, 10, -82, 91446, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', 'Call of Fire', 'Speak with the Spirit of Fire in the Pei-Wu Forest.', 'The Zhao-Ren set the Pei-Wu Forest smouldering, $N, and something in the flames is angry. Fire is the hardest of the elements to speak with: it does not listen, it consumes. Go and speak with the spirit there.', ''),
  (91446, 2, 10, 10, -82, 91447, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 901047, 6, 'Raging Ember destroyed', 'Tempers Flare', 'Destroy 6 Raging Embers in the Pei-Wu Forest, then return to the Spirit of Fire.', 'Fire without a master burns until nothing is left, little shaman. My anger has taken shape in these woods. Put out the embers, and show me you can stand in the heat without being consumed.', ''),
  (91447, 2, 10, 10, -82, 0, 5, 3599, 2075, 5176, 1, 6654, 0, 0, 0, 6654, 1, 0, 0, '', 'Call of Fire', 'Bring the Torch of the Eternal Flame to Master Bo Earthsong.', 'It is done. Take this torch; a spark of me burns in it and will not go out. Carry it to the one who sent you, and let them bind it to a totem for you.', ''),
  (91448, 2, 10, 10, -263, 91449, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', 'Heeding the Call', 'Speak with the Great Bear Spirit in the Pei-Wu Forest.', 'Something old walks among the tiger cubs of the Pei-Wu Forest, $N. The animals make way for it. I believe it is the spirit that teaches druids the shape of the bear.$B$BGo and listen to it.', ''),
  (91449, 2, 10, 10, -263, 0, 5, 19179, 19179, 0, 0, 0, 0, 0, 0, 0, 0, 901049, 1, 'Echo of Lunaclaw defeated', 'Body and Heart', 'Defeat an Echo of Lunaclaw in the Pei-Wu Forest, then return to Master Ren Leafwhisper.', 'The bear is strength, young druid, but strength without heart is only weight.$B$BAn echo of Lunaclaw walks these woods, a memory of one who once tested all who came to me. Face it. Show me your body can endure and your heart will not break, and the shape of the bear is yours.$B$BThen return to the one who sent you.', 'Return to Master Ren Leafwhisper.');
DELETE FROM `quest_template_addon` WHERE `ID` IN (91430, 91431, 91432, 91433, 91434, 91435, 91436, 91437, 91438, 91440, 91441, 91442, 91443, 91444, 91445, 91446, 91447, 91448, 91449);
INSERT INTO `quest_template_addon` (`ID`, `AllowableClasses`, `PrevQuestID`, `ProvidedItemCount`) VALUES
  (91430, 1, 0, 0),
  (91431, 2, 0, 0),
  (91432, 4, 0, 0),
  (91433, 8, 0, 0),
  (91434, 16, 0, 0),
  (91435, 64, 0, 0),
  (91436, 128, 0, 0),
  (91437, 256, 0, 0),
  (91438, 1024, 0, 0),
  (91440, 4, 0, 1),
  (91441, 4, 91440, 1),
  (91442, 4, 91441, 1),
  (91443, 4, 91442, 0),
  (91444, 256, 0, 1),
  (91445, 64, 0, 0),
  (91446, 64, 91445, 0),
  (91447, 64, 91446, 1),
  (91448, 1024, 0, 0),
  (91449, 1024, 91448, 0);
DELETE FROM `quest_request_items` WHERE `ID` IN (91430, 91431, 91432, 91433, 91434, 91435, 91436, 91437, 91438, 91440, 91441, 91442, 91443, 91444, 91445, 91446, 91447, 91448, 91449);
INSERT INTO `quest_request_items` (`ID`, `EmoteOnComplete`, `EmoteOnIncomplete`, `CompletionText`) VALUES
  (91440, 1, 1, 'Did the moth settle on your hand?'),
  (91441, 1, 1, 'Has the cub stopped biting yet?'),
  (91442, 1, 1, 'Did the tiger accept you?'),
  (91444, 1, 1, 'Has it bowed yet?'),
  (91446, 1, 1, 'The embers still burn, little shaman. I feel every one.'),
  (91447, 1, 1, 'You smell of smoke. Tell me that is the torch.'),
  (91449, 1, 1, 'Did the spirit find you worthy?');
DELETE FROM `quest_offer_reward` WHERE `ID` IN (91430, 91431, 91432, 91433, 91434, 91435, 91436, 91437, 91438, 91440, 91441, 91442, 91443, 91444, 91445, 91446, 91447, 91448, 91449);
INSERT INTO `quest_offer_reward` (`ID`, `Emote1`, `RewardText`) VALUES
  (91430, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91431, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91432, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91433, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91434, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91435, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91436, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91437, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91438, 4, 'Good. Your training has only begun, $N. Come back to me as you grow.'),
  (91440, 4, 'It follows the light of your spirit now. Next, something with claws.'),
  (91441, 4, 'A loyal cub. One more, $N, and you will need no rod at all.'),
  (91442, 4, 'From now on you can tame any beast you like, no rod required. Come back and I will teach you how to care for it.'),
  (91443, 4, 'Your pet will learn new tricks now, and you know how to feed it. Walk the path together, $N.'),
  (91444, 4, 'I can feel the cold of the Void on you. The bond is yours now, $N. Call it when you need a wall between you and harm.'),
  (91445, 4, 'Another child of the turtle. ... You came here to listen. That is rare. Listen, then.'),
  (91446, 4, 'Quieter. You did not run from the heat, and you did not burn more than you had to. That is the first lesson fire teaches.'),
  (91447, 4, 'An eternal flame. Hold still while I bind it into a totem for you, $N. Plant it, and let the fire fight beside you.'),
  (91448, 4, 'A child of the turtle, smelling of bamboo and tea. ... And yet the wild answered when you called. Listen, then.'),
  (91449, 4, 'Claws, fur, and a heart to match. The bear is yours now, $N. Use it wisely.');
DELETE FROM `creature_queststarter` WHERE `quest` IN (91430, 91431, 91432, 91433, 91434, 91435, 91436, 91437, 91438, 91440, 91441, 91442, 91443, 91444, 91445, 91446, 91447, 91448, 91449);
INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
  (901030, 91430),
  (901031, 91431),
  (901032, 91432),
  (901033, 91433),
  (901034, 91434),
  (901035, 91435),
  (901036, 91436),
  (901037, 91437),
  (901038, 91438),
  (901032, 91440),
  (901032, 91441),
  (901032, 91442),
  (901032, 91443),
  (901037, 91444),
  (901035, 91445),
  (901046, 91446),
  (901046, 91447),
  (901038, 91448),
  (901048, 91449);
DELETE FROM `creature_questender` WHERE `quest` IN (91430, 91431, 91432, 91433, 91434, 91435, 91436, 91437, 91438, 91440, 91441, 91442, 91443, 91444, 91445, 91446, 91447, 91448, 91449);
INSERT INTO `creature_questender` (`id`, `quest`) VALUES
  (901030, 91430),
  (901031, 91431),
  (901032, 91432),
  (901033, 91433),
  (901034, 91434),
  (901035, 91435),
  (901036, 91436),
  (901037, 91437),
  (901038, 91438),
  (901032, 91440),
  (901032, 91441),
  (901032, 91442),
  (901032, 91443),
  (901037, 91444),
  (901046, 91445),
  (901046, 91446),
  (901035, 91447),
  (901048, 91448),
  (901038, 91449);
-- ARAC's Call of Earth (F-002) from the island's shaman trainer, when F-002 is in the manifest
DELETE FROM `creature_queststarter` WHERE `id` = 901035 AND `quest` IN (92801, 92802);
DELETE FROM `creature_questender` WHERE `id` = 901035 AND `quest` IN (92801, 92802);
INSERT INTO `creature_queststarter` (`id`, `quest`) SELECT 901035, `ID` FROM `quest_template` WHERE `ID` IN (92801, 92802);
INSERT INTO `creature_questender` (`id`, `quest`) SELECT 901035, `ID` FROM `quest_template` WHERE `ID` IN (92801, 92802);
-- practice credit: any rank on a Training Target (Practice Credit) or an Injured Trainee
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` IN (53714, 901041) AND `id` BETWEEN 3000 AND 3999;
INSERT INTO `smart_scripts` (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`, `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`, `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`, `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`, `target_x`, `target_y`, `target_z`, `target_o`, `comment`) VALUES
  (53714, 0, 3000, 0, 8, 0, 100, 0, 100, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91430: credit when hit by 100 (I-387)'),
  (53714, 0, 3001, 0, 8, 0, 100, 0, 6178, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91430: credit when hit by 6178 (I-387)'),
  (53714, 0, 3002, 0, 8, 0, 100, 0, 11578, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91430: credit when hit by 11578 (I-387)'),
  (53714, 0, 3003, 0, 8, 0, 100, 0, 20271, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91431: credit when hit by 20271 (I-387)'),
  (53714, 0, 3004, 0, 8, 0, 100, 0, 53407, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91431: credit when hit by 53407 (I-387)'),
  (53714, 0, 3005, 0, 8, 0, 100, 0, 53408, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91431: credit when hit by 53408 (I-387)'),
  (53714, 0, 3006, 0, 8, 0, 100, 0, 1978, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 1978 (I-387)'),
  (53714, 0, 3007, 0, 8, 0, 100, 0, 13549, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13549 (I-387)'),
  (53714, 0, 3008, 0, 8, 0, 100, 0, 13550, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13550 (I-387)'),
  (53714, 0, 3009, 0, 8, 0, 100, 0, 13551, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13551 (I-387)'),
  (53714, 0, 3010, 0, 8, 0, 100, 0, 13552, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13552 (I-387)'),
  (53714, 0, 3011, 0, 8, 0, 100, 0, 13553, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13553 (I-387)'),
  (53714, 0, 3012, 0, 8, 0, 100, 0, 13554, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13554 (I-387)'),
  (53714, 0, 3013, 0, 8, 0, 100, 0, 13555, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 13555 (I-387)'),
  (53714, 0, 3014, 0, 8, 0, 100, 0, 25295, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 25295 (I-387)'),
  (53714, 0, 3015, 0, 8, 0, 100, 0, 27016, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 27016 (I-387)'),
  (53714, 0, 3016, 0, 8, 0, 100, 0, 49000, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 49000 (I-387)'),
  (53714, 0, 3017, 0, 8, 0, 100, 0, 49001, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91432: credit when hit by 49001 (I-387)'),
  (53714, 0, 3018, 0, 8, 0, 100, 0, 2098, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 2098 (I-387)'),
  (53714, 0, 3019, 0, 8, 0, 100, 0, 6760, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 6760 (I-387)'),
  (53714, 0, 3020, 0, 8, 0, 100, 0, 6761, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 6761 (I-387)'),
  (53714, 0, 3021, 0, 8, 0, 100, 0, 6762, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 6762 (I-387)'),
  (53714, 0, 3022, 0, 8, 0, 100, 0, 8623, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 8623 (I-387)'),
  (53714, 0, 3023, 0, 8, 0, 100, 0, 8624, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 8624 (I-387)'),
  (53714, 0, 3024, 0, 8, 0, 100, 0, 11299, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 11299 (I-387)'),
  (53714, 0, 3025, 0, 8, 0, 100, 0, 11300, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 11300 (I-387)'),
  (53714, 0, 3026, 0, 8, 0, 100, 0, 26865, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 26865 (I-387)'),
  (53714, 0, 3027, 0, 8, 0, 100, 0, 31016, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 31016 (I-387)'),
  (53714, 0, 3028, 0, 8, 0, 100, 0, 48667, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 48667 (I-387)'),
  (53714, 0, 3029, 0, 8, 0, 100, 0, 48668, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91433: credit when hit by 48668 (I-387)'),
  (901041, 0, 3000, 0, 8, 0, 100, 0, 2050, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91434: credit when hit by 2050 (I-387)'),
  (901041, 0, 3001, 0, 8, 0, 100, 0, 2052, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91434: credit when hit by 2052 (I-387)'),
  (901041, 0, 3002, 0, 8, 0, 100, 0, 2053, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91434: credit when hit by 2053 (I-387)'),
  (53714, 0, 3030, 0, 8, 0, 100, 0, 8042, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 8042 (I-387)'),
  (53714, 0, 3031, 0, 8, 0, 100, 0, 8044, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 8044 (I-387)'),
  (53714, 0, 3032, 0, 8, 0, 100, 0, 8045, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 8045 (I-387)'),
  (53714, 0, 3033, 0, 8, 0, 100, 0, 8046, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 8046 (I-387)'),
  (53714, 0, 3034, 0, 8, 0, 100, 0, 10412, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 10412 (I-387)'),
  (53714, 0, 3035, 0, 8, 0, 100, 0, 10413, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 10413 (I-387)'),
  (53714, 0, 3036, 0, 8, 0, 100, 0, 10414, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 10414 (I-387)'),
  (53714, 0, 3037, 0, 8, 0, 100, 0, 25454, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 25454 (I-387)'),
  (53714, 0, 3038, 0, 8, 0, 100, 0, 49230, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 49230 (I-387)'),
  (53714, 0, 3039, 0, 8, 0, 100, 0, 49231, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91435: credit when hit by 49231 (I-387)'),
  (53714, 0, 3040, 0, 8, 0, 100, 0, 116, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 116 (I-387)'),
  (53714, 0, 3041, 0, 8, 0, 100, 0, 205, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 205 (I-387)'),
  (53714, 0, 3042, 0, 8, 0, 100, 0, 837, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 837 (I-387)'),
  (53714, 0, 3043, 0, 8, 0, 100, 0, 7322, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 7322 (I-387)'),
  (53714, 0, 3044, 0, 8, 0, 100, 0, 8406, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 8406 (I-387)'),
  (53714, 0, 3045, 0, 8, 0, 100, 0, 8407, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 8407 (I-387)'),
  (53714, 0, 3046, 0, 8, 0, 100, 0, 8408, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 8408 (I-387)'),
  (53714, 0, 3047, 0, 8, 0, 100, 0, 10179, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 10179 (I-387)'),
  (53714, 0, 3048, 0, 8, 0, 100, 0, 10180, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 10180 (I-387)'),
  (53714, 0, 3049, 0, 8, 0, 100, 0, 10181, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 10181 (I-387)'),
  (53714, 0, 3050, 0, 8, 0, 100, 0, 25304, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 25304 (I-387)'),
  (53714, 0, 3051, 0, 8, 0, 100, 0, 27071, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 27071 (I-387)'),
  (53714, 0, 3052, 0, 8, 0, 100, 0, 27072, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 27072 (I-387)'),
  (53714, 0, 3053, 0, 8, 0, 100, 0, 38697, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 38697 (I-387)'),
  (53714, 0, 3054, 0, 8, 0, 100, 0, 42841, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 42841 (I-387)'),
  (53714, 0, 3055, 0, 8, 0, 100, 0, 42842, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91436: credit when hit by 42842 (I-387)'),
  (53714, 0, 3056, 0, 8, 0, 100, 0, 348, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 348 (I-387)'),
  (53714, 0, 3057, 0, 8, 0, 100, 0, 707, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 707 (I-387)'),
  (53714, 0, 3058, 0, 8, 0, 100, 0, 1094, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 1094 (I-387)'),
  (53714, 0, 3059, 0, 8, 0, 100, 0, 2941, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 2941 (I-387)'),
  (53714, 0, 3060, 0, 8, 0, 100, 0, 11665, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 11665 (I-387)'),
  (53714, 0, 3061, 0, 8, 0, 100, 0, 11667, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 11667 (I-387)'),
  (53714, 0, 3062, 0, 8, 0, 100, 0, 11668, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 11668 (I-387)'),
  (53714, 0, 3063, 0, 8, 0, 100, 0, 25309, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 25309 (I-387)'),
  (53714, 0, 3064, 0, 8, 0, 100, 0, 27215, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 27215 (I-387)'),
  (53714, 0, 3065, 0, 8, 0, 100, 0, 47810, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 47810 (I-387)'),
  (53714, 0, 3066, 0, 8, 0, 100, 0, 47811, 0, 0, 0, 0, 0, 33, 901040, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91437: credit when hit by 47811 (I-387)'),
  (901041, 0, 3003, 0, 8, 0, 100, 0, 774, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 774 (I-387)'),
  (901041, 0, 3004, 0, 8, 0, 100, 0, 1058, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 1058 (I-387)'),
  (901041, 0, 3005, 0, 8, 0, 100, 0, 1430, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 1430 (I-387)'),
  (901041, 0, 3006, 0, 8, 0, 100, 0, 2090, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 2090 (I-387)'),
  (901041, 0, 3007, 0, 8, 0, 100, 0, 2091, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 2091 (I-387)'),
  (901041, 0, 3008, 0, 8, 0, 100, 0, 3627, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 3627 (I-387)'),
  (901041, 0, 3009, 0, 8, 0, 100, 0, 8910, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 8910 (I-387)'),
  (901041, 0, 3010, 0, 8, 0, 100, 0, 9839, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 9839 (I-387)'),
  (901041, 0, 3011, 0, 8, 0, 100, 0, 9840, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 9840 (I-387)'),
  (901041, 0, 3012, 0, 8, 0, 100, 0, 9841, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 9841 (I-387)'),
  (901041, 0, 3013, 0, 8, 0, 100, 0, 25299, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 25299 (I-387)'),
  (901041, 0, 3014, 0, 8, 0, 100, 0, 26981, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 26981 (I-387)'),
  (901041, 0, 3015, 0, 8, 0, 100, 0, 26982, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 26982 (I-387)'),
  (901041, 0, 3016, 0, 8, 0, 100, 0, 48440, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 48440 (I-387)'),
  (901041, 0, 3017, 0, 8, 0, 100, 0, 48441, 0, 0, 0, 0, 0, 33, 901041, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 91438: credit when hit by 48441 (I-387)');
UPDATE `creature_template` SET `AIName` = 'SmartAI' WHERE `entry` IN (53714, 901041);
DELETE FROM `item_template` WHERE entry = 84610;
INSERT INTO `item_template` SET
  entry = 84610, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901040, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Ash Moth.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84611;
INSERT INTO `item_template` SET
  entry = 84611, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901041, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Pei-Wu Tiger Cub.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84612;
INSERT INTO `item_template` SET
  entry = 84612, class = 12, subclass = 0, name = 'Taming Rod', displayid = 26595, Quality = 1, Flags = 64, BuyCount = 1,
  ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901042, spelltrigger_1 = 0, spellcharges_1 = 3,
  spellcooldown_1 = -1, spellcategorycooldown_1 = -1, bonding = 4, description = 'Use on a Pei-Wu Tiger.', Material = -1;
DELETE FROM `item_template` WHERE entry = 84613;
INSERT INTO `item_template` SET
  entry = 84613, class = 12, subclass = 0, name = 'Attuned Orb of Dominion', displayid = 39424, Quality = 1, Flags = 64,
  BuyCount = 1, ItemLevel = 1, maxcount = 1, stackable = 1, spellid_1 = 901046, spelltrigger_1 = 0, spellcooldown_1 = -1,
  spellcategorycooldown_1 = -1, bonding = 4,
  description = 'Use at the summoning circle in Korga Strongmane''s camp to call and subjugate a voidwalker.', Material = 3;
DELETE FROM `conditions` WHERE SourceTypeOrReferenceId = 17 AND SourceEntry BETWEEN 901040 AND 901042;
INSERT INTO `conditions` (SourceTypeOrReferenceId, SourceGroup, SourceEntry, SourceId, ElseGroup, ConditionTypeOrReference, ConditionTarget, ConditionValue1, ConditionValue2, ConditionValue3, NegativeCondition, ErrorType, ErrorTextId, ScriptName, Comment) VALUES
  (17, 0, 901040, 0, 0, 31, 1, 3, 56172, 0, 0, 0, 0, '', 'I-387 Tame Ash Moth - only on an Ash Moth'),
  (17, 0, 901041, 0, 0, 31, 1, 3, 56174, 0, 0, 0, 0, '', 'I-387 Tame Pei-Wu Tiger Cub - only on a Pei-Wu Tiger Cub'),
  (17, 0, 901042, 0, 0, 31, 1, 3, 55946, 0, 0, 0, 0, '', 'I-387 Tame Pei-Wu Tiger - only on a Pei-Wu Tiger');
DELETE FROM `spell_script_names` WHERE spell_id BETWEEN 901040 AND 901045;
INSERT INTO `spell_script_names` (spell_id, ScriptName) VALUES
  (901040, 'spell_hun_tame_beast'), (901041, 'spell_hun_tame_beast'), (901042, 'spell_hun_tame_beast'),
  (901043, 'spell_hun_taming_the_beast'), (901044, 'spell_hun_taming_the_beast'), (901045, 'spell_hun_taming_the_beast');
DELETE FROM `creature_text` WHERE CreatureID = 901045;
INSERT INTO `creature_text` (CreatureID, GroupID, ID, Text, Type, Language, Probability, Emote, Duration, Sound, BroadcastTextId, TextRange, comment) VALUES
  (901045, 0, 0, 'Who dares summon the power of the void?', 12, 8, 100, 0, 0, 0, 1986, 0, 'Unbound Voidwalker - summoned (stock 5676)'),
  (901045, 1, 0, 'You will live forever in torment for this, pathetic warlock.', 12, 8, 100, 0, 0, 0, 1987, 0, 'Unbound Voidwalker - aggro (stock 5676)'),
  (901045, 2, 0, 'Enough... The orb has spoken. I serve.', 12, 0, 100, 0, 0, 0, 0, 0, 'Unbound Voidwalker - submits (I-387)');
DELETE FROM `smart_scripts` WHERE entryorguid = 901045 AND source_type = 0;
DELETE FROM `smart_scripts` WHERE entryorguid IN (90104500, 90104501) AND source_type = 9;
INSERT INTO `smart_scripts` (entryorguid, source_type, id, link, event_type, event_phase_mask, event_chance, event_flags, event_param1, event_param2, event_param3, event_param4, event_param5, event_param6, action_type, action_param1, action_param2, action_param3, action_param4, action_param5, action_param6, target_type, target_param1, target_param2, target_param3, target_param4, target_x, target_y, target_z, target_o, comment) VALUES
  (901045, 0, 0, 0, 54, 0, 100, 1, 0, 0, 0, 0, 0, 0, 80, 90104500, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - On Just Summoned - Run Intro'),
  (901045, 0, 1, 0, 2, 0, 100, 1, 0, 30, 0, 0, 0, 0, 11, 7750, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Between 0-30% Health - Cast Consuming Rage'),
  (901045, 0, 2, 0, 4, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - On Aggro - Say Line 1'),
  (901045, 0, 3, 0, 21, 0, 100, 0, 0, 0, 0, 0, 0, 0, 41, 1000, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - On Reached Home - Despawn'),
  (901045, 0, 4, 0, 2, 0, 100, 1, 0, 15, 0, 0, 0, 0, 80, 90104501, 2, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Between 0-15% Health - Run Submit'),
  (90104500, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 42, 0, 10, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Invincible below 10% health'),
  (90104500, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 35, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Set Faction 35'),
  (90104500, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 11, 7741, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Cast Summoned Demon'),
  (90104500, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Say Line 0'),
  (90104500, 9, 4, 0, 0, 0, 100, 0, 3000, 3000, 0, 0, 0, 0, 2, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Set Faction 14'),
  (90104500, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 49, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Intro - Start Attacking'),
  (90104501, 9, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 35, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Set Faction 35'),
  (90104501, 9, 1, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Combat Stop'),
  (90104501, 9, 2, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Set Passive'),
  (90104501, 9, 3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 5, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Emote Bow'),
  (90104501, 9, 4, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Say Line 2'),
  (90104501, 9, 5, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 33, 901045, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Kill Credit to Summoner'),
  (90104501, 9, 6, 0, 0, 0, 100, 0, 2500, 2500, 0, 0, 0, 0, 86, 697, 2, 23, 0, 0, 0, 23, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Summoner casts Summon Voidwalker (triggered)'),
  (90104501, 9, 7, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Unbound Voidwalker - Submit - Despawn');
DELETE FROM `event_scripts` WHERE id = 901046;
INSERT INTO `event_scripts` (id, delay, command, datalong, datalong2, dataint, x, y, z, o) VALUES
  (901046, 0, 10, 901045, 180000, 0, 406.60, 3636.00, 90.73, 0);
DELETE FROM `gameobject_template` WHERE entry = 901040;
INSERT INTO `gameobject_template` (entry, type, displayId, name, size, Data0, Data1) VALUES (901040, 8, 465, 'Summoning Circle', 2, 1653, 10);
DELETE FROM `gameobject_template_addon` WHERE entry = 901040;
INSERT INTO `gameobject_template_addon` (entry, faction) VALUES (901040, 35);
DELETE FROM `gameobject` WHERE guid = 13409901;
INSERT INTO `gameobject` (guid, id, map, spawnMask, phaseMask, position_x, position_y, position_z, orientation, rotation0, rotation1, rotation2, rotation3, spawntimesecs, animprogress, state, Comment) VALUES
  (13409901, 901040, 860, 1, 1, 406.60, 3636.00, 90.73, 0, 0, 0, 0, 1, 300, 100, 1, '[I-387] Summoning Circle - Korga''s camp');
DELETE FROM `gameobject` WHERE guid = 13409901 AND NOT @AracTrainers;
