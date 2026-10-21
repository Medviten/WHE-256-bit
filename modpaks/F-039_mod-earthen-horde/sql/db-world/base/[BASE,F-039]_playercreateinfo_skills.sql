-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HordeEarthenMask AND `raceMask_2` = @HordeEarthenMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@HordeEarthenMask, 0, @HordeEarthenRacials, 0, @HordeEarthenRacialNameenUS, @HordeEarthenMask_2);