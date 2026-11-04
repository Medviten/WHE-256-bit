-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @ManariMask AND `raceMask_2` = @ManariMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@ManariMask, 0, @ManariRacials, 0, @ManariRacialNameenUS, @ManariMask_2);
