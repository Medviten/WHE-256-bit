-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @ZandalariTrollMask AND `classMask` = 0 AND `skill` = @ZandalariTrollRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@ZandalariTrollMask, 0, @ZandalariTrollRacials, 0, 'Zandalari Troll - Racial');
