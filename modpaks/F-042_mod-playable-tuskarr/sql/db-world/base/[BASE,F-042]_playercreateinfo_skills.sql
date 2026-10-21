-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @TuskarrMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@TuskarrMask, 0, @TuskarrRacials, 0, @TuskarrRacialNameenUS);