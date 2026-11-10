-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @IllidariBloodElfMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@IllidariBloodElfMask, 0, @IllidariBloodElfRacials, 0, @IllidariBloodElfRacialNameenUS);
