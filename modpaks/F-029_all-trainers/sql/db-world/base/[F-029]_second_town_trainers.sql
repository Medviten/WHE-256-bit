/* Class trainers in the second towns (Goldshire, Kharanos, Dolanaar, Azure Watch, Razor Hill, Bloodhoof Village, Brill,
   Falconwing Square) for the classes ARAC adds there and Cataclysm didn't (its own new trainers come from Neltharion,
   zz_[AUTO,F-029]_*). Each is a new NPC copied from a stock trainer of the same class and faction (stats, look,
   equipment, gossip, trainer list), but none of its quests, beside a stock trainer of the town. */
DROP TEMPORARY TABLE IF EXISTS `f029_clones`;
CREATE TEMPORARY TABLE `f029_clones` (`new_entry` INT UNSIGNED, `src` INT UNSIGNED, `new_name` VARCHAR(100));
INSERT INTO `f029_clones` VALUES
(142044, 17212, 'Haruun'), -- Goldshire Shaman Trainer
(142045, 3602, 'Faerin Dawnleaf'), -- Goldshire Druid Trainer
(142046, 3602, 'Theron Mossbrook'), -- Kharanos Druid Trainer
(142047, 17483, 'Vaelura'), -- Dolanaar Paladin Trainer
(142048, 17212, 'Kaarun'), -- Dolanaar Shaman Trainer
(142049, 3599, 'Elarion Duskstep'), -- Azure Watch Rogue Trainer
(142050, 906, 'Edmund Graves'), -- Azure Watch Warlock Trainer
(142051, 3602, 'Ilthas Starbough'), -- Azure Watch Druid Trainer
(142052, 16275, 'Liriel Dawnward'), -- Razor Hill Paladin Trainer
(142053, 5880, 'Zun''jaka'), -- Razor Hill Mage Trainer
(142054, 3170, 'Grutok'), -- Bloodhoof Village Rogue Trainer
(142055, 16269, 'Aelynna Sunwhisper'), -- Bloodhoof Village Mage Trainer
(142056, 3172, 'Murgash Bleakeye'), -- Bloodhoof Village Warlock Trainer
(142057, 16275, 'Saelia Brightvow'), -- Brill Paladin Trainer
(142058, 3173, 'Dorgal Stormtongue'), -- Brill Shaman Trainer
(142059, 3064, 'Halani Rainmane'), -- Brill Druid Trainer
(142060, 3173, 'Throm Earthcaller'), -- Falconwing Square Shaman Trainer
(142061, 3064, 'Kaya Mistrunner'); -- Falconwing Square Druid Trainer

DELETE FROM `creature_template` WHERE `entry` IN (142044, 142045, 142046, 142047, 142048, 142049, 142050, 142051, 142052, 142053, 142054, 142055, 142056, 142057, 142058, 142059, 142060, 142061);
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (142044, 142045, 142046, 142047, 142048, 142049, 142050, 142051, 142052, 142053, 142054, 142055, 142056, 142057, 142058, 142059, 142060, 142061);
DELETE FROM `creature_template_addon` WHERE `entry` IN (142044, 142045, 142046, 142047, 142048, 142049, 142050, 142051, 142052, 142053, 142054, 142055, 142056, 142057, 142058, 142059, 142060, 142061);
DELETE FROM `creature_equip_template` WHERE `CreatureID` IN (142044, 142045, 142046, 142047, 142048, 142049, 142050, 142051, 142052, 142053, 142054, 142055, 142056, 142057, 142058, 142059, 142060, 142061);
DELETE FROM `creature_default_trainer` WHERE `CreatureId` IN (142044, 142045, 142046, 142047, 142048, 142049, 142050, 142051, 142052, 142053, 142054, 142055, 142056, 142057, 142058, 142059, 142060, 142061);

DROP TEMPORARY TABLE IF EXISTS `f029_clone_templates`;
CREATE TEMPORARY TABLE `f029_clone_templates` SELECT m.`new_entry`, m.`new_name`, c.*
  FROM `f029_clones` m JOIN `creature_template` c ON c.`entry` = m.`src`;
UPDATE `f029_clone_templates` SET `entry` = `new_entry`, `name` = `new_name`, `KillCredit1` = 0, `KillCredit2` = 0;
ALTER TABLE `f029_clone_templates` DROP COLUMN `new_entry`, DROP COLUMN `new_name`;
INSERT INTO `creature_template` SELECT * FROM `f029_clone_templates`;
DROP TEMPORARY TABLE `f029_clone_templates`;

INSERT INTO `creature_template_model` (`CreatureID`, `Idx`, `CreatureDisplayID`, `DisplayScale`, `Probability`, `VerifiedBuild`)
  SELECT m.`new_entry`, t.`Idx`, t.`CreatureDisplayID`, t.`DisplayScale`, t.`Probability`, 0
  FROM `f029_clones` m JOIN `creature_template_model` t ON t.`CreatureID` = m.`src`;
