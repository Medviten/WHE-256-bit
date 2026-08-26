-- ARAC additions

-- New entries
DELETE FROM `charbaseinfo` WHERE `race` = 9 AND `class` = 2;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (9, 2); -- goblin paladin
DELETE FROM `charbaseinfo` WHERE `race` = 9 AND `class` = 11;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (9, 11); -- goblin druid
DELETE FROM `charbaseinfo` WHERE `race` = 12 AND `class` = 2;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (12, 2); -- worgen paladin
DELETE FROM `charbaseinfo` WHERE `race` = 12 AND `class` = 7;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (12, 7); -- worgen shaman
