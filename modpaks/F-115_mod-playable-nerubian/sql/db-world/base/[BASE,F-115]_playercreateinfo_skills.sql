-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @NerubianMask AND `raceMask_2` = @NerubianMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@NerubianMask, 0, @NerubianRacials, 0, @NerubianRacialNameenUS, @NerubianMask_2);
