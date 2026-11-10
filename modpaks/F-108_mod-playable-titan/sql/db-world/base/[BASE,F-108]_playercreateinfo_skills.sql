-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @TitanMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@TitanMask, 0, @TitanRacials, 0, @TitanRacialNameenUS);
