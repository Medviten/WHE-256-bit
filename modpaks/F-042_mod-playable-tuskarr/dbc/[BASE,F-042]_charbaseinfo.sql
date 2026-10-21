-- charbaseinfo: the classes of @TuskarrHome

DELETE FROM `charbaseinfo` WHERE `race` = @Tuskarr;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Tuskarr, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @TuskarrHome) AS `home`;
