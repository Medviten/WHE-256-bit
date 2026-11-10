-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @GrummleMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@GrummleMask, 0, @GrummleRacials, 0, @GrummleRacialNameenUS);
