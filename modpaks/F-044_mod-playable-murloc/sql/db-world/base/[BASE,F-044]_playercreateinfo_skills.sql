/* Add racial skills */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @MurlocMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@MurlocMask, 0, @MurlocRacials, 0, @MurlocRacialNameenUS);
