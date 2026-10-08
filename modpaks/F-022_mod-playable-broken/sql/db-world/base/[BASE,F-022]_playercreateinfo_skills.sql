-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @BrokenMask AND `classMask` = 0 AND `skill` = @BrokenRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@BrokenMask, 0, @BrokenRacials, 0, @BrokenRacialNameenUS);
