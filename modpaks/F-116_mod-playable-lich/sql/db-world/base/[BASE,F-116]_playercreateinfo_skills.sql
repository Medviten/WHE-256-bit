-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @LichMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@LichMask, 0, @LichRacials, 0, @LichRacialNameenUS);
