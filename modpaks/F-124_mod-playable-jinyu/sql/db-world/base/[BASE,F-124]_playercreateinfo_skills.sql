-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @JinyuMask AND `raceMask_2` = @JinyuMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@JinyuMask, 0, @JinyuRacials, 0, @JinyuRacialNameenUS, @JinyuMask_2);
