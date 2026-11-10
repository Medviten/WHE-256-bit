-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @MoargMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@MoargMask, 0, @MoargRacials, 0, @MoargRacialNameenUS);
