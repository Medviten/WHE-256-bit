/* ARAC additions */

DELETE FROM `charbaseinfo` WHERE `race` = 14 AND `class` = 2;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (14, 2); -- mag'har orc paladin
DELETE FROM `charbaseinfo` WHERE `race` = 14 AND `class` = 11;
INSERT INTO `charbaseinfo` (`race`, `class`) VALUES (14, 11); -- mag'har orc druid
