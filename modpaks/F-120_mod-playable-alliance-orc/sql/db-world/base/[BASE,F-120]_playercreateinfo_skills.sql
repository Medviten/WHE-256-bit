-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @AllianceOrcMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@AllianceOrcMask, 0, @AllianceOrcRacials, 0, @AllianceOrcRacialNameenUS);
