-- charbaseinfo: the classes of @DrakkinHome

DELETE FROM `charbaseinfo` WHERE `race` = @Drakkin;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Drakkin, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @DrakkinHome) AS `home`;
