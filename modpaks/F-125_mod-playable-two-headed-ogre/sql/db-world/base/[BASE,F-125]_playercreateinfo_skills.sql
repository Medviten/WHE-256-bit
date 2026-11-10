-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @TwoHeadedOgreMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@TwoHeadedOgreMask, 0, @TwoHeadedOgreRacials, 0, @TwoHeadedOgreRacialNameenUS);
