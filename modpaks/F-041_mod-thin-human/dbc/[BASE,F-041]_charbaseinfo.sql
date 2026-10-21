-- charbaseinfo: the classes of @ThinHumanHome

DELETE FROM `charbaseinfo` WHERE `race` = @ThinHuman;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @ThinHuman, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @ThinHumanHome) AS `home`;
