-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SporelingMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@SporelingMask, 0, @SporelingRacials, 0, @SporelingRacialNameenUS);
