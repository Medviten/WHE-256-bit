/*Updates existing starting skills to include Alliance Pandaren where relevant
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @AlliancePandarenMask WHERE `skill` = 45; -- Bows
-- UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @AlliancePandarenMask WHERE `skill` = 46; -- Guns
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @AlliancePandarenMask WHERE `skill` = 226; -- Crossbows
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @AlliancePandarenMask WHERE `skill` = 173; -- Daggers
UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @AlliancePandarenMask WHERE `skill` = 160; -- 2H-maces

UPDATE `playercreateinfo_skills` SET `racemask` = `racemask` | @AlliancePandarenMask WHERE `skill` = 98; -- Common language
*/

-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` IN (@AlliancePandarenMask) AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@AlliancePandarenMask, 0, @AlliancePandarenRacials, 0, 'AlliancePandaren - Racial');
