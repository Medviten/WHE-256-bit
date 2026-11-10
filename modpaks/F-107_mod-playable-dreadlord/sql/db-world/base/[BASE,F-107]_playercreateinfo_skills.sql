-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DreadlordMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@DreadlordMask, 0, @DreadlordRacials, 0, @DreadlordRacialNameenUS);
