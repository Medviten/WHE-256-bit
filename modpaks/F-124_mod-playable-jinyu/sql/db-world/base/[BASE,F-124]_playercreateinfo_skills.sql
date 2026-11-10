-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @JinyuMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@JinyuMask, 0, @JinyuRacials, 0, @JinyuRacialNameenUS);
