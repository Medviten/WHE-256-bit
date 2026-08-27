-- ARAC additions

DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 2;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 2); -- ogre paladin
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 4;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 4); -- ogre rogue
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 5;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 5); -- ogre priest
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 6;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 6); -- ogre death knight
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 11;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 11); -- ogre druid
