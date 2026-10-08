-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` IN (@AlliancePandarenMask) AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@AlliancePandarenMask, 0, @AlliancePandarenRacials, 0, @AlliancePandarenRacialNameenUS);
