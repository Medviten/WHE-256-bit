-- [I-378] Gilneas class trainer quests target Cataclysm spells the WotLK client cannot train yet.
--
-- Quests 14266-14283 come over unchanged from Neltharion (Cataclysm), so their objectives, texts and the generated
-- SmartAI spellhit credit rows name Cataclysm's low-level signature ability of each class. On 3.3.5a several of
-- those spells train far above the quest's level 2-3:
--   14266 Warrior  100 Charge          -> level 4
--   14276 Hunter 56641 Steady Shot     -> level 50
--   14279 Priest  2061 Flash Heal      -> level 20
--   14281 Mage    5143 Arcane Missiles -> level 8, and the text describes Cataclysm's "Arcane Missiles!" proc
--   14283 Druid    774 Rejuvenation    -> level 4
--
-- Fix, as Kezan's [I-273] does for F-013: all seven class quests become QuestLevel/MinLevel 4 and target the
-- ability the class trainer teaches at level 4.
--
--   Quest  Class    Trainer                   Spell                  ID
--   14266  Warrior  Sergeant Cleese           Charge                100  (unchanged)
--   14272  Rogue    Loren the Fence           Eviscerate           2098  (unchanged)
--   14274  Warlock  Vitus Darkwalker          Immolate              348  (unchanged)
--   14276  Hunter   Huntsman Blake            Serpent Sting        1978  (was 56641)
--   14279  Priest   Sister Almyra             Lesser Heal          2052  (was 2061)
--   14281  Mage     Myriam Spellwaker         Frostbolt             116  (was 5143)
--   14283  Druid    Celestine of the Harvest  Rejuvenation          774  (unchanged)
--
-- The class quests are on the zone's main path (each leads to a Safety in Numbers quest, which Old Divisions 14157
-- needs), so players must reach level 4 before them without grinding. Stock XP up to there is 1,315 of the 2,700
-- that level 4 takes. The seven quests before them now give the most XP their level allows (difficulty 8) and the
-- class lead-ins (14265-14280, which send the player to the trainer) move to level 4 with their class quests:
--   14078 160 + 14091 340 + 14093 340 + 14094 340 + 14098 340 + 14099 500 + lead-in 710 = 2,730 XP
-- The kills 14093 needs come on top.
--
-- This file loads after zz_[AUTO,F-130]_*.sql ("[I-" sorts after "[AUTO,"), so the scoped updates override the
-- generated rows. The replacement spells and texts are hand-written choices, so they live here, not in the port.

-- ---------------------------------------------------------------------------
-- XP before the class quests
-- ---------------------------------------------------------------------------

UPDATE `quest_template` SET `RewardXPDifficulty` = 8 WHERE `ID` IN (14078, 14091, 14093, 14094, 14098, 14099);

