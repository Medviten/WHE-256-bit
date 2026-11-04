-- Racial skills
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @CultistMask AND `raceMask_2` = @CultistMask_2 AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`, `raceMask_2`) VALUES
(@CultistMask, 0, @CultistRacials, 0, @CultistRacialNameenUS, @CultistMask_2);
