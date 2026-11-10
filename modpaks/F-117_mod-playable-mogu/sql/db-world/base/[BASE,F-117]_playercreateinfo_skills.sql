-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @MoguMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@MoguMask, 0, @MoguRacials, 0, @MoguRacialNameenUS);
