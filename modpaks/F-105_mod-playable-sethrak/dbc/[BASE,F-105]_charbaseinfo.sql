-- charbaseinfo: the classes of @SethrakHome

DELETE FROM `charbaseinfo` WHERE `race` = @Sethrak;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Sethrak, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @SethrakHome) AS `home`;
