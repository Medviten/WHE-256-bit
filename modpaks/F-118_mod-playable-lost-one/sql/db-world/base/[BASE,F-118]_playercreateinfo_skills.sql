-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @LostOneMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@LostOneMask, 0, @LostOneRacials, 0, @LostOneRacialNameenUS);
