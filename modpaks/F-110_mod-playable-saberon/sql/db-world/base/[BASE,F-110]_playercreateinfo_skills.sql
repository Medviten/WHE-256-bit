-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @SaberonMask AND `raceMask_2` = @SaberonMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@SaberonMask, 0, @SaberonRacials, 0, @SaberonRacialNameenUS, @SaberonMask_2);
