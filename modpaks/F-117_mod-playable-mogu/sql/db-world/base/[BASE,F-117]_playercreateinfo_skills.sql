-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @MoguMask AND `raceMask_2` = @MoguMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@MoguMask, 0, @MoguRacials, 0, @MoguRacialNameenUS, @MoguMask_2);
