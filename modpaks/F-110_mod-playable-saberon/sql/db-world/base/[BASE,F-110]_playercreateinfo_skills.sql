-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SaberonMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@SaberonMask, 0, @SaberonRacials, 0, @SaberonRacialNameenUS);
