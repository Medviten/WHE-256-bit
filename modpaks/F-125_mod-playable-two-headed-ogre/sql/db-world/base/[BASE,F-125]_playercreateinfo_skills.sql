-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @TwoHeadedOgreMask AND `raceMask_2` = @TwoHeadedOgreMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@TwoHeadedOgreMask, 0, @TwoHeadedOgreRacials, 0, @TwoHeadedOgreRacialNameenUS, @TwoHeadedOgreMask_2);
