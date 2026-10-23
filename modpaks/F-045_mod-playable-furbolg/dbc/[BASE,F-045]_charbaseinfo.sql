-- charbaseinfo: the classes of @FurbolgHome

DELETE FROM `charbaseinfo` WHERE `race` = @Furbolg;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Furbolg, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @FurbolgHome) AS `home`;
