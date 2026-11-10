-- charbaseinfo: the classes of @SurekiHome

DELETE FROM `charbaseinfo` WHERE `race` = @Sureki;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Sureki, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @SurekiHome) AS `home`;
