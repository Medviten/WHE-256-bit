-- charbaseinfo: the classes of @EluneChosenHome

DELETE FROM `charbaseinfo` WHERE `race` = @EluneChosen;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @EluneChosen, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @EluneChosenHome) AS `home`;
