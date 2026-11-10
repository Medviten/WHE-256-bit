-- charbaseinfo: the classes of @LostOneHome

DELETE FROM `charbaseinfo` WHERE `race` = @LostOne;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @LostOne, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @LostOneHome) AS `home`;
