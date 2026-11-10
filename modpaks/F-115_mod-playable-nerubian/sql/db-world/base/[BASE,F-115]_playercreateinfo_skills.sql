-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @NerubianMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@NerubianMask, 0, @NerubianRacials, 0, @NerubianRacialNameenUS);
