-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @EluneChosenMask AND `raceMask_2` = @EluneChosenMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@EluneChosenMask, 0, @EluneChosenRacials, 0, @EluneChosenRacialNameenUS, @EluneChosenMask_2);
