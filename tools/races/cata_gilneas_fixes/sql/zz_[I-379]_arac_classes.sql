-- [I-379] Classes Gilneas has no trainer or class quest for (ARAC's paladins and shamans, F-100's heroes).
--
-- Gilneas' class trainers and class quests cover the seven Cataclysm Worgen classes. Each class quest leads to its
-- "Safety in Numbers" (14285-14291), and Old Divisions (14157) and While You're At It (24930) need one of those, so
-- any other class was stuck there. They now count as done for the classes without a Gilneas class quest.
--
-- With F-029 (all trainers; its variables.sql sets @AllTrainersEnabled), a paladin and a shaman trainer also stand
-- beside Sister Almyra wherever she trains, in the same phases, as F-029 adds trainers to the stock starting areas.
-- Their gossip is stock's (Aurelon's paladin menu 7260, the shaman menu 4103); their looks are Gilnean guard and
-- citizen displays.
--
-- Loads after zz_[AUTO,F-130]_*.sql ("[I-" sorts after "[AUTO,"). Spawn guids 13009901+ stay clear of the port's.

SET @GilneasAracTrainers = COALESCE(@AllTrainersEnabled, 0) <> 0;

-- ---------------------------------------------------------------------------
-- Main path: Safety in Numbers, or a class without a Gilneas class quest
-- (warrior 1, hunter 4, rogue 8, priest 16, mage 128, warlock 256, druid 1024 = 1437)
-- ---------------------------------------------------------------------------

DELETE FROM `conditions` WHERE `SourceTypeOrReferenceId` IN (19, 20) AND `SourceGroup` = 0
  AND `SourceEntry` IN (14157, 24930) AND `SourceId` = 0 AND `ElseGroup` = 7;
INSERT INTO `conditions` (`SourceTypeOrReferenceId`, `SourceGroup`, `SourceEntry`, `SourceId`, `ElseGroup`,
  `ConditionTypeOrReference`, `ConditionTarget`, `ConditionValue1`, `ConditionValue2`, `ConditionValue3`,
  `NegativeCondition`, `ErrorType`, `ErrorTextId`, `ScriptName`, `Comment`) VALUES
  (19, 0, 14157, 0, 7, 15, 0, 1437, 0, 0, 1, 0, 0, '', 'Old Divisions: classes without a Gilneas class quest (I-379)'),
  (19, 0, 24930, 0, 7, 15, 0, 1437, 0, 0, 1, 0, 0, '', 'While You''re At It: classes without a Gilneas class quest (I-379)');

-- ---------------------------------------------------------------------------
-- Paladin and shaman trainers (spawned only with F-029)
-- ---------------------------------------------------------------------------

DELETE FROM `creature_template` WHERE `entry` IN (@GilneasPaladinTrainerCreatureID, @GilneasShamanTrainerCreatureID);
INSERT INTO `creature_template` (`entry`, `difficulty_entry_1`, `difficulty_entry_2`, `difficulty_entry_3`, `KillCredit1`, `KillCredit2`, `name`, `subname`, `IconName`, `gossip_menu_id`, `minlevel`, `maxlevel`, `exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `speed_swim`, `speed_flight`, `detection_range`, `rank`, `dmgschool`, `DamageModifier`, `BaseAttackTime`, `RangeAttackTime`, `BaseVariance`, `RangeVariance`, `unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, `type_flags`, `lootid`, `pickpocketloot`, `skinloot`, `PetSpellDataId`, `VehicleId`, `mingold`, `maxgold`, `AIName`, `MovementType`, `HoverHeight`, `HealthModifier`, `ManaModifier`, `ArmorModifier`, `ExperienceModifier`, `RacialLeader`, `movementId`, `RegenHealth`, `CreatureImmunitiesId`, `flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES
  (@GilneasPaladinTrainerCreatureID, 0, 0, 0, 0, 0, 'Brother Aldous Harrow', 'Paladin Trainer', NULL, 7260, 5, 5, 0, 2163, 49, 1, 1.1429, 1, 1.1429, 18, 0, 0, 0.75, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0),
  (@GilneasShamanTrainerCreatureID, 0, 0, 0, 0, 0, 'Edwin Thornfield', 'Shaman Trainer', NULL, 4103, 5, 5, 0, 2163, 49, 1, 1.1429, 1, 1.1429, 18, 0, 0, 0.75, 2000, 2000, 1, 1, 2, 768, 2048, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, '', 0);

-- Gilneas City Guard (29466) and male citizen (30215) displays
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@GilneasPaladinTrainerCreatureID, @GilneasShamanTrainerCreatureID);
INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`) VALUES
  (@GilneasPaladinTrainerCreatureID, 0, 29466, 1, 1, 0),
  (@GilneasShamanTrainerCreatureID, 0, 30215, 1, 1, 0);

