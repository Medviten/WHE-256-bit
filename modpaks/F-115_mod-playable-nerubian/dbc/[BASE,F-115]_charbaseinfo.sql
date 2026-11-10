-- charbaseinfo: the classes of @NerubianHome

DELETE FROM `charbaseinfo` WHERE `race` = @Nerubian;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Nerubian, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @NerubianHome) AS `home`;
