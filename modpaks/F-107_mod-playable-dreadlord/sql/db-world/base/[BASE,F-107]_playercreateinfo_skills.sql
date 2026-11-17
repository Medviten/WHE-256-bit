-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DreadlordMask AND `raceMask_2` = @DreadlordMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@DreadlordMask, 0, @DreadlordRacials, 0, @DreadlordRacialNameenUS, @DreadlordMask_2);
