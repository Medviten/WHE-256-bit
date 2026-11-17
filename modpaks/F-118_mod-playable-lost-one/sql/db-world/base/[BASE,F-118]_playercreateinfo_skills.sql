-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @LostOneMask AND `raceMask_2` = @LostOneMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@LostOneMask, 0, @LostOneRacials, 0, @LostOneRacialNameenUS, @LostOneMask_2);
