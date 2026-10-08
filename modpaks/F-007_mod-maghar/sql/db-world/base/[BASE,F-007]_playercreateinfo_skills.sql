/* Add racial skills */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` IN (@MagharOrcMask) AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@MagharOrcMask, 0, @MagharOrcRacials, 0, @MagharOrcRacialNameenUS);
