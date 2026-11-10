-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HarpyMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@HarpyMask, 0, @HarpyRacials, 0, @HarpyRacialNameenUS);