-- class lead-ins: level 4 like the quests they lead to (MinLevel stays 1, so they're still offered)
UPDATE `quest_template` SET `QuestLevel` = 4, `RewardXPDifficulty` = 8
WHERE `ID` IN (14265, 14269, 14273, 14275, 14277, 14278, 14280);

-- ---------------------------------------------------------------------------
-- quest_template
-- ---------------------------------------------------------------------------

-- 14266 Warrior, 14272 Rogue, 14274 Warlock, 14283 Druid: spell already trainable at 4, level only
UPDATE `quest_template` SET `QuestLevel` = 4, `MinLevel` = 4 WHERE `ID` IN (14266, 14272, 14274, 14283);

-- 14276 Hunter: Steady Shot (level 50) -> Serpent Sting (level 4)
UPDATE `quest_template` SET
  `QuestLevel` = 4,
  `MinLevel` = 4,
  `LogTitle` = 'Serpent Sting',
  `LogDescription` = 'Speak to Huntsman Blake and learn Serpent Sting. Practice using Serpent Sting 2 times against a Bloodfang Worgen.',
  `ObjectiveText1` = 'Practice Serpent Sting'
WHERE `ID` = 14276;

-- 14279 Priest: Flash Heal (level 20) -> Lesser Heal (level 4)
UPDATE `quest_template` SET
  `QuestLevel` = 4,
  `MinLevel` = 4,
  `LogDescription` = 'Reach level 4 and learn ''Lesser Heal'' from Sister Almyra. Practice casting Lesser Heal 3 times on Wounded Guards.',
  `ObjectiveText1` = 'Practice Lesser Heal on Wounded Guard'
WHERE `ID` = 14279;

-- 14281 Mage: Arcane Missiles (level 8, Cataclysm proc wording) -> Frostbolt (level 4)
UPDATE `quest_template` SET
  `QuestLevel` = 4,
  `MinLevel` = 4,
  `LogTitle` = 'Frostbolt',
  `LogDescription` = 'Speak to Myriam Spellwaker and learn Frostbolt. Use Frostbolt against a Bloodfang Worgen.',
  `QuestDescription` = 'The path ahead is difficult, $N.  We must devote the entirety of our mental power to the task at hand.$B$BYet sometimes, that is not enough.  Sometimes the situation calls for raw firepower.$B$BI know just the spell for such a situation and I''ll be more than glad to share it with you. Once you''ve learned it, practice using it against the Bloodfang Worgen to our west.',
  `ObjectiveText1` = 'Practice Frostbolt'
WHERE `ID` = 14281;

-- ---------------------------------------------------------------------------
-- smart_scripts: repoint the generated spellhit credit rows (cata_gilneas_port.py's cast credit)
--
-- Bloodfang Worgen 35118 gives the hunter's credit as 44175 "Spell Practice Credit" (its KillCredit1) and the mage's
-- as itself; Wounded Guard 47091 gives the priest's and druid's. Scoped to event_type 8 (SPELLHIT) and the old spell.
-- ---------------------------------------------------------------------------

-- Hunter: 56641 Steady Shot -> 1978 Serpent Sting
UPDATE `smart_scripts` SET `event_param1` = 1978, `comment` = 'quest 14276: credit when hit by 1978 (I-378)'
WHERE `source_type` = 0 AND `entryorguid` IN (35118, 44175) AND `event_type` = 8 AND `event_param1` = 56641;

-- Mage: 5143 Arcane Missiles -> 116 Frostbolt
UPDATE `smart_scripts` SET `event_param1` = 116, `comment` = 'quest 14281: credit when hit by 116 (I-378)'
WHERE `source_type` = 0 AND `entryorguid` = 35118 AND `event_type` = 8 AND `event_param1` = 5143;

-- Priest: 2061 Flash Heal -> 2052 Lesser Heal rank 2
UPDATE `smart_scripts` SET `event_param1` = 2052, `comment` = 'quest 14279: credit when hit by 2052 (I-378)'
WHERE `source_type` = 0 AND `entryorguid` = 47091 AND `event_type` = 8 AND `event_param1` = 2061;

-- SPELLHIT matches one exact spell id, so the ranks a player may cast instead also give credit: Lesser Heal rank 1
-- (2050, known from level 1) and rank 3 (591, level 6), Rejuvenation rank 2 (1058, level 10). Rows 910-912 belong
-- to this file.
DELETE FROM `smart_scripts` WHERE `source_type` = 0 AND `entryorguid` = 47091 AND `id` IN (910, 911, 912);
INSERT INTO `smart_scripts`
  (`entryorguid`, `source_type`, `id`, `link`, `event_type`, `event_phase_mask`, `event_chance`, `event_flags`,
   `event_param1`, `event_param2`, `event_param3`, `event_param4`, `event_param5`, `event_param6`,
   `action_type`, `action_param1`, `action_param2`, `action_param3`, `action_param4`, `action_param5`, `action_param6`,
   `target_type`, `target_param1`, `target_param2`, `target_param3`, `target_param4`,
   `target_x`, `target_y`, `target_z`, `target_o`, `comment`)
VALUES
  (47091, 0, 910, 0, 8, 0, 100, 0, 2050, 0, 0, 0, 0, 0, 33, 47091, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 14279: credit when hit by 2050 (I-378)'),
  (47091, 0, 911, 0, 8, 0, 100, 0, 591, 0, 0, 0, 0, 0, 33, 47091, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 14279: credit when hit by 591 (I-378)'),
  (47091, 0, 912, 0, 8, 0, 100, 0, 1058, 0, 0, 0, 0, 0, 33, 47091, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 'quest 14283: credit when hit by 1058 (I-378)');
