-- charbaseinfo: 5 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 1;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 1); -- ogre warrior
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 3;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 3); -- ogre hunter
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 7;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 7); -- ogre shaman
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 8;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 8); -- ogre mage
DELETE FROM `charbaseinfo` WHERE `race` = 15 AND `class` = 9;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (15, 9); -- ogre warlock
