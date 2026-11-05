-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @AllianceHaranirMask AND `raceMask_2` = @AllianceHaranirMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@AllianceHaranirMask, 0, @AllianceHaranirRacials, 0, @AllianceHaranirRacialNameenUS, @AllianceHaranirMask_2);
