-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HordeSkyborneMask AND `raceMask_2` = @HordeSkyborneMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@HordeSkyborneMask, 0, @HordeSkyborneRacials, 0, @HordeSkyborneRacialNameenUS, @HordeSkyborneMask_2);
