-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SethrakMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@SethrakMask, 0, @SethrakRacials, 0, @SethrakRacialNameenUS);
