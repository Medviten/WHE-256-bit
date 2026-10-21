-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @MechagnomeMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@MechagnomeMask, 0, @MechagnomeRacials, 0, @MechagnomeRacialNameenUS);