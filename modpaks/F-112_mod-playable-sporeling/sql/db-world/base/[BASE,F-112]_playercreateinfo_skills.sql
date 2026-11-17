-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SporelingMask AND `raceMask_2` = @SporelingMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@SporelingMask, 0, @SporelingRacials, 0, @SporelingRacialNameenUS, @SporelingMask_2);
