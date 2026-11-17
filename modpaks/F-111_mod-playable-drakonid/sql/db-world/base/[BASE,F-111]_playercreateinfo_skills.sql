-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DrakonidMask AND `raceMask_2` = @DrakonidMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@DrakonidMask, 0, @DrakonidRacials, 0, @DrakonidRacialNameenUS, @DrakonidMask_2);
