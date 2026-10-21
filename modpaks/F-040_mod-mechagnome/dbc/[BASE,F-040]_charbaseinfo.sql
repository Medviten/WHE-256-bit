-- charbaseinfo: the classes of @MechagnomeHome

DELETE FROM `charbaseinfo` WHERE `race` = @Mechagnome;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @Mechagnome, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @MechagnomeHome) AS `home`;
