-- charbaseinfo: the classes of @HordeEarthenHome

DELETE FROM `charbaseinfo` WHERE `race` = @HordeEarthen;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @HordeEarthen, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @HordeEarthenHome) AS `home`;
