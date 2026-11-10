-- charbaseinfo: the classes of @IllidariBloodElfHome

DELETE FROM `charbaseinfo` WHERE `race` = @IllidariBloodElf;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @IllidariBloodElf, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @IllidariBloodElfHome) AS `home`;
