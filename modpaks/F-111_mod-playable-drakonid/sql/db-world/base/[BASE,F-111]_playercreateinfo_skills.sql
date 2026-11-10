-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DrakonidMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@DrakonidMask, 0, @DrakonidRacials, 0, @DrakonidRacialNameenUS);
