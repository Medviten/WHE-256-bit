-- charbaseinfo: the classes of @SaberonHome

DELETE FROM `charbaseinfo` WHERE `race` = @Saberon;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Saberon, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @SaberonHome) AS `home`;
