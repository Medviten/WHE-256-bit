-- charbaseinfo: the classes of @SporelingHome

DELETE FROM `charbaseinfo` WHERE `race` = @Sporeling;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Sporeling, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @SporelingHome) AS `home`;
