-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @VrykulMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@VrykulMask, 0, @VrykulRacials, 0, @VrykulRacialNameenUS);