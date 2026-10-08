-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @DarkIronDwarfMask AND `classMask` = 0 AND `skill` = @DarkIronDwarfRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@DarkIronDwarfMask, 0, @DarkIronDwarfRacials, 0, @DarkIronDwarfRacialNameenUS);
