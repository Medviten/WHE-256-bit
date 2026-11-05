-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HordeHaranirMask AND `raceMask_2` = @HordeHaranirMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@HordeHaranirMask, 0, @HordeHaranirRacials, 0, @HordeHaranirRacialNameenUS, @HordeHaranirMask_2);
