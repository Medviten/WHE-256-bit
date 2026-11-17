-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DrakkinMask AND `raceMask_2` = @DrakkinMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@DrakkinMask, 0, @DrakkinRacials, 0, @DrakkinRacialNameenUS, @DrakkinMask_2);
