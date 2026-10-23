-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @FurbolgMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@FurbolgMask, 0, @FurbolgRacials, 0, @FurbolgRacialNameenUS);