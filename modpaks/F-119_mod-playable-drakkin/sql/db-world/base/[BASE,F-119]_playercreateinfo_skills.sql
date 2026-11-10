-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DrakkinMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@DrakkinMask, 0, @DrakkinRacials, 0, @DrakkinRacialNameenUS);
