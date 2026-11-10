-- charbaseinfo: the classes of @TitanHome

DELETE FROM `charbaseinfo` WHERE `race` = @Titan;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Titan, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @TitanHome) AS `home`;
