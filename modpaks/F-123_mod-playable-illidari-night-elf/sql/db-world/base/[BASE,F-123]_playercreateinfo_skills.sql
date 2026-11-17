-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @IllidariNightElfMask AND `raceMask_2` = @IllidariNightElfMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@IllidariNightElfMask, 0, @IllidariNightElfRacials, 0, @IllidariNightElfRacialNameenUS, @IllidariNightElfMask_2);
