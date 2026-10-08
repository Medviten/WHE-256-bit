-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` IN (@HordePandarenMask) AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@HordePandarenMask, 0, @HordePandarenRacials, 0, @HordePandarenRacialNameenUS);
