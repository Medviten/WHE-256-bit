-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HarpyMask AND `raceMask_2` = @HarpyMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@HarpyMask, 0, @HarpyRacials, 0, @HarpyRacialNameenUS, @HarpyMask_2);
