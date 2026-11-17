-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @TitanMask AND `raceMask_2` = @TitanMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@TitanMask, 0, @TitanRacials, 0, @TitanRacialNameenUS, @TitanMask_2);
