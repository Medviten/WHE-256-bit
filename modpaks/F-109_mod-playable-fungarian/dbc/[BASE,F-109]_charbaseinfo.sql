-- charbaseinfo: the classes of @FungarianHome

DELETE FROM `charbaseinfo` WHERE `race` = @Fungarian;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Fungarian, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @FungarianHome) AS `home`;
