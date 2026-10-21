-- charbaseinfo: the classes of @AllianceEarthenHome

DELETE FROM `charbaseinfo` WHERE `race` = @AllianceEarthen;
INSERT INTO `charbaseinfo` (`race`, `class`)
SELECT @AllianceEarthen, `class` FROM (SELECT `class` FROM `charbaseinfo` WHERE `race` = @AllianceEarthenHome) AS `home`;
