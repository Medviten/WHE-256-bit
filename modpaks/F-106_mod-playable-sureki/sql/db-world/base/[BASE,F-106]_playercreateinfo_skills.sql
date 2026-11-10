-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SurekiMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@SurekiMask, 0, @SurekiRacials, 0, @SurekiRacialNameenUS);
