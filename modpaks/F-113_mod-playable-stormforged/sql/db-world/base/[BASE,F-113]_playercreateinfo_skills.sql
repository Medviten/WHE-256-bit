-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @StormforgedMask AND `raceMask_2` = @StormforgedMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@StormforgedMask, 0, @StormforgedRacials, 0, @StormforgedRacialNameenUS, @StormforgedMask_2);
