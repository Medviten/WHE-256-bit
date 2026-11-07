-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @AllianceSkyborneMask AND `raceMask_2` = @AllianceSkyborneMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@AllianceSkyborneMask, 0, @AllianceSkyborneRacials, 0, @AllianceSkyborneRacialNameenUS, @AllianceSkyborneMask_2);
