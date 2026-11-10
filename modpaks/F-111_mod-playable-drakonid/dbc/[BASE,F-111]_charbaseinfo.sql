-- charbaseinfo: the classes of @DrakonidHome

DELETE FROM `charbaseinfo` WHERE `race` = @Drakonid;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Drakonid, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @DrakonidHome) AS `home`;
