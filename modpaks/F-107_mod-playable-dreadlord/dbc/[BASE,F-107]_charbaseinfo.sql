-- charbaseinfo: the classes of @DreadlordHome

DELETE FROM `charbaseinfo` WHERE `race` = @Dreadlord;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Dreadlord, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @DreadlordHome) AS `home`;
