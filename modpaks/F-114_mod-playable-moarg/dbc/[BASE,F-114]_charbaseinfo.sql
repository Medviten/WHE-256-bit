-- charbaseinfo: the classes of @MoargHome

DELETE FROM `charbaseinfo` WHERE `race` = @Moarg;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Moarg, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @MoargHome) AS `home`;
