-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @NightborneMask AND `classMask` = 0 AND `skill` = @NightborneRacials;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`,`classMask`,`skill`,`rank`,`comment`)
VALUES (@NightborneMask, 0, @NightborneRacials, 0, @NightborneRacialNameenUS);
