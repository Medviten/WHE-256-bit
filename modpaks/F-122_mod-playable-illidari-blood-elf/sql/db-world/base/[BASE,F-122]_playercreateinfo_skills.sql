-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @IllidariBloodElfMask AND `raceMask_2` = @IllidariBloodElfMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@IllidariBloodElfMask, 0, @IllidariBloodElfRacials, 0, @IllidariBloodElfRacialNameenUS, @IllidariBloodElfMask_2);