-- Full trainer lists, as the other Gilneas trainers have: Alliance paladin 3 (Brother Wilhelm), shaman 14 (Tuluun).
-- (6 and 15 are the starting-area lists, which stop at level 6)
DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN (@GilneasPaladinTrainerCreatureID, @GilneasShamanTrainerCreatureID);
INSERT INTO `creature_default_trainer` (`CreatureId`, `TrainerId`) VALUES
  (@GilneasPaladinTrainerCreatureID, 3),
  (@GilneasShamanTrainerCreatureID, 14);

-- 1.5 yards either side of each Sister Almyra spawn, same phase and facing
DELETE FROM `creature` WHERE `guid` BETWEEN 13009901 AND 13009910;
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) VALUES
  (13009901, @GilneasPaladinTrainerCreatureID, 0, 0, 0, 1, 2, 0, -1698.88, 1307.30, 19.7825, 1.1435, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas paladin trainer (I-379)'),
  (13009902, @GilneasShamanTrainerCreatureID, 0, 0, 0, 1, 2, 0, -1696.14, 1306.06, 19.7825, 1.1435, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas shaman trainer (I-379)'),
  (13009903, @GilneasPaladinTrainerCreatureID, 0, 0, 0, 1, 7, 0, -1894.29, 2306.75, 44.2471, 4.8520, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas paladin trainer (I-379)'),
  (13009904, @GilneasShamanTrainerCreatureID, 0, 0, 0, 1, 7, 0, -1897.27, 2306.33, 44.2471, 4.8520, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas shaman trainer (I-379)'),
  (13009905, @GilneasPaladinTrainerCreatureID, 0, 0, 0, 1, 8, 0, -2454.18, 1535.52, 25.1159, 3.4383, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas paladin trainer (I-379)'),
  (13009906, @GilneasShamanTrainerCreatureID, 0, 0, 0, 1, 8, 0, -2455.06, 1538.38, 25.1159, 3.4383, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas shaman trainer (I-379)'),
  (13009907, @GilneasPaladinTrainerCreatureID, 0, 0, 0, 1, 1032, 0, -1383.96, 1223.18, 35.6430, 3.7350, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas paladin trainer (I-379)'),
  (13009908, @GilneasShamanTrainerCreatureID, 0, 0, 0, 1, 1032, 0, -1385.64, 1225.66, 35.6430, 3.7350, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas shaman trainer (I-379)'),
  (13009909, @GilneasPaladinTrainerCreatureID, 0, 0, 0, 1, 8, 0, -1759.92, 1651.46, 20.9939, 2.7576, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas paladin trainer (I-379)'),
  (13009910, @GilneasShamanTrainerCreatureID, 0, 0, 0, 1, 8, 0, -1758.80, 1654.24, 20.9939, 2.7576, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 1, 'F-130 Gilneas shaman trainer (I-379)');
DELETE FROM `creature` WHERE `guid` BETWEEN 13009901 AND 13009910 AND NOT @GilneasAracTrainers;
