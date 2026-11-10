-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @IllidariNightElfMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@IllidariNightElfMask, 0, @IllidariNightElfRacials, 0, @IllidariNightElfRacialNameenUS);
