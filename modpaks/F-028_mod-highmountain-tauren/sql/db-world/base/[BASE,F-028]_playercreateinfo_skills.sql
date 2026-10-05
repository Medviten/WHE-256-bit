-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @HighmountainTaurenMask AND `classMask` = 0 AND `skill` = @HighmountainTaurenRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@HighmountainTaurenMask, 0, @HighmountainTaurenRacials, 0, 'Highmountain Tauren - Racial');
