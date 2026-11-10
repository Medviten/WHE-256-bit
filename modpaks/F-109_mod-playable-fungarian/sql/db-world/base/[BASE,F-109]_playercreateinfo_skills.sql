-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @FungarianMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@FungarianMask, 0, @FungarianRacials, 0, @FungarianRacialNameenUS);
