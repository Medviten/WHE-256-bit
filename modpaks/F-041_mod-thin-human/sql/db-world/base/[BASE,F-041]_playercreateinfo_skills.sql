-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @ThinHumanMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@ThinHumanMask, 0, @ThinHumanRacials, 0, @ThinHumanRacialNameenUS);