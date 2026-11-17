-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @FungarianMask AND `raceMask_2` = @FungarianMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@FungarianMask, 0, @FungarianRacials, 0, @FungarianRacialNameenUS, @FungarianMask_2);
