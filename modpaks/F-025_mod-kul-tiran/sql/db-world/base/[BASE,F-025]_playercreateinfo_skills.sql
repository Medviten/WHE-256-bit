-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @KulTiranMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@KulTiranMask, 0, @KulTiranRacials, 0, @KulTiranRacialNameenUS);