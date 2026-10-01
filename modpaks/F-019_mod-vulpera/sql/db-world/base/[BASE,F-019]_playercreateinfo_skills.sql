-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @VulperaMask AND `classMask` = 0 AND `skill` = @VulperaRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@VulperaMask, 0, @VulperaRacials, 0, 'Vulpera - Racial');
