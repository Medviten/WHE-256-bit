-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @StormforgedMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@StormforgedMask, 0, @StormforgedRacials, 0, @StormforgedRacialNameenUS);
