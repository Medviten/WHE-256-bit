-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @MoargMask AND `raceMask_2` = @MoargMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@MoargMask, 0, @MoargRacials, 0, @MoargRacialNameenUS, @MoargMask_2);
