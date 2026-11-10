-- charbaseinfo: the classes of @LichHome

DELETE FROM `charbaseinfo` WHERE `race` = @Lich;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Lich, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @LichHome) AS `home`;
