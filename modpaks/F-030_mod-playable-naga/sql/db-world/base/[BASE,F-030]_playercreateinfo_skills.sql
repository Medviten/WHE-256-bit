-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @NagaMask AND `classMask` = 0 AND `skill` = @NagaRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@NagaMask, 0, @NagaRacials, 0, 'Naga - Racial');
