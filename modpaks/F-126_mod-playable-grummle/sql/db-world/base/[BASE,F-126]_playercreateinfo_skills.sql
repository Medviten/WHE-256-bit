-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @GrummleMask AND `raceMask_2` = @GrummleMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@GrummleMask, 0, @GrummleRacials, 0, @GrummleRacialNameenUS, @GrummleMask_2);
