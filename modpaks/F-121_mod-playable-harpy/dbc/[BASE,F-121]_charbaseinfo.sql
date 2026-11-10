-- charbaseinfo: the classes of @HarpyHome

DELETE FROM `charbaseinfo` WHERE `race` = @Harpy;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Harpy, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @HarpyHome) AS `home`;