INSERT INTO `creature_template_addon` (`entry`, `path_id`, `mount`, `bytes1`, `bytes2`, `emote`, `visibilityDistanceType`, `auras`)
  SELECT m.`new_entry`, 0, a.`mount`, a.`bytes1`, a.`bytes2`, a.`emote`, a.`visibilityDistanceType`, a.`auras`
  FROM `f029_clones` m JOIN `creature_template_addon` a ON a.`entry` = m.`src`;
INSERT INTO `creature_equip_template` (`CreatureID`, `ID`, `ItemID1`, `ItemID2`, `ItemID3`, `VerifiedBuild`)
  SELECT m.`new_entry`, q.`ID`, q.`ItemID1`, q.`ItemID2`, q.`ItemID3`, 0
  FROM `f029_clones` m JOIN `creature_equip_template` q ON q.`CreatureID` = m.`src`;
INSERT INTO `creature_default_trainer` (`CreatureId`, `TrainerId`)
  SELECT m.`new_entry`, d.`TrainerId` FROM `f029_clones` m JOIN `creature_default_trainer` d ON d.`CreatureId` = m.`src`;
DROP TEMPORARY TABLE `f029_clones`;

/* Two yards apart, beside the town's stock warrior (Falconwing Square: rogue) trainer, facing the same way */
DELETE FROM `creature` WHERE `guid` BETWEEN 6210200 AND 6210217;
INSERT INTO `creature` (`guid`, `id`, `map`, `zoneId`, `areaId`, `spawnMask`, `phaseMask`, `equipment_id`, `position_x`, `position_y`, `position_z`, `orientation`, `spawntimesecs`, `wander_distance`, `currentwaypoint`, `curhealth`, `curmana`, `MovementType`, `npcflag`, `unit_flags`, `dynamicflags`, `ScriptName`, `VerifiedBuild`, `CreateObject`, `Comment`) VALUES
(6210200, 142044, 0, 0, 0, 1, 1, 1, -9462.789, 107.587, 57.8784, 2.6529, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Goldshire Shaman trainer'),
(6210201, 142045, 0, 0, 0, 1, 1, 1, -9460.911, 111.119, 57.8784, 2.6529, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Goldshire Druid trainer'),
(6210202, 142046, 0, 0, 0, 1, 1, 1, -5606.077, -528.415, 399.7380, 0.1745, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Kharanos Druid trainer'),
(6210203, 142047, 1, 0, 0, 1, 1, 1, 9820.417, 952.852, 1308.8600, 1.1345, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Dolanaar Paladin trainer'),
(6210204, 142048, 1, 0, 0, 1, 1, 1, 9824.043, 951.162, 1308.8600, 1.1345, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Dolanaar Shaman trainer'),
(6210205, 142049, 530, 0, 0, 1, 1, 1, -4167.035, -12536.644, 44.9161, 1.6930, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Azure Watch Rogue trainer'),
(6210206, 142050, 530, 0, 0, 1, 1, 1, -4163.065, -12536.156, 44.9161, 1.6930, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Azure Watch Warlock trainer'),
(6210207, 142051, 530, 0, 0, 1, 1, 1, -4169.020, -12536.887, 44.9161, 1.6930, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Azure Watch Druid trainer'),
(6210208, 142052, 1, 0, 0, 1, 1, 1, 309.355, -4827.895, 9.6629, 1.6232, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Razor Hill Paladin trainer'),
(6210209, 142053, 1, 0, 0, 1, 1, 1, 313.349, -4827.685, 9.6629, 1.6232, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Razor Hill Mage trainer'),
(6210210, 142054, 1, 0, 0, 1, 1, 1, -2345.986, -495.759, -8.9640, 4.7927, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Bloodhoof Village Rogue trainer'),
(6210211, 142055, 1, 0, 0, 1, 1, 1, -2349.974, -496.081, -8.9640, 4.7927, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Bloodhoof Village Mage trainer'),
(6210212, 142056, 1, 0, 0, 1, 1, 1, -2343.993, -495.599, -8.9640, 4.7927, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Bloodhoof Village Warlock trainer'),
(6210213, 142057, 0, 0, 0, 1, 1, 1, 2253.790, 240.194, 33.7170, 0.5061, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Brill Paladin trainer'),
(6210214, 142058, 0, 0, 0, 1, 1, 1, 2255.730, 236.696, 33.7170, 0.5061, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Brill Shaman trainer'),
(6210215, 142059, 0, 0, 0, 1, 1, 1, 2252.821, 241.943, 33.7170, 0.5061, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Brill Druid trainer'),
(6210216, 142060, 530, 0, 0, 1, 1, 1, 9535.409, -6877.554, 26.2321, 3.8223, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Falconwing Square Shaman trainer'),
(6210217, 142061, 530, 0, 0, 1, 1, 1, 9532.891, -6874.446, 26.2321, 3.8223, 300, 0, 0, 1, 0, 0, 0, 0, 0, '', 0, 0, 'Falconwing Square Druid trainer');
