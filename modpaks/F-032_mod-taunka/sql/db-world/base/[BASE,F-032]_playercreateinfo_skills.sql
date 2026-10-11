-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @TaunkaMask AND `classMask` = 0 AND `skill` = @TaunkaRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@TaunkaMask, 0, @TaunkaRacials, 0, 'Highmountain Tauren - Racial');
