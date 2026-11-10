-- charbaseinfo: the classes of @StormforgedHome

DELETE FROM `charbaseinfo` WHERE `race` = @Stormforged;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Stormforged, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @StormforgedHome) AS `home`;
