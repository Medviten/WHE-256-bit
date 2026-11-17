-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @AllianceOrcMask AND `raceMask_2` = @AllianceOrcMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@AllianceOrcMask, 0, @AllianceOrcRacials, 0, @AllianceOrcRacialNameenUS, @AllianceOrcMask_2);
