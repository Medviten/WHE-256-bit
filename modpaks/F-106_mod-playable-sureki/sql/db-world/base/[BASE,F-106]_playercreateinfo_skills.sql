-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SurekiMask AND `raceMask_2` = @SurekiMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@SurekiMask, 0, @SurekiRacials, 0, @SurekiRacialNameenUS, @SurekiMask_2);
