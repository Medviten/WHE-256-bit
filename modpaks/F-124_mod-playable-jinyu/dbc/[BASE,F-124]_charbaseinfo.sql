-- charbaseinfo: the classes of @JinyuHome

DELETE FROM `charbaseinfo` WHERE `race` = @Jinyu;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Jinyu, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @JinyuHome) AS `home`;
