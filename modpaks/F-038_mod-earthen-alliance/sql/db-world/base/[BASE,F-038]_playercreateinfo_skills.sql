-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @AllianceEarthenMask AND `raceMask_2` = @AllianceEarthenMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@AllianceEarthenMask, 0, @AllianceEarthenRacials, 0, @AllianceEarthenRacialNameenUS, @AllianceEarthenMask_2);