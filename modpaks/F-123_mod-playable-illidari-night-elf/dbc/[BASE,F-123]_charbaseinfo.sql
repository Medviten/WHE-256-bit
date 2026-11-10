-- charbaseinfo: the classes of @IllidariNightElfHome

DELETE FROM `charbaseinfo` WHERE `race` = @IllidariNightElf;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @IllidariNightElf, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @IllidariNightElfHome) AS `home`;
