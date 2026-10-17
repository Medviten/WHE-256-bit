-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @VoidElfMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@VoidElfMask, 0, @VoidElfRacials, 0, @VoidElfRacialNameenUS);
