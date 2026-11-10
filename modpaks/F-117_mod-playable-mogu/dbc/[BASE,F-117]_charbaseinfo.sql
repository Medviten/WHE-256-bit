-- charbaseinfo: the classes of @MoguHome

DELETE FROM `charbaseinfo` WHERE `race` = @Mogu;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Mogu, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @MoguHome) AS `home`;
