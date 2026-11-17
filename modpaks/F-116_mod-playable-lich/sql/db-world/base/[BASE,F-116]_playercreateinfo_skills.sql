-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @LichMask AND `raceMask_2` = @LichMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@LichMask, 0, @LichRacials, 0, @LichRacialNameenUS, @LichMask_2);
