/* Add racial skills */
DELETE FROM `playercreateinfo_skills` WHERE `raceMask` = @OgreMask AND `classMask` = 0;
INSERT IGNORE INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(@OgreMask, 0, @OgreRacials, 0, @OgreRacialNameenUS);
